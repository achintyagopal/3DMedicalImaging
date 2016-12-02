class ObjExporter():

    def compress(self, points, faces):

        compressed_pts = []
        compressed_faces = []
        for triangle in faces:
            compressed_face = []
            for index in triangle:
                pt = points[index]
                new_index = compressed_pts.find(pt)
                if new_index != -1:
                    compressed_pts.append(pt)
                    compressed_face.append(len(compressed_pts) - 1)
                else:
                    compressed_face.append(new_index)

            compressed_faces.append(compressed_face)

        return compressed_pts, compressed_faces

    def write_to_file(self, filename, points, faces, x_offset, y_offset):

        s = "g name\n"
        for pt in points:
            s += "v " + str(int(2 * (pt[0] - x_offset))) 
            s += " " + str(int(2 * (pt[1] - y_offset))) 
            s += " " + str(int(2 * pt[2])) + "\n"

        s += "usemtl anotherName\nusemap anotherName\n"
        for f in faces:
            s += "f"
            for v in f:
                s += " " + str(v + 1) + "/" + str(v + 1) + "/" + str(v + 1)
            s += "\n"

        f = open(filename,'w')
        f.write(s)