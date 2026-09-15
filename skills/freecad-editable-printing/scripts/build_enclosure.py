"""Run with FreeCAD's bundled Python. Creates a NEW proof document, not an editor."""
from pathlib import Path
import json
import FreeCAD as App
import Part
import Sketcher
import MeshPart

OUT = Path(__file__).resolve().parent
DEFAULTS = dict(Width=60, Depth=40, Height=25, Wall=2, Floor=2,
                LidThickness=2, LipHeight=4, LipWall=1.6, Clearance=0.3)
ROWS = {key: i + 2 for i, key in enumerate(DEFAULTS)}

def rectangle(sketch, width, depth, nominal_w, nominal_d):
    """Native constrained rectangle, centered on origin; expressions drive size."""
    points = [(-nominal_w/2, -nominal_d/2), (nominal_w/2, -nominal_d/2),
              (nominal_w/2, nominal_d/2), (-nominal_w/2, nominal_d/2)]
    first = sketch.GeometryCount
    for i in range(4):
        a, b = points[i], points[(i+1) % 4]
        sketch.addGeometry(Part.LineSegment(App.Vector(*a, 0), App.Vector(*b, 0)), False)
    for i in range(4):
        sketch.addConstraint(Sketcher.Constraint('Coincident', first+i, 2, first+(i+1)%4, 1))
        sketch.addConstraint(Sketcher.Constraint('Horizontal' if i%2 == 0 else 'Vertical', first+i))
    for constraint, expression in [
        (Sketcher.Constraint('DistanceX', first, 1, -nominal_w/2), '-('+width+')/2'),
        (Sketcher.Constraint('DistanceY', first, 1, -nominal_d/2), '-('+depth+')/2'),
        (Sketcher.Constraint('Distance', first, nominal_w), width),
        (Sketcher.Constraint('Distance', first+1, nominal_d), depth),
    ]:
        index = sketch.addConstraint(constraint)
        sketch.setExpression('Constraints[%d]' % index, expression)

def sketch(doc, body, name, z=None):
    obj = doc.addObject('Sketcher::SketchObject', name)
    body.addObject(obj)
    if z:
        obj.setExpression('Placement.Base.z', z)
    return obj

def pad(doc, body, profile, name, length):
    obj = body.newObject('PartDesign::Pad', name)
    obj.Profile = profile
    obj.setExpression('Length', length)
    doc.recompute()
    profile.Visibility = False
    for previous in body.Group:
        if previous != obj:
            previous.Visibility = False
    return obj

def create():
    doc = App.newDocument('EditableEnclosure')
    sheet = doc.addObject('Spreadsheet::Sheet', 'Parameters')
    sheet.Label = 'Parameters (edit column B, millimeters)'
    sheet.set('A1', 'Parameter'); sheet.set('B1', 'Value'); sheet.set('C1', 'Meaning')
    meanings = ['Outer width', 'Outer depth', 'Enclosure height excluding lid',
                'Side wall thickness', 'Bottom thickness', 'Lid plate thickness',
                'Insertion depth of lid lip', 'Lip ring thickness', 'Gap PER SIDE; slip fit, not a latch']
    for (key, val), meaning in zip(DEFAULTS.items(), meanings):
        row = ROWS[key]
        sheet.set('A'+str(row), key); sheet.set('B'+str(row), str(val)+' mm')
        sheet.setAlias('B'+str(row), key); sheet.set('C'+str(row), meaning)
    sheet.setColumnWidth('A', 165); sheet.setColumnWidth('B', 100); sheet.setColumnWidth('C', 350)
    sheet.setBackground('B2:B10', (1.0, 0.94, 0.70))
    sheet.set('A12', 'Edit yellow cells; recompute (F5). Both parts share these dimensions.')
    sheet.set('A13', 'Keep Height > Floor + LipHeight; all thicknesses and clearance positive.')
    sheet.set('A14', 'Min(Width,Depth) > 2*(Wall+Clearance+LipWall). Lid is shown print-side down.')
    doc.recompute()
    w, d = 'Parameters.Width', 'Parameters.Depth'
    box = doc.addObject('PartDesign::Body', 'Enclosure'); box.Label = 'Enclosure - open top'
    base = sketch(doc, box, 'FloorSketch'); rectangle(base, w, d, 60, 40)
    pad(doc, box, base, 'FloorPad', 'Parameters.Floor')
    walls = sketch(doc, box, 'WallsSketch', 'Parameters.Floor')
    rectangle(walls, w, d, 60, 40)
    rectangle(walls, w+'-2*Parameters.Wall', d+'-2*Parameters.Wall', 56, 36)
    pad(doc, box, walls, 'WallsPad', 'Parameters.Height-Parameters.Floor')
    lid = doc.addObject('PartDesign::Body', 'Lid'); lid.Label = 'Lid - lip up for printing'
    lid.setExpression('Placement.Base.x', 'Parameters.Width+12 mm')
    plate = sketch(doc, lid, 'LidPlateSketch'); rectangle(plate, w, d, 60, 40)
    pad(doc, lid, plate, 'LidPlatePad', 'Parameters.LidThickness')
    lip = sketch(doc, lid, 'LipSketch', 'Parameters.LidThickness')
    ow = w+'-2*Parameters.Wall-2*Parameters.Clearance'
    od = d+'-2*Parameters.Wall-2*Parameters.Clearance'
    rectangle(lip, ow, od, 55.4, 35.4)
    rectangle(lip, ow+'-2*Parameters.LipWall', od+'-2*Parameters.LipWall', 52.2, 32.2)
    pad(doc, lid, lip, 'LipPad', 'Parameters.LipHeight')
    doc.recompute()
    return doc

