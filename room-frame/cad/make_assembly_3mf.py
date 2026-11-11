#!/usr/bin/env python3
"""Complete assembly as 3MF: every piece a separate named, coloured object (CAD frame, mm:
X right, Z up, glass on the -Y side, back wall at y = 0)."""
import json, os, numpy as np, trimesh
from trimesh.transformations import euler_matrix
import build
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'build', 'scene.json')))
scene, cache = trimesh.Scene(), {}
for ins in S['instances']:
    p = ins['part']
    if p not in cache:
        cache[p] = trimesh.load(os.path.join(HERE, 'build', 'installed', p + '.stl'))   # already CAD frame
    m = cache[p].copy()
    T = euler_matrix(*np.radians(ins['r']), 'sxyz'); T[:3, 3] = ins['t']; m.apply_transform(T)
    hexc = build.MAT_RGB[S['parts'][p]].lstrip('#')
    m.visual.face_colors = [int(hexc[i:i + 2], 16) for i in (0, 2, 4)] + [255]
    scene.add_geometry(m, geom_name=f"{ins['label']}__{p}")
out = os.path.join(os.path.dirname(HERE), 'assembly', 'Store_Versile_Assembly.3mf')
scene.export(out)
r = trimesh.load(out)
print('3MF objects:', len(r.geometry), 'bounds', np.round(r.bounds, 1).tolist())
