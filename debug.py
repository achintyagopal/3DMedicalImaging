import sys
import os
import argparse
import pickle

import cv2

from src.MeshInvariance import load, rotationally_invariant_identifier
from src.projectionVector import projection_based_vector
import src.Projection as Projection

from test.threshold import threshold
from test.marchingCubes import marching_cubes
from test.instance import Instance
from test.images import *

def threshold_imgs(directory):
    # get directory
    # directory = "test/SortedData/"
    # for each patient (store patient id as label)
    # complete_instances = [[], []]

    for patient_id in os.listdir(directory):
        
        patient_direc = os.path.join(directory, patient_id)
        if not os.path.isdir(patient_direc):
            continue

        print 'Patient:', patient_id    

        num_sets = 0
        for sets in os.listdir(patient_direc):

            set_direc = os.path.join(patient_direc, sets)
            if not os.path.isdir(set_direc):
                continue
            if num_sets >= 3:
                continue

            print "Set:", sets

            output_img, slice_thickness = threshold(set_direc)

            # for i in range(output_img.shape[0]):
                # show_image(output_img[i], 100)
            # with open('data/threshold/' + str(patient_id) + '_' + str(num_sets) + '.file', 'wb') as writer:
                # pickle.dump(output_img, writer)

            num_sets += 1
            # break
        # break


def check_threshold(directory):

    for filename in os.listdir(directory):
        file_direc = os.path.join(directory, filename)
        if not os.path.isfile(file_direc):
            continue

        print filename
        if filename.startswith('0522c0713') or filename.startswith('0522c0479'):
            continue

        with open(file_direc, 'rb') as reader:
            output_img = pickle.load(reader)
            for i in range(output_img.shape[0]):
                # print i
                show_image(output_img[i], 100)
            # break

def marching_cubes_data(directory):
    for patient_id in os.listdir(directory):
        
        patient_direc = os.path.join(directory, patient_id)
        if not os.path.isdir(patient_direc):
            continue

        print 'Patient:', patient_id    

        num_sets = 0
        for sets in os.listdir(patient_direc):

            set_direc = os.path.join(patient_direc, sets)
            if not os.path.isdir(set_direc):
                continue
            if num_sets >= 3:
                continue

            print "Set:", sets

            filename = str(patient_id) + '_' + str(num_sets)
            # if os.path.isfile('data/mesh/' + filename + '.obj'):
                # num_sets += 1
                # continue

            output_img, slice_thickness = threshold(set_direc)

            filename = str(patient_id) + '_' + str(num_sets)

            points, faces = marching_cubes(output_img, slice_thickness, 'data/mesh/' + filename + '.obj')

            with open('data/geometry/' + filename + '_points' + '.file', 'wb') as writer:
                pickle.dump(points, writer)
        
            with open('data/geometry/' + filename + '_faces' + '.file', 'wb') as writer:
                pickle.dump(faces, writer) 

            num_sets += 1


def create_projections(proj_data, mesh_directory, threshold_data):
    file_list = os.listdir(mesh_directory)
    for i in xrange(0, len(file_list), 2):
        f1 = file_list[i]
        f2 = file_list[i + 1]
        faces_direc = os.path.join(mesh_directory, f1)
        points_direc = os.path.join(mesh_directory, f2)
        # print "Faces", faces_direc
        # print "Points", points_direc
        patient_id = f1[:-11]
        with open(threshold_data + patient_id + '.file', 'rb') as reader:
            img_3d = pickle.load(reader)
        # print img_3d.shape

        with open(faces_direc, 'rb') as reader:
            faces = pickle.load(reader)
        # print "Load faces"

        with open(points_direc, 'rb') as reader:
            points = pickle.load(reader)
        # print "Load points"
        shape = img_3d.shape
        # shape = (96,512,512)
        # print patient_id

        img = Projection.project_mesh(points, faces, shape)
        smoothed_img = Projection.smooth_projection(img)
        filename = proj_data + patient_id + '_proj.file'
        print filename
        # show_image(smoothed_img)
        # break
        # save_image(smoothed_img, proj_data + patient_id + '_proj.jpg')
        with open(filename, 'wb') as writer:
            pickle.dump(smoothed_img, writer)


def create_profile(proj_data, mesh_directory, threshold_data):
    file_list = os.listdir(mesh_directory)
    for i in xrange(0, len(file_list), 2):
        f1 = file_list[i]
        f2 = file_list[i + 1]
        faces_direc = os.path.join(mesh_directory, f1)
        points_direc = os.path.join(mesh_directory, f2)
        # print "Faces", faces_direc
        # print "Points", points_direc
        patient_id = f1[:-11]
        with open(threshold_data + patient_id + '.file', 'rb') as reader:
            img_3d = pickle.load(reader)
        # print img_3d.shape

        with open(faces_direc, 'rb') as reader:
            faces = pickle.load(reader)
        # print "Load faces"

        with open(points_direc, 'rb') as reader:
            points = pickle.load(reader)
        # print "Load points"
        shape = img_3d.shape
        # shape = (96,512,512)
        # print patient_id

        img = Projection.project_mesh_profile(points, faces, shape)
        smoothed_img = Projection.smooth_projection(img)
        filename = proj_data + patient_id + '_proj.file'
        print filename
        # show_image(smoothed_img)
        # break
        # save_image(smoothed_img, proj_data + patient_id + '_proj.jpg')
        with open(filename, 'wb') as writer:
            pickle.dump(smoothed_img, writer)


