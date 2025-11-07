from variables_definition import *
from os import listdir, path
from os.path import isfile, join
from SSI_method import SSI_training,  SSI_testing
from SSI_method_functions import read_samples, threshold_finding, SSI_classifier

x, y, group = read_samples(autistic_directory, normal_directory)
#input_command1 = input("Please type \'S\' for SSI method. \n")
#input_command2 = input("Please type \'t\' for Training procedure or \'te\' for test #procedure: \n")
#if (input_command1 == 'S' or 's') and input_command2 == 't':
print("Training using SSI method")
root_feature = SSI_training(x, y, group)
print("Using SSI method on this data, we found that there is(are) case(s)in which a single feature can seperate several instances in target class from the rest by a simple threshold.\n\n")
features = []
thresholds = []
for i in range(len(root_feature)):
    if root_feature[i] <= 100 and root_feature[i] >= 78:
        print("\t One feature seen on the root of tree classifier is VFTD of an MFCC coefficient.")
    if root_feature[i] <= 22 and root_feature[i] >= 7:
        print("\t One feature seen on the root of tree classifier is VFTD of a SONE coefficient.")
print("Checking features to see which one can seperate more ASD subjets and instances than others from the rest in the training set:")
feature_list = range(root_feature[i]-15 , root_feature[i]+15) # a range of features probably similar to the one found by Exclusive Instances
selected_feature, threshold = threshold_finding(x , y, group, 1) # Setting feature_list to 1 means searching all the features not those in a specific range
features.append(selected_feature)
thresholds.append(threshold)
print("The best feature(s) among others is(are) {} with the threshold(s) of {},         respectively".format(selected_feature, threshold))
print("The classifier(s) achieved are feture(s) {} with the thersholds of {}".format(features,thresholds))              

#else:
print("****************************************************************************")
print("****************************************************************************")
print("****************************************************************************")
print("****************************************************************************")
   # if (input_command1 == 'S' or 's') and input_command2 == 'te':
print("Testing the test data set using SSI method")
sources = [male_autistic_test_directory, female_autistic_test_directory, male_normal_test_directory,  female_normal_test_directory]
subject_files = []
for j in range(len(sources)):
    source_files = [path.join(sources[j], f) for f in listdir(sources[j]) if isfile(join(sources[j], f))]
    subject_files.extend(source_files)
SSI_testing(SSI_classifier, subject_files)

