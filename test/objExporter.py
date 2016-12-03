class ObjExporter():

    def write_to_file(self, filename, points, faces, x_offset, y_offset, z_scale = 1):

        s = "g name\n"
        for pt in points:
            s += "v " + str(int(2 * (pt[0] - x_offset))) 
            s += " " + str(int(2 * (pt[1] - y_offset))) 
            s += " " + str(int(pt[2] * z_scale)) + "\n"

        s += "usemtl anotherName\nusemap anotherName\n"
        for f in faces:
            s += "f"
            for v in f:
                s += " " + str(v + 1) + "/" + str(v + 1) + "/" + str(v + 1)
            s += "\n"

        f = open(filename,'w')
        f.write(s)