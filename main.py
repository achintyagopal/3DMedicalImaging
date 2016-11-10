import sys
import os


def parse_arguments():
    pass


def get_data(args):
    pass


def threshold(nib_file):
    pass


def label(threshold_data):
    pass


def get_corners_per_voxel(labelled_data):
    pass


def create_mesh(corners_data):
    pass


def save_mesh(mesh):
    pass


def main():

    args = parse_arguments()
    nib_file = get_data(args)
    threshold_data = threshold(nib_file)
    labelled_data = label(threshold_data)
    corners_data = get_corners_per_voxel(labelled_data)
    mesh = create_mesh(corners_data)
    save_mesh(mesh)


if __name__ == "__main__":
    main()
