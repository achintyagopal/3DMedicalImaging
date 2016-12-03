import sys
import os

import src.meshingTest


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


def main():

    args = get_args()

    if args.mode =="train":
        # load feature_file
        # get training feature vectors
        # train model
        # save model
        pass
    elif args.mode == "test":
        # load model_file
        # looad feature-file
        # get testing feature vectors
        # test model
        # calculate accuracy
        # print accuracy
        # save predictions file
        pass
    else:
        # get directory
        # for each patient (store patient id as label)
        # take min(4, sets) sets
        # for each set:
        # threshold
        # if not threshold: mrachingCubes
        # if feature: 
            # check algorithm, create accordingly
            # if set# == 1 or 2: train
            # if set# == 3 or 4: test
        pass



if __name__ == "__main__":
    main()
