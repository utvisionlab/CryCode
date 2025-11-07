function fileNamesFeatureExtraction( motherDirectory, savingAddress)
	% mother directory is a directory address of Autistic or Normal voices
	%Each subject's voices are in a folder with its name
	%savingAddress is the address of a folder we want to save the result as a text 
	%files with the names of subjects
	% This function is written instead of GUI_feature_matrices function
	% mainDirectory is the address of voice files of one subject
	% fileName is the name of a text file we want to put features in it (the
	% name of person or any name for the features of one subject
	motherFolderInfo = dir(motherDirectory);
	sizeofMother = size(motherFolderInfo);

	% Getting the names of folders in mother directory
	if ( sizeofMother(1) >= 3)
	   fileNames = cell(sizeofMother(1)-2,1); %preallocating empty cell array 
		for i = 3 : sizeofMother(1)
		   fileNames{i-2}= motherFolderInfo(i).name; % These names should be used for txt files
		end
	end
	sizeofFileNames = size(fileNames);
	for j = 1 : sizeofFileNames
		mainDirectory = strcat(motherDirectory,fileNames(j));
		mainFolderInfo = dir(mainDirectory{1});
		sizeofMain = size(mainFolderInfo);

		% Getting the names of folders in main directory
		if ( sizeofMain(1) >= 3)
			 folderNames = cell(sizeofMain(1)-2,1); %preallocating empty cell array 
			 for i = 3 : sizeofMain(1)
				  folderNames{i-2}= mainFolderInfo(i).name;
			 end
		end
		sizeofFileNames = size(folderNames);
		featureMatrix = [];
		for i = 1 : sizeofFileNames(1)
			Z = ComputeFeatureSet1Matrix(mainDirectory, folderNames{i});
			featureMatrix = [featureMatrix; Z];
		end
		save_feature_matrix(savingAddress,fileNames{j},featureMatrix);
	end

end

