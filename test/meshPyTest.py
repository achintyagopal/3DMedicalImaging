from meshpy.triangle import MeshInfo, build
# from meshpy.tet import MeshInfo, build

mesh_info = MeshInfo()

mesh_info.set_points([(0,0,0), (0,1,0), (1,0,0)])

# mesh_info.set_facets([
#         [0, 1, 2, 3],
#         # [4, 5, 6, 7],
#         # [0, 4, 5, 1],
#         # [1, 5, 6, 2],
#         # [2, 6, 7, 3],
#         # [3, 7, 4, 0],
#         ])
# mesh = build(mesh_info)
# mesh.write_vtk("test.vtk")

# from __future__ import absolute_import
# from six.moves import range
# def main():
#     from math import pi, cos, sin
#     from meshpy.tet import MeshInfo, build
#     from meshpy.geometry import \
#             generate_surface_of_revolution, EXT_OPEN, \
#             GeometryBuilder

#     r = 3

#     points = 10
#     dphi = pi/points

#     def truncate(r):
#         if abs(r) < 1e-10:
#             return 0
#         else:
#             return r

#     rz = [(truncate(r*sin(i*dphi)), r*cos(i*dphi)) for i in range(points+1)]

#     geob = GeometryBuilder()
#     geob.add_geometry(*generate_surface_of_revolution(rz,
#             closure=EXT_OPEN, radial_subdiv=10))

#     mesh_info = MeshInfo()
#     geob.set(mesh_info)

#     mesh = build(mesh_info)
#     mesh.write_vtk("ball.vtk")

#     #mesh.write_neu(file("torus.neu", "w"),
#             #{1: ("pec", 0)})




# if __name__ == "__main__":
#     main()