def check(doc, values):
    doc.recompute()
    for obj in doc.Objects:
        assert 'Invalid' not in obj.State, (obj.Name, obj.State)
        if obj.TypeId == 'Sketcher::SketchObject':
            assert obj.FullyConstrained, (obj.Name, 'not fully constrained')
    box, lid = doc.Enclosure.Shape, doc.Lid.Shape
    for shape in (box, lid):
        assert shape.isValid() and len(shape.Solids) == 1
    w, d, h, t, f, lt, lh, lw, c = [values[k] for k in DEFAULTS]
    for actual, expected in zip((box.BoundBox.XLength, box.BoundBox.YLength, box.BoundBox.ZLength,
                                 lid.BoundBox.XLength, lid.BoundBox.YLength, lid.BoundBox.ZLength),
                                (w, d, h, w, d, lt+lh)):
        assert abs(actual-expected) < 1e-6, (actual, expected)
    expected_box = w*d*h-(w-2*t)*(d-2*t)*(h-f)
    a, b = w-2*t-2*c, d-2*t-2*c
    expected_lid = w*d*lt+(a*b-(a-2*lw)*(b-2*lw))*lh
    assert abs(box.Volume-expected_box) < 1e-5
    assert abs(lid.Volume-expected_lid) < 1e-5
    assembled = lid.copy()
    assembled.translate(App.Vector(-(w+12), 0, 0))
    assembled.rotate(App.Vector(), App.Vector(1,0,0), 180)
    assembled.translate(App.Vector(0,0,h+lt))
    assert box.common(assembled).Volume < 1e-6, 'lid collides with enclosure'
    mesh_results = {}
    for name, shape in [('enclosure', box), ('lid', lid)]:
        mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.15, Relative=False)
        assert mesh.isSolid(), name+' mesh is not closed'
        mesh_results[name] = {'volume_mm3': shape.Volume, 'triangles': mesh.CountFacets}
    return {'parameters_mm': values, 'checks': 'fully constrained sketches, valid solids, dimensions, analytic volumes, assembly collision, closed meshes', 'parts': mesh_results}

def run():
    doc = create()
    result = [check(doc, DEFAULTS.copy())]
    path = OUT / 'editable_enclosure.FCStd'
    doc.saveAs(str(path))
    App.closeDocument(doc.Name)
    doc = App.openDocument(str(path))
    result.append(check(doc, DEFAULTS.copy()))
    cases = [dict(Width=80, Depth=55, Height=35, Wall=2.4, Floor=2.4, Clearance=0.5),
             dict(Width=45, Depth=32, Height=18, Wall=1.6, Floor=1.6, LidThickness=1.6, LipHeight=3, LipWall=1.2, Clearance=0.2)]
    for changes in cases:
        values = dict(DEFAULTS, **changes)
        for key, value in values.items():
            doc.Parameters.set('B'+str(ROWS[key]), str(value)+' mm')
        result.append(check(doc, values))
    for key, value in DEFAULTS.items():
        doc.Parameters.set('B'+str(ROWS[key]), str(value)+' mm')
    check(doc, DEFAULTS.copy())
    doc.recompute()
    doc.save()
    (OUT/'validation.json').write_text(json.dumps({'freecad_version': App.Version(), 'tests': result}, indent=2))
    App.closeDocument(doc.Name)
    # Saving with the geometry-only API omits GUI visibility and camera data.
    # Use a fresh GUI-enabled process to persist a useful opening presentation.
    import subprocess
    import sys
    subprocess.run([sys.executable, str(OUT/'save_presentation.py'), str(path)], check=True)
    print('PASS: native document saved, reopened, resized twice, restored, and GUI presentation verified.')

if __name__ == '__main__':
    run()
