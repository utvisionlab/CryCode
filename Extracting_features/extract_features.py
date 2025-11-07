# This code extract feature sets #1 and #2 from the data and combines them 
from phonation import phonationVowels
from glottal import glottal_features
from read_files import folder_names, file_names
import scipy.stats as st
import os
import pandas as pd
from os import getcwd, path
import numpy as np

def phonation_glottal(directory, saving_directory ):
    folders = folder_names(directory)
    for folder in folders:
        source_files = file_names(path.join(directory,folder))
        source_files.sort()
        nfiles = len(source_files)
        Features_phon = []
        Features_glot = []
        k = 1
        for file in source_files:
            voice_address = path.join(directory,folder, file)
            print("Processing audio " + str(k) + " from " + str(nfiles) + " " + folder)
            F0, DF0, DDF0, F0semi, Jitter, Shimmer, apq, ppq, logE, degreeU = phonationVowels(voice_address, False)
            print("Processing audio " + str(k) + " from " + str(nfiles) + " " + folder)
            varGCIt, avgNAQt, varNAQt, avgQOQt, varQOQt, avgH1H2t, varH1H2t, avgHRFt, varHRFt = glottal_features(voice_address,
                                                                                                                 False)
            k = k + 1
            Features_mean_phon = [DF0.mean(0), DDF0.mean(0), Jitter.mean(0), Shimmer.mean(0), apq.mean(0), ppq.mean(0)] #logE.mean(0) ommited
            Features_std_phon = [DF0.std(0), DDF0.std(0), Jitter.std(0), Shimmer.std(0), apq.std(0), ppq.std(0), logE.std(0)]
            Features_sk_phon = [st.skew(DF0), st.skew(DDF0), st.skew(Jitter), st.skew(Shimmer), st.skew(apq), st.skew(ppq),
                           st.skew(logE)] 
            Features_ku_phon = [st.kurtosis(DF0, fisher=False), st.kurtosis(DDF0, fisher=False),
                           st.kurtosis(Jitter, fisher=False),
                           st.kurtosis(Shimmer, fisher=False), st.kurtosis(apq, fisher=False),
                           st.kurtosis(ppq, fisher=False),
                           st.kurtosis(logE, fisher=False)] 
            Features_mean_glot = [varGCIt.mean(0), avgNAQt.mean(0), varNAQt.mean(0), avgQOQt.mean(0), varQOQt.mean(0),
                             avgH1H2t.mean(0), varH1H2t.mean(0), avgHRFt.mean(0), varHRFt.mean(0)] 
            Features_std_glot = [varGCIt.std(0), avgNAQt.std(0), varNAQt.std(0), avgQOQt.std(0), varQOQt.std(0), avgH1H2t.std(0),
                            varH1H2t.std(0), avgHRFt.std(0), varHRFt.std(0)] 
            Features_sk_glot = [st.skew(varGCIt), st.skew(avgNAQt), st.skew(varNAQt), st.skew(avgQOQt), st.skew(varQOQt),
                           st.skew(avgH1H2t), st.skew(varH1H2t), st.skew(avgHRFt), st.skew(varHRFt)] 
            Features_ku_glot = [st.kurtosis(varGCIt, fisher=False), st.kurtosis(avgNAQt, fisher=False),
                           st.kurtosis(varNAQt, fisher=False), st.kurtosis(avgQOQt, fisher=False),
                           st.kurtosis(varQOQt, fisher=False), st.kurtosis(avgH1H2t, fisher=False),
                           st.kurtosis(varH1H2t, fisher=False), st.kurtosis(avgHRFt, fisher=False),
                           st.kurtosis(varHRFt, fisher=False)] 
            feat_vec_phon = np.hstack(([degreeU], Features_mean_phon, Features_std_phon, Features_sk_phon, Features_ku_phon))
            feat_vec_glot = np.hstack(([Features_mean_glot, Features_std_glot, Features_sk_glot, Features_ku_glot]))
            Features_phon.append(feat_vec_phon)
            Features_glot.append(feat_vec_glot)
        Features_phon = np.asarray(Features_phon)
        Features_glot = np.asarray(Features_glot)
        features = np.concatenate((Features_phon, Features_glot), axis=1)
        np.savetxt(path.join(saving_directory, folder), features, delimiter=",")

