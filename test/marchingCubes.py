import sys
import os
from volumeCreator import *
import numpy as np

def marching_cubes(image):
    
    points = []
    faces = []
    height, rows, cols = image.shape[:]

    edges_coord = [(0.5, 1, 1), (1, 0.5, 1), (0.5, 0, 1), (0, 0.5, 1),
                    (0.5, 1, 0), (1, 0.5,0), (0.5,0,0), (0, 0.5, 0),
                    (0,1, 0.5), (1,1,0.5), (1,0,0.5), (0,0,0.5)]

    edge_calc = VolumeCreator()

    for z in range(height - 1):
        for y in range(rows - 1):
            if y % 20 == 0:
                print y, z
            for x in range(cols - 1):
                val = 0
                for a in range(2):
                    for b in range(2):
                        for c in range(2):
                            val <<= 1
                            if b == 0:
                                if image.item((z+a, y+b, x+c)) != 0:
                                    val += 1
                            else:
                                if image.item((z+a, y+b, x-c+1)) != 0:
                                    val += 1

                shapes = edge_calc.get_shapes(val)

                if len(shapes) == 0:
                    continue

                for shape in shapes:
                    edges = []
                    for edge in shape:
                        edges.append(edge + len(points))
                    faces.append(edges)

                for edge_coord in edges_coord:
                    c,b,a = edge_coord
                    points.append((z+a, y+b, x+c))



    s = "g name\n"
    for pt in points:
        s += "v " + str(int(2 * (pt[2] - cols / 2))) + " " + str(int(2 * (pt[1] - rows / 2))) + " " + str(int(2 * pt[0])) + "\n"
    s += "usemtl anotherName\nusemap anotherName\n"
    for f in faces:
        s += "f"
        for v in f:
            s += " " + str(v + 1) + "/" + str(v + 1) + "/" + str(v + 1)
        s += "\n"

    f = open('something.obj','w')
    f.write(s)
    # with open("something.obj", 'wb') as writer:
        # writer.write(s)
        # write.close()


    # mesh_info = MeshInfo()
    # mesh_info.set_points(points)
    # mesh_info.set_facets(faces)
    # mesh = build(mesh_info)
    # mesh.write_vtk("test.vtk")