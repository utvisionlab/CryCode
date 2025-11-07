import pandas
import numpy as np
from os import listdir
from os.path import isfile, join
from collections import Counter
from sklearn.cluster import AgglomerativeClustering, KMeans


def subject_names(autistic_directory, normal_directory):
    autistic_files = [f for f in listdir(autistic_directory) if isfile(join(autistic_directory, f))]
    normal_files = [f for f in listdir(normal_directory) if isfile(join(normal_directory, f))]
    return autistic_files, normal_files

def find_max_sample_number_matrix(group):
    # This is for the case we have samples in a matrix
    maximum_row = 0
    count = Counter(group)
    for i in set(group): # I used set to have [1,2,3,4,5....]
        row_count = count[i]
        if row_count > maximum_row:
            maximum_row = row_count
    return maximum_row


def balance_samples_matrix(samples_matrix, class_array, group_array):
    #samples_matrix is a 2d list
    # This is for the case we have samples in a matrix
    count = Counter(group_array)
    max_num_rows = find_max_sample_number_matrix(group_array)
    k = 0 # index for samples rows
    x_upsampled = []
    x_upsampled_idx = []
    y_upsampled = []
    g_upsampled = []
    # Upsampling to maximum number of samples
    for i in set(group_array):
        row_size = count[i]
        x = samples_matrix[k:k+row_size][:]
        y = class_array[k:k+row_size]
        g = group_array[k:k+row_size]
        k = k + row_size
        # Upsampling
        if row_size < max_num_rows:
            difference = max_num_rows - row_size
            if row_size < difference:  # in case the number of rows are not sufficient to select from
                devisor = difference // row_size
                remainder = difference % row_size
                x_upsampled.extend(x)
                y_upsampled.extend(y)
                g_upsampled.extend(g)
                for j in range(0,devisor):
                    x_upsampled.extend(x)
                    y_upsampled.extend(y)
                    g_upsampled.extend(g)
                x_upsampled.extend(x[0:remainder][:])
                y_upsampled.extend(y[0:remainder])
                g_upsampled.extend(g[0:remainder])
            else:
                x_upsampled.extend(x)
                y_upsampled.extend(y)
                g_upsampled.extend(g)
                x_upsampled.extend(x[0:difference][:])
                y_upsampled.extend(y[0:difference])
                g_upsampled.extend(g[0:difference])
        else:
            x_upsampled.extend(x)
            y_upsampled.extend(y)
            g_upsampled.extend(g)
    return x_upsampled, y_upsampled, g_upsampled

def read_subject_samples(subject_file_directory):
    # Open and read a text file of a subject's samples and put it in a matrix

    # X is an array of all samples and selected features
    X = []
    # y is an array of each sample classes
    y = []

    # samples is a list of subject's samples
    samples = []
    df = pandas.read_csv(subject_file_directory, header=None)
    excel_matrix = df.values
    data = excel_matrix[:, :]
    return data


def read_samples(autistic_directory, normal_directory):
    # Open and read all text files of subjects' samples and put it in a matrix

    # group is a list for indicating each subject
    group = []

    # X is an array of all samples and selected features
    X = []
    # y is an array of each sample classes
    y = []

    # autistic_samples is a list of autistic samples
    autistic_samples = []

    # normal_samples is a list of all normal samples
    normal_samples = []

    only_autistic_files, only_normal_files = subject_names(autistic_directory, normal_directory)

    i = 1  # A number for indicating the group of each sample (each group is for one subject)
    for file_name in only_autistic_files:
        df = pandas.read_csv(join(autistic_directory, file_name), header=None)
        excel_matrix = df.values
        all_data = excel_matrix[:, :]
        a = all_data
        autistic_samples.extend(a)
        group.extend(([i] * len(a)))
        i = i + 1

    for file_name in only_normal_files:
        df = pandas.read_csv(join(normal_directory, file_name), header=None)
        excel_matrix = df.values
        all_data = excel_matrix[:, :]
        a = all_data
        normal_samples.extend(a)
        group.extend(([i] * len(a)))
        i = i + 1

    X.extend(autistic_samples)
    X.extend(normal_samples)
    y.extend("1" * len(autistic_samples))
    y.extend("0" * len(normal_samples))

    return X, y, group


def remove_duplicate(x, y, yc, group):
    # This function is used as before clusttering upsampling was done and some samples are duplicate
    final_x = []
    final_y = []
    final_yc = []
    final_group = []
    for i in range(len(x)):
        if not (any((x[i] == row).all() for row in final_x)):
            final_x.append(x[i])
            final_y.append(y[i])
            final_yc.append(yc[i])
            final_group.append(group[i])
    return final_x, final_y, final_yc, final_group

def remove_exclusive(exclusive_x, x,y,group):
    final_x = []
    final_y = []
    final_group = []
    for i in range(len(x)):
        if not (any((x[i] == row).all() for row in exclusive_x)):
            final_x.append(x[i])
            final_y.append(y[i])
            final_group.append(group[i])
    return final_x, final_y, final_group

def list_append(x_list_new, x, x_scaled, y_list_new, y, group_list_new,
                group, index_list_new, i, scaled):
    if scaled is True:
        x_list_new.append(x_scaled[i])
    else:
        x_list_new.append(x[i])
    y_list_new.append(y[i])
    group_list_new.append(group[i])
    index_list_new.append(i)

    return x_list_new, y_list_new, group_list_new, index_list_new

def clustering(x_scaled, y, n_clusters):

    hc = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')

    # Save clusters for chart
    y_hc = hc.fit_predict(x_scaled) #This is for the time we want to use all features in clustering
    y = list(map(int, y))
    y_array = np.array(y)

    return y_array, y_hc

