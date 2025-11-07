CryCode 
------
Cry sounds are collected from children with Autism Spectrum Disorder (ASD) and Typically Developing (TD) children with the same age range. There is a code of our proposed method for finding special cry instances and features from children with ASD that can help in screening autism at early ages.

#### Dataset
The cry sounds dataset includes original cry sounds and the cleaned version of them that is available in "data/Row_and_cleaned_cry_data" folder. 
The data extracted from the cleaned version of the sounds, using our local platform, is available in "data/Extracted_features" folder. The mentioned data is available as text files including features extracted using matlab R2015b (32 bit) and python 3.7.2 (64 bit) installed on windows operating system.

#### Run steps
At first, the proposed method (SSI classifier) applies on the instances saved in "data/Extracted_features" folder which are extracted from the cleaned sounds using our local system and are uploaded to be used only in classification process. This procedure does not take a long time and it provides the exact process explained in the "method" section of the paper. Indeed, it shows what led us to find the two mentioned features and the thresholds.

After that, the whole process including extracting the features from cleaned sounds as well as the training and testing phases runs. As, running of this part of the code lasts about one hour and one may want to see only the process of training and testing the classifier, this whole process is placed after the first mentioned step.
To extract features from the cleaned data, which is reorginized and available in "data/Data_for_extracting_features" folder, there are codes in Matlab and python in "code/Extracting_features". It should be mentioned that the extraction codes for the first and second feature sets are from [1] and [2,3], respectively, with some modifications explained in the paper. To reduce the time of running the codes of the whole process, the second feature set, which needs much more time than the first set, is not computed for the test data set as the features that are testd in testing phase are from the first set. 

Note: In our previous original extracted features (located in /data/Extracted_features) in the second feature set, the fundamental frequency is computed using praat but in the current platform, which is on Ubuntu, RAPT algorithm is used due to the limitations.
In case you may need more information about the code for second feature set please see https://github.com/jcvasquezc/DisVoice.

To extract features from the cleaned data, which is reorginized and available in "data/Data_for_extracting_features" folder, there are codes in Matlab and python in "code/Extracting_features". It should be mentioned that the extraction codes for the first and second feature sets are from [1] and [2,3], respectively, with some modifications explained in the paper.

To extract features, the two steps below appears:
1. Run "FeatureSet1Extraction.m" in MATLAB to extract feature set 1.

2. Run "extract_features.py" in order to extract feature set 2 and also combine two feature sets.

Note: The DisVoice package code (the second feature set) is used in "extract_features.py".
	
Fter running the whole code the features are extracted and placed in the "/results" foldre in text files with the names of each subject. Also, they are temporary available during the run time in order to be used by the classifier. 

Note: It should be mentioned that few features are different in values relative to our original data set. This may happen due to running the code on a differnt platform and/or hardware and may cause to have differnt clusters during the training phase.
	
	
#### References for feature extraction phase
[1] Motlagh SHRE, Moradi H, Pouretemad H, editors. Using general sound descriptors for early autism detection: 2013 9th Asian Control Conference (ASCC) 
Control; 2013; Istanbul, Turkey: IEEE. 2013. Doi: 10.1109/ASCC.2013.6606386.

[2] Belalcázar-Bolaños E.A., Orozco-Arroyave J.R., Vargas-Bonilla J.F., Haderlein T., Nöth E. Glottal Flow Patterns Analyses for Parkinson’s Disease 
Detection: Acoustic and Nonlinear Approaches. In: Sojka P., Horák A., Kopeček I., Pala K., editors. Text, Speech, and Dialogue: Proceedings of the 19th 
International Conference on Text, Speech, and Dialogue; 2016 Sep 12-16; Brno , Czech Republic. Cham: Springer; 2016. Doi : 10.1007/978-3-319-45510-5_46.

[3] Arias-Vergara T, Vásquez-Correa JC, Orozco-Arroyave JR. Parkinson’s disease and aging: analysis of their effect in phonation and articulation of speech. Cognitive Computation. 2017 Dec 1;9(6):731-48.

