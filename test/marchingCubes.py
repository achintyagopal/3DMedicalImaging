import sys
import os
import numpy as np
from meshCreator import MeshCreator
from objExporter import ObjExporter
import pickle

def marching_cubes(image, spacing, thickness, filename):
    
    points = []
    faces = []
    height, rows, cols = image.shape[:]

    edges_coord = [(0.5, 1, 1), (1, 0.5, 1), (0.5, 0, 1), (0, 0.5, 1),
                    (0.5, 1, 0), (1, 0.5,0), (0.5,0,0), (0, 0.5, 0),
                    (0,1, 0.5), (1,1,0.5), (1,0,0.5), (0,0,0.5)]

    mesh_creator = MeshCreator()

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
                                    
                shapes = mesh_creator.get_shapes(val)

                if len(shapes) == 0:
                    continue

                for shape in shapes:
                    edges = []
                    for edge in shape:
                        edges.append(edge + len(points))
                    faces.append(edges)

                for edge_coord in edges_coord:
                    a, b, c = edge_coord
                    points.append((x+a, y+b, z+c))

    # with open('points.file', 'wb') as writer:
        # pickle.dump(points, writer)

    # with open('faces.file', 'wb') as writer:
        # pickle.dump(faces, writer)

    exporter = ObjExporter()
    exporter.write_to_file(filename, points, faces, cols/2, rows/2, int(thickness/ spacing[0]))
    return points, faces