def ellipses(proj_data):

    for filename in os.listdir(proj_data):
        
        if not os.path.join(proj_data, filename).endswith('.file'):
            continue

        with open(os.path.join(proj_data, filename), 'rb') as reader:
            smoothed_img = pickle.load(reader)

        ellipses = Projection.gradient_descent(smoothed_img, iteration=100, win=15)
        with open(os.path.join(proj_data, filename), 'rb') as reader:
            smoothed_img = pickle.load(reader)
        right, left, nose = ellipses
        cv2.ellipse(smoothed_img, right, color=(255,0,0), thickness = 5)
        cv2.ellipse(smoothed_img, left, color=(255,0,0), thickness = 5)
        cv2.ellipse(smoothed_img, nose, color=(255,0,0), thickness = 5)


        show_image(smoothed_img)
        # break

def view_profile(profile_data):
    for filename in os.listdir(profile_data):
        with open(os.path.join(profile_data, filename), 'rb') as reader:
            img = pickle.load(reader)
        show_image(img[img.shape[0]/6:])

def fft_test(mesh_directory):
    # file_list = os.listdir(mesh_directory)
    for filename in os.listdir(mesh_directory):
        # f1 = file_list[i]
        # f2 = file_list[i + 1]
        # faces_direc = os.path.join(mesh_directory, f1)
        # points_direc = os.path.join(mesh_directory, f2)

        # with open(faces_direc, 'rb') as reader:
        #     faces = pickle.load(reader)
        # # print "Load faces"

        # with open(points_direc, 'rb') as reader:
        #     points = pickle.load(reader)        
        if not filename.endswith('.obj'):
            continue

        mesh = load(os.path.join(mesh_directory, filename))
        # mesh.show()
        print filename
        # meshes = mesh.split()
        # i = 0
        # for mesh in meshes:
            # mesh.show()
            # filename = 'data/connected' + str(i) + '.obj'
            # with open(filename, 'wb') as writer:

            # i += 1
        # print mesh.euler_number
        # return
        vector = rotationally_invariant_identifier(mesh, 15)
        vector = (vector * 1e8/ vector[0] - 1e8) 
        print vector
        print ""

def main():
    directory = "test/SortedData/"
    threshold_data = "data/threshold/"
    mesh_data = "data/geometry/"
    proj_data = "data/projections/"
    profile_data = "data/profile/"
    meshes = 'data/mesh/'
    # threshold_imgs(directory)
    # check_threshold(threshold_data)
    # marching_cubes_data(directory)
    # create_projections(proj_data, mesh_data, threshold_data)
    # create_profile(profile_data, mesh_data, threshold_data)
    # view_profile(profile_data)
    ellipses(proj_data)
    # fft_test(meshes)

    # output_img, slice_thickness, pixel_spacing = threshold('test/SortedData/0522c0713/set4')
    # for i in range(output_img.shape[0]):
    #     # print i
    #     show_image(output_img[i], 100)


    # for root, dirs, _ in os.walk(directory):
    # for patient_id in 
    #     for patient_id in dirs:

    #         print 'Patient ', patient_id

    #         # take min(3, sets) sets
    #         for root_2, dirs_2, _ in os.walk(os.path.join(root, patient_id)):  # sorry about var names :/
    #           print "Root 2:", root_2
    #             num_sets = 0
    #             for set_name in dirs_2:

    #                 print 'Thesholding set ', num_sets
    #                 # if num_sets < 3:
    #                   # if not os.path.isdir(os.path.join(root_2, set_name)):
    #                       # continue
    #                   # print os.path.join(root_2, set_name)
    #                     # output_img, slice_thickness, pixel_spacing = threshold(os.path.join(root_2, set_name))
    #                     # if args.mode == "threshold":
    #                     # with open('data/' + str(patient_id) + '_' + str(num_sets) + '.file', 'wb') as writer:
    #                     #     pickle.dump(output_img, writer)

    #                 num_sets += 1

    #                 # filename = str(patient_id) + '_' + str(num_sets) + '.obj'
    #                 # if args.mode != 'threshold':
    #                 #     print 'MarchingCubes set ', num_sets
    #                 #     points, faces = marching_cubes(output_img, pixel_spacing, slice_thickness, filename)
                    
    #                 # if args.mode == 'feature':
    #                 #     print 'Featuring set ', num_sets
    #                 #     feature_vector = create_instance(filename, points, faces, output_img.shape, args.feature_algorithm)
    #                 #     instance = Instance(feature_vector, patient_id)
    #                 #     # check algorithm, create accordingly
    #                 #     if num_sets in (1,2):
    #                 #         complete_instances[0].append(instance)
    #                 #     else:
    #                 #         complete_instances[1].append(instance)

if __name__ == "__main__":
    main()