#Extracting feature set #2 
directory1 = path.join('/data','Data_for_extracting_features','Train', 'Autistic')
saving_directory1 = path.join('/code', 'Extracting_features', 'Temp_extracted_features', 'temp_Autistic_train2')
phonation_glottal(directory1,saving_directory1)

directory2 = path.join('/data','Data_for_extracting_features','Train','Normal')
saving_directory2 = path.join('/code','Extracting_features','Temp_extracted_features','temp_Normal_train2')
phonation_glottal(directory2, saving_directory2)

#These lines are ommited to reduce the run time. Actually, the test phase does not use the second feature set at all.
# directory3 = path.join('/data','Data_for_extracting_features','Test','Male','Autistic')
# saving_directory3 = path.join('/code','Extracting_features','Temp_extracted_features','temp_maleAutistic_test2')
# phonation_glottal(directory3, saving_directory3)

# directory4 = path.join('/data','Data_for_extracting_features','Test','Male','Normal')
# saving_directory4 = path.join('/code','Extracting_features','Temp_extracted_features','temp_maleNormal_test2')
# phonation_glottal(directory4, saving_directory4)

# directory5 = path.join('/data','Data_for_extracting_features','Test','Female','Autistic')
# saving_directory5 = path.join('/code','Extracting_features','Temp_extracted_features','temp_femaleAutistic_test2')
# phonation_glottal(directory5, saving_directory5)

# directory6 = path.join('/data','Data_for_extracting_features','Test','Female','Normal')
# saving_directory6 = path.join('/code','Extracting_features','Temp_extracted_features','temp_femaleNormal_test2')
# phonation_glottal(directory6, saving_directory6)

# Combine feature sets #1 and #2
train_feature_set1_addresses = {1: "temp_Autistic_train1", 2: "temp_Normal_train1"}#, 3: "temp_maleAutistic_test1",
                          #4: "temp_maleNormal_test1", 5: "temp_femaleAutistic_test1", 6: "temp_femaleNormal_test1"}
test_feature_set1_addresses = {3: "temp_maleAutistic_test1", #{1: "temp_Autistic_train1", 2: "temp_Normal_train1",
                          4: "temp_maleNormal_test1", 5: "temp_femaleAutistic_test1", 6: "temp_femaleNormal_test1"}
# train_feature_set2_addresses = {1: "temp_Autistic_train2", 2: "temp_Normal_train2"}#, 3: "temp_maleAutistic_test2",
#                           #4: "temp_maleNormal_test2", 5: "temp_femaleAutistic_test2", 6: "temp_femaleNormal_test2"}
# test_feature_set2_addresses = {3: "temp_maleAutistic_test2", #{1: "temp_Autistic_train2", 2: "temp_Normal_train2",
#                           4: "temp_maleNormal_test2", 5: "temp_femaleAutistic_test2", 6: "temp_femaleNormal_test2"}
# features_final_address = {1: "Autistic_train", 2: "Normal_train", 3: "maleAutistic_test",
#                           4: "maleNormal_test", 5: "femaleAutistic_test", 6: "femaleNormal_test"}


for folder in train_feature_set1_addresses.values():
    feature_set1_address = path.join('/code','Extracting_features','Temp_extracted_features', folder)
    feature_set2_address = path.join('/code','Extracting_features','Temp_extracted_features', folder[:-1]+"2")
    for file_name in os.listdir(feature_set1_address):
        df_a = pd.read_csv(path.join(feature_set1_address, file_name), header=None)
        df_b = pd.read_csv(path.join(feature_set2_address, file_name[:-4]), header=None) 
        df_c = pd.concat([df_a, df_b], axis=1)
        df_c.to_csv(path.join('/code', 'Extracting_features', 'Temp_extracted_features', folder[5:-1], file_name), sep=',', header=None, index=False)
        df_c.to_csv(path.join('/results', file_name), sep=',', header=None, index=False)
        
for folder in test_feature_set1_addresses.values():
    feature_set1_address = path.join('/code','Extracting_features','Temp_extracted_features', folder)
    # feature_set2_address = path.join('/code','Extracting_features','Temp_extracted_features', folder[:-1]+"2")
    for file_name in os.listdir(feature_set1_address):
        df_a = pd.read_csv(path.join(feature_set1_address, file_name), header=None)
        df_a.transpose()
        df_a.to_csv(path.join('/code', 'Extracting_features', 'Temp_extracted_features', folder[5:-1], file_name), sep=',', header=None, index=False)
        df_a.to_csv(path.join('/results', file_name), sep=',', header=None, index=False)