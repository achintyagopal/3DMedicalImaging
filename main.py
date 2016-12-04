import sys
import os

import src.meshingTest

from test.threshold import threshold
from test.marchingCubes import marchingCubes


def get_args():

    parser = argparse.ArgumentParser(description="This is the main file for running 3DMedicalImaging.")

    parser.add_argument("--folder", type=str,
        help="The folder that contains patient_ids/set#/<>.dcm .")

    parser.add_argument("--mode", type=str, required=True, choices=["threshold", "meshing", "feature", "train", "test"],
                        help="Operating mode: feature extraction, train or test.")

    parser.add_argument("--feature-file", type=str,
                        help="The name of the file containing feature converter/ instance creator")

    parser.add_argument("--model-file", type=str,
                        help="The name of the model file to create/load.")

    parser.add_argument("--predictions-file", type=str, help="The predictions file to create.")

    parser.add_argument("--feature-algorithm", type=str, help="The name of the algorithm for training.")

    parser.add_argument("--training-algorithm", type=str, help="The name of the algorithm for training.")

    args = parser.parse_args()
    check_args(args)

    return args

def check_args(args):
    if args.mode == "threshold":
        if args.folder is None:
            raise Exception("--folder (folder with data) should be specified in mode \"threshold\"")
    elif args.mode == "meshing":
        if args.folder is None:
            raise Exception("--folder (folder with data) should be specified in mode \"meshing\"")
    elif args.mode == "feature":
        if args.folder is None:
            raise Exception("--folder (folder with data) should be specified in mode \"feature\"")
        if args.feature_algorithm is None:
            raise Exception("--feature-algorithm (feature extraction algorithm) should be specified in mode \"feature\"")
        if args.feature_file is None:
            raise Exception("--feature-file (where to save feature vectors) should be specified in mode \"feature\"")
    elif args.mode == "train":
        if args.feature_file is None:
            raise Exception("--feature-file (where feature vectors are saved) should be specified in mode \"train\"")
        if not os.path.exists(args.feature_file):
            raise Exception("feature file specified by --feature-file does not exist.")
        if args.training_algorithm is None:
            raise Exception("--training-algorithm must be specificied in mode \"train\"")
        if args.model_file is None:
            raise Exception("--model-file should be specified in mode \"train\"")
    else:
        if args.feature_file is None:
            raise Exception("--feature-file (where feature vectors are saved) should be specified in mode \"train\"")
        if not os.path.exists(args.feature_file):
            raise Exception("feature file specified by --feature-file does not exist.")
        if args.predictions_file is None:
            raise Exception("--prediction-file should be specified in mode \"test\"")
        if args.model_file is None:
            raise Exception("--model-file should be specified in mode \"test\"")
        if not os.path.exists(args.model_file):
            raise Exception("model file specified by --model-file does not exist.")

def train(training_instances, algorithm):

    return None

def predict(predictor, testing_instances, filename):
    
    # predict all testing instances
    predictions = predictor.test(testing_instances)

    # create predictions file
    try:
        total_correct = 0
        total = 0
        with open(predictions_file, 'w') as writer:
            for i in range(len(predictions)):
                prediction = predctions[i]
                correct_label = testing_instances[i].get_label()
                writer.write(str(prediction))
                writer.write(' ')
                writer.write(str(correct_label))
                writer.write('\n')
        
                # compute accuracy
                if correct_label == prediction:
                    total_correct += 1
                total += 1

    # print accuracy
    print total_correct/float(total)

    except IOError:
        raise Exception("Exception while opening/writing file for writing predicted labels: " + predictions_file)



def main():

    args = get_args()

    if args.mode =="train":
        # load feature_file
        try:
            with open(args.feature_file, 'rb') as reader:
                instances = pickle.load(reader)
        except IOError:
            raise Exception("Exception while reading the model file.")
        except pickle.PickleError:
            raise Exception("Exception while loading pickle.")
                
        # get training feature vectors
        training_instances = instances[0] # or instances["train"]

        # train model
        predictor = train(training_instances, args.training_algorithm)

        # save the model
        try:
            with open(args.model_file, 'wb') as writer:
                pickle.dump(predictor, writer)
        except IOError:
            raise Exception("Exception while writing to the model file.")        
        except pickle.PickleError:
            raise Exception("Exception while dumping pickle.")

    elif args.mode == "test":
        # load model_file
        try:
            with open(args.model_file, 'rb') as writer:
                predictor = pickle.load(predictor)
        except IOError:
            raise Exception("Exception while writing to the model file.")        
        except pickle.PickleError:
            raise Exception("Exception while dumping pickle.")

        # load feature_file
        try:
            with open(args.feature_file, 'rb') as reader:
                instances = pickle.load(reader)
        except IOError:
            raise Exception("Exception while reading the model file.")
        except pickle.PickleError:
            raise Exception("Exception while loading pickle.")

        # get testing feature vectors
        testing_instances = instances[1] # or instances["test"]

        predict(predictor, testing_instances, args.predictions_file)

    else:
        # get directory
        directory = args.folder
        # for each patient (store patient id as label)
        for root, dirs, files in os.walk(directory):
            for patient_id in dirs:

                print 'Patient ', patient_id
                # take min(4, sets) sets
                for root_2, dirs_2, files_2 in os.walk(patient_id):  # should the arg be directory + patient_id ? sorry about var names :/
                    num_sets = 0
                    for set_name in dirs_2:

                        print 'Thesholding set ', num_sets
                        if num_sets < 4:
                            output_img, slice_thickness, pixel_spacing = threshold(set_name) # again, should this be directory + patient_id + set_name ?
                        num_sets += 1

                        # if not threshold: marchingCubes
                        if args.mode != 'threshold':
                            print 'MarchingCubes set ', num_sets
                            marching_cubes(output_img, pixel_spacing, slice_thickness, str(patient_id) + '_' + str(num_sets) + '.obj')
                        
                        # if feature: 
                        if args.mode == 'feature':
                            print 'Featuring set ', num_sets
                            # TODO check algorithm, create accordingly
                            # if set# == 1 or 2: train
                            # if set# == 3 or 4: test



if __name__ == "__main__":
    main()
