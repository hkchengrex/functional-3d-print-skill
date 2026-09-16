"""Software z-buffer preview: works without an offscreen OpenGL context."""
import math
import numpy as np
from PIL import Image


def render(items, path, width=1400, height=1000):
    triangles = []
    def project(v):
        return ((v.x+v.y)/math.sqrt(2), (v.x-v.y)/math.sqrt(6)-v.z*math.sqrt(2/3), (v.x-v.y+v.z)/math.sqrt(3))
    for shape, color in items:
        verts, faces = shape.tessellate(.08)
        for a,b,c in faces:
            normal = (verts[b]-verts[a]).cross(verts[c]-verts[a])
            if normal.Length:
                normal.normalize()
            shade = .65+.35*abs(normal.z*.8-normal.y*.5+normal.x*.3)
            triangles.append(([project(verts[i]) for i in (a,b,c)], [min(255,int(v*255*shade)) for v in color]))
    assert triangles, 'Nothing to render'
    points = np.array([p for ps,_ in triangles for p in ps])
    low = points[:,:2].min(axis=0); high = points[:,:2].max(axis=0)
    scale = min((width-80)/max(high[0]-low[0],1e-6), (height-80)/max(high[1]-low[1],1e-6))
    offset = (np.array([width,height])-(high-low)*scale)/2
    pixels = np.full((height,width,3), 244, dtype=np.uint8)
    depth = np.full((height,width), -np.inf)
    for ps,color in triangles:
        pp = (np.array(ps)[:,:2]-low)*scale+offset
        (ax,ay),(bx,by),(cx,cy) = pp
        den = (by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-8: continue
        x0,y0 = np.maximum(0,pp.min(axis=0).astype(int))
        x1,y1 = np.minimum([width,height],pp.max(axis=0).astype(int)+2)
        yy,xx = np.mgrid[y0:y1,x0:x1]
        aa = ((by-cy)*(xx+.5-cx)+(cx-bx)*(yy+.5-cy))/den
        bb = ((cy-ay)*(xx+.5-cx)+(ax-cx)*(yy+.5-cy))/den
        cc = 1-aa-bb
        zz = aa*ps[0][2]+bb*ps[1][2]+cc*ps[2][2]
        region = depth[y0:y1,x0:x1]
        mask = (aa>=-1e-7)&(bb>=-1e-7)&(cc>=-1e-7)&(zz>region)
        region[mask]=zz[mask]
        pixels[y0:y1,x0:x1][mask]=color
    Image.fromarray(pixels).save(path)