def find_index(array, item):
    index = []
    for i in range(len(array)):
        if array[i] == item:
            index.append(i)
    return index

def exclusive_instances(y_array, yc_array, n_clusters):
    exclusive_clusters_index = []
    y_count = Counter(y_array)
    Counter(yc_array)
    ASD_instance_number = y_count[1]
    yc_ASD = []
    yc_TD = []
    for i in range(len(y_array)):
        if y_array[i] == 1:
            yc_ASD.append(yc_array[i])
        else:
            if y_array[i] == 0:
                yc_TD.append(yc_array[i])
    ASD_clusters_count = Counter(yc_ASD)  # checking cluster array for ASD instances
    TD_clusters_count = Counter(yc_TD)  # checking cluster array for TD intstances

    for i in range(n_clusters):
        if ASD_clusters_count[i]!=0 and TD_clusters_count[i]==0:
            ASD_cluster_indexes = find_index(yc_array, i)
            exclusive_clusters_index.append(ASD_cluster_indexes)
    return exclusive_clusters_index

from sklearn.tree import _tree
def tree_to_code(tree, f_numbers, root):
    feature_names = []
    features = np.array(range(f_numbers))
    for j in features:
        feature_names.append(str(j))
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            root.append(int(name))
            print ("{}if feature {} <= {}:".format(indent, name, threshold))
            print("{} The instance is TD".format(indent))
            recurse(tree_.children_left[node], depth + 1)
            print ("{}if feature {} > {}".format(indent, name, threshold))
            print("{} The instance is ASD".format(indent))
            recurse(tree_.children_right[node], depth + 1)
            feature = int(name)

    recurse(0, 1)

def treshold_testing(instance, thrsh, feature_number):
    global normal_counter
    global aut_counter

    if instance[feature_number] <= thrsh:
        normal_counter = normal_counter + 1
    else:
        aut_counter = aut_counter + 1



def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def threshold_finding(subject_instances , subject_class, group, feature_index):
# This function looks for the best result on separating ASD and TD instances by thresholding on features
    if feature_index == 1: # All features are going to be searched for thresholds seperating the most ASD instances from TD instances
        feature_indices = range(len(np.array(subject_instances)[0,:]))
    else: # The indicated features are going to be searched for thresholds ...
        feature_indices = feature_index

    y_count = Counter(subject_class)
    ASD_instance_number = y_count['1']
    ASD_instances = subject_instances[:ASD_instance_number]
    TD_instances = subject_instances[ASD_instance_number:]
    count = Counter(group)
    feature_thr2 = []
    feature_thr1 = []
    feature_thr = []
    for tf in feature_indices:
        feature_thr1.append(np.max(np.array(TD_instances)[:,tf]))
    tf = 0
    for af in feature_indices:
        greater_flag = 0
        greater_ASD_value = []
        for l in range(len(ASD_instances)):
            if np.array(ASD_instances)[l,af]> feature_thr1[tf]:
                greater_ASD_value.append(np.array(ASD_instances)[l,af])
                greater_flag = 1
        if greater_flag == 1:
            feature_thr2.append(np.min(greater_ASD_value))
        else:
            feature_thr2.append(feature_thr1[tf])
        tf = tf + 1
    for f in range(len(feature_thr1)):  # Finding the mean value of the border
        feature_thr.append((feature_thr1[f]+feature_thr2[f])/2)

    ASD_subject_detected = len(feature_indices)*[0]
    ASD_instance_detected = len(feature_indices)*[0]
    for k in range(len(feature_indices)):
        j = 0
        for i in set(group[:ASD_instance_number]):
            row_size = count[i]
            ASD_subject_instances = ASD_instances[j:j+row_size][:]
            j = j + row_size
            subject_instance_detected = 0
            for instance in ASD_subject_instances:
                if instance[feature_indices[k]] > feature_thr[k]:
                    ASD_instance_detected[k] = ASD_instance_detected[k] + 1
                    subject_instance_detected = 1
            if subject_instance_detected == 1:
                ASD_subject_detected[k] = ASD_subject_detected[k] + 1
    max_subject = 0
    for k in range(len(feature_indices)):
        if ASD_subject_detected[k] >= max_subject:
            max_subject = ASD_subject_detected[k]
    max_subjects_indexes = [bf for bf, subject_detected in enumerate(ASD_subject_detected) if subject_detected == max_subject]
    max_instance = 0
    selected_features = []
    thresholds = []
    for index in max_subjects_indexes:
        if ASD_instance_detected[index] >= max_instance:
            max_instance = ASD_instance_detected[index]
            selected_features.append(feature_indices[index])
            thresholds.append(feature_thr[index])
    return selected_features, thresholds


def SSI_classifier(subject_instances):
    autistic_instances_counter1 = 0
    autistic_instances_counter2 = 0
    autistic = 0
    instances_number = len(subject_instances)
    for i in range(instances_number):
        if subject_instances[i][83] > 0.099: # VFTD of 7th coef. of MFCC (the first acheived classifier)
            autistic_instances_counter1 = autistic_instances_counter1 + 1
            autistic = 1
        if subject_instances[i][20] > 1.14: # VFTD of 6th coef of SONE (the second acheived cassifier)
            autistic_instances_counter2 = autistic_instances_counter2 + 1
            autistic = 1
    first_classifier_portion = autistic_instances_counter1/instances_number
    second_classifier_portion = autistic_instances_counter2/instances_number
    return autistic, first_classifier_portion, second_classifier_portion



