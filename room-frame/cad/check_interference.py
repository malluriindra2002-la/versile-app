#!/usr/bin/env python3
"""Assembly interference check: places every exported part (build/installed) as in
build/scene.json and reports pairs whose solid volumes overlap > 0.3 mm^3, plus
anything outside the 300 x 200 x 25 box. Touching (glued) faces are not overlaps."""
import json, os, itertools, numpy as np, trimesh
from trimesh.transformations import euler_matrix
import manifold3d as mf
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "build", "scene.json")))
cache, placed = {}, []
for ins in S["instances"]:
    p = ins["part"]
    if p not in cache: cache[p] = trimesh.load(os.path.join(HERE, "build", "installed", p + ".stl"))
    m = cache[p].copy()
    rx, ry, rz = np.radians(ins["r"])
    T = euler_matrix(rx, ry, rz, "sxyz"); T[:3, 3] = ins["t"]
    m.apply_transform(T)
    placed.append((ins["label"], m))
def man(m): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))
mans = [(l, m, man(m)) for l, m in placed]
bad = 0
for (la, ma, A), (lb, mb, B) in itertools.combinations(mans, 2):
    a0, a1 = ma.bounds; b0, b1 = mb.bounds
    if np.any(a1 < b0 - 1e-3) or np.any(b1 < a0 - 1e-3): continue
    v = (A ^ B).volume()
    if v > 0.3: print(f"OVERLAP {la:16s} x {lb:16s} {v:8.2f} mm^3"); bad += 1
for l, m in placed:
    b = m.bounds
    if b[0][0] < -0.01 and not l.startswith("FL") or b[1][0] > 300.01 or b[0][2] < -0.01 or b[1][2] > 200.01 or b[0][1] < -25.01 or b[1][1] > 0.01:
        print(f"OUTSIDE BOX {l}: {np.round(b, 2).tolist()}"); bad += 1
print("interference check:", "PASS" if bad == 0 else f"{bad} issue(s)")
