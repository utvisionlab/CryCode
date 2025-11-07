import os
import pickle
import numpy as np
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from SSI_method_functions import  read_subject_samples, remove_duplicate, balance_samples_matrix, clustering, \
    exclusive_instances, tree_to_code, remove_exclusive

def SSI_training(x, y, group):

    n_clusters = 1
    pickling = 1
    unpickling = 0

    x_save_normal= []  # all normal
    y_save_normal = []
    group_save_normal = []
    root_feature = []  # the feature in the root of the tree will be added to this list by the function tree_to_code

    yc = y

    for i in range(len(x)): #Saving all normal samples
        if y[i]=='0':
            x_save_normal.append(x[i])
            y_save_normal.append(0)
            group_save_normal.append(group[i])

    fp = 1 # file index for pickling
    fu = 0 # file index for unpickling

    while ((any(value >=10 for value in Counter(yc).values())) or (n_clusters == 1)):
        if unpickling==1:
            with open("x_remained"+str(fu)+".txt", "rb") as f_x_remained:   # Unpickling
                x = pickle.load(f_x_remained)
            with open("y_remained"+str(fu)+".txt", "rb") as f_y_remained:   # Unpickling
                y = pickle.load(f_y_remained)
            with open("group_remained"+str(fu)+".txt", "rb") as f_g_remained:   # Unpickling
                group = pickle.load(f_g_remained)
            f_x_remained.close()
            f_y_remained.close()
            f_g_remained.close()
        print("The subjects numbers which have at least one instance in training set for now:")
        print(set(group))
        x_balanced, y_balanced, g_balanced = balance_samples_matrix(x, y, group)

        min_max_scaler = MinMaxScaler()
        x_train_minmax = min_max_scaler.fit_transform(x_balanced)

        n_clusters = n_clusters + 1

        y_array, yc_array = clustering(x_train_minmax, y_balanced, n_clusters) # as it will be used in tree the scaled version is not used and PCA is also removed
        x, y, yc, group = remove_duplicate(x_balanced, y_array, yc_array, g_balanced)

        # Showing the instances in 1 and 0; 1 for ASD and 0 for TD
        pr_len = 30  # a limit for the lenght of each line when printing
        k = 0
        print("This is the instance view of each group: 1 for ASD and 0 for TD")
        while k <= len(y) - pr_len:
            print(y[k:k + pr_len])
            k = k + pr_len
        print(y[k:])
        # Showing the instances cluster numbers
        k = 0
        print("This is the instance view of each cluster: each number indicates the cluster number of each instance")
        while k <= len(yc) - pr_len:
            print(yc[k:k + pr_len])
            k = k + pr_len
        print(yc[k:])
        dtree = DecisionTreeClassifier()
        exclusive_clusters_indexes = exclusive_instances(y, yc, n_clusters) # If there is EI, returns their indexes and if not it returns an empty array

        number_of_features = len(np.array(x)[0,:])
        all_exclusive_ins = []
        all_exclusive_grp = []
        # If there is any exclusive cluster with atleast 10 instances a Tree will be trained and be shown in the output
        if exclusive_clusters_indexes:
            for i in range(len(exclusive_clusters_indexes)):
                index_list = exclusive_clusters_indexes[i]
                x_exclusive = [x[j] for j in index_list]
                grp_exclusive = [group[k] for k in index_list]
                y_exclusive = [y[j] for j in index_list]
                all_exclusive_ins.extend(x_exclusive) # making a list of all founded exclusive instances
                all_exclusive_grp.extend(grp_exclusive)
                if len(x_exclusive) >= 10:
                    x_train = x_exclusive + x_save_normal
                    y_train = y_exclusive + y_save_normal
                    dtree.fit(x_train, y_train)
                    print("A cluster of exclusive instances with at least 10 instances have been found.")
                    print("Exclusive instances of the cluster number {} are instances from subjects: {}.".format(yc[index_list[0]], set(grp_exclusive)))
                    tree_to_code(dtree, number_of_features, root_feature) # Printing the tree elements

            x_remained, y_remained, group_remained = remove_exclusive(all_exclusive_ins, x,y,group)
            # pickling
            with open("x_remained"+str(fp)+".txt", "wb") as f_x_remained:
                pickle.dump(x_remained, f_x_remained)
            with open("y_remained"+str(fp)+".txt", "wb") as f_y_remained:
                pickle.dump(y_remained, f_y_remained)
            with open("group_remained"+str(fp)+".txt", "wb") as f_g_remained:
                pickle.dump(group_remained, f_g_remained)
            f_x_remained.close()
            f_y_remained.close()
            f_g_remained.close()
            fp = fp + 1
            fu = fu + 1
            unpickling = 1
            n_clusters = 1
            # input("Press Enter to continue...")
    return root_feature


def SSI_testing(classifier, subject_files ):
    for i in range(len(subject_files)):
        subject_instances = read_subject_samples(subject_files[i])
        autistic_flag, first_classifier_portion, second_classifier_portion = classifier(subject_instances)
        if autistic_flag == 1:
            print("The subject {} is tagges as AUTISTIC".format(os.path.basename(os.path.normpath(subject_files[i])) ))
        else:
            print("The subject {} is tagges as NORMAL".format(os.path.basename(os.path.normpath(subject_files[i]))))

        print("The portion of autistic instances found by the first classifier is {}:".format(first_classifier_portion*100))
        print("The portion of autistic instances found by the second classifier is {}:".format(second_classifier_portion*100))


