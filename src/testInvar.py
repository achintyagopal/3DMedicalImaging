import trimesh
import numpy as np 
import MeshInvariance

filename = "something_part2.obj"

mesh = MeshInvariance.load(filename)

print mesh.is_watertight

v1 = MeshInvariance.rotationally_invariant_identifier(mesh)

# mesh.show()

filename = "something_part3.obj"

mesh = MeshInvariance.load(filename)

print mesh.is_watertight

v2 = MeshInvariance.rotationally_invariant_identifier(mesh)

print v1
print v2
print np.linalg.norm(v1 - v2)
