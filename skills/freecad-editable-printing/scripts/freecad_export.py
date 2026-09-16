"""Worker executed by FreeCAD's bundled Python; invoked by export_project.py."""
import json
import os
from pathlib import Path
import sys
import zipfile
from xml.etree import ElementTree as E
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import FreeCAD as A
import FreeCADGui as G
import Mesh


def main(manifest):
    root = manifest.parent
    m = json.loads(manifest.read_text(encoding='utf-8-sig'))
    resolve = lambda p: (root/p).resolve()
    work = resolve(m.get('work', '.export'))
    G.showMainWindow(); G.getMainWindow().hide()
    d = A.openDocument(str(resolve(m['source'])))
    d.recompute()
    shapes = {}
    for obj in m['objects']:
        for part in obj['parts']:
            name = part['object']
            item = d.getObject(name)
            assert item is not None, f'No FreeCAD object: {name}'
            assert not item.Shape.isNull() and item.Shape.isValid() and item.Shape.Solids, f'Invalid solid: {name}'
            assert not any(s in ('Invalid', 'Error') for s in item.State), f'Feature error: {name}'
            shapes[name] = item.Shape.copy()
    for name in m.get('preserve_objects', []):
        assert d.getObject(name) is not None, f'Missing preserved feature: {name}'
    for obj in d.Objects:
        if obj.ViewObject:
            obj.ViewObject.Visibility = False
    visible = m.get('presentation', {}).get('objects', list(shapes))
    colors = m.get('presentation', {}).get('colors', {})
    for name in visible:
        obj = d.getObject(name)
        assert obj is not None, f'Unknown presentation object: {name}'
        obj.ViewObject.Visibility = True
        if getattr(obj, 'Tip', None):
            obj.Tip.ViewObject.Visibility = True
        if name in colors:
            obj.ViewObject.ShapeColor = tuple(colors[name])
    view = G.activeDocument().activeView()
    view.setAnimationEnabled(False)
    view.viewAxonometric(); view.fitAll(); G.updateGui()
    target = resolve(m['outputs']['freecad'])
    d.saveAs(str(target)); A.closeDocument(d.Name)
    d = A.openDocument(str(target)); d.recompute()
    for name, shape in shapes.items():
        reopened = d.getObject(name).Shape
        assert reopened.isValid() and abs(reopened.Volume-shape.Volume) <= max(1e-6, shape.Volume*1e-8), f'CAD reopen mismatch: {name}'
    for name in visible:
        assert d.getObject(name).ViewObject.Visibility, f'Hidden after reopening: {name}'
    from render_preview import render
    render([(d.getObject(name).Shape, colors.get(name, [.3,.35,.4])) for name in visible], resolve(m['outputs']['preview']))
    ns = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    E.register_namespace('', ns)
    def el(parent, tag, **attrs):
        return E.SubElement(parent, '{'+ns+'}'+tag, **attrs)
    model = E.Element('{'+ns+'}model', unit='millimeter')
    resources = el(model, 'resources'); build = el(model, 'build'); config = E.Element('config')
    ident = 0; checks = {}
    for obj in m['objects']:
        part_ids = []
        for part in obj['parts']:
            ident += 1; part_ids.append((ident, part))
            shape = shapes[part['object']]
            verts, faces = shape.tessellate(m.get('mesh_deflection', .015))
            mesh_check = Mesh.Mesh([(verts[a], verts[b], verts[c]) for a,b,c in faces])
            assert mesh_check.isSolid(), f'Open mesh: {part["object"]}'
            t = part.get('transform', [1,0,0,0,1,0,0,0,1,0,0,0])
            assert len(t) == 12
            det = t[0]*(t[4]*t[8]-t[5]*t[7])-t[1]*(t[3]*t[8]-t[5]*t[6])+t[2]*(t[3]*t[7]-t[4]*t[6])
            assert abs(det-1) < 1e-6, 'Use orientation-preserving rigid transforms (no reflection/scale)'
            basis = [A.Vector(*t[i:i+3]) for i in (0,3,6)]
            assert all(abs(v.Length-1)<1e-6 for v in basis) and all(abs(basis[i].dot(basis[j]))<1e-6 for i,j in [(0,1),(0,2),(1,2)])
            resource = el(resources, 'object', id=str(ident), type='model', name=part['name'])
            mesh = el(resource, 'mesh'); vv = el(mesh, 'vertices'); tt = el(mesh, 'triangles')
            transformed = []
            for v in verts:
                xyz = [v.x*t[k]+v.y*t[k+3]+v.z*t[k+6]+t[k+9] for k in range(3)]
                transformed.append(xyz)
                el(vv, 'vertex', **dict(zip('xyz', map(str, xyz))))
            assert min(v[2] for v in transformed) >= -1e-5, 'Part below bed'
            for a,b,c in faces:
                el(tt, 'triangle', v1=str(a), v2=str(b), v3=str(c))
            checks[part['name']] = {'solid': True, 'closed_mesh': True, 'triangles': len(faces)}
        ident += 1
        assembly = el(resources, 'object', id=str(ident), type='model', name=obj['name'])
        components = el(assembly, 'components')
        for pid, part in part_ids:
            el(components, 'component', objectid=str(pid))
        xy = obj['position']
        el(build, 'item', objectid=str(ident), transform=f'1 0 0 0 1 0 0 0 1 {xy[0]} {xy[1]} 0')
        co = E.SubElement(config, 'object', id=str(ident))
        E.SubElement(co, 'metadata', key='name', value=obj['name'])
        E.SubElement(co, 'metadata', key='extruder', value=str(obj['parts'][0]['extruder']))
        for pid, part in part_ids:
            assert 1 <= part['extruder'] <= len(m['bambu']['filaments'])
            pp = E.SubElement(co, 'part', id=str(pid), subtype='normal_part')
            for key, value in [('name',part['name']), ('extruder',str(part['extruder']))]:
                E.SubElement(pp, 'metadata', key=key, value=value)
    with zipfile.ZipFile(work/'geometry.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('3D/3dmodel.model', E.tostring(model))
        z.writestr('Metadata/model_settings.config', E.tostring(config))
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    (work/'cad-checks.json').write_text(json.dumps(checks, indent=2))
    A.closeDocument(d.Name)


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve())
