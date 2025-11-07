% Sinartisi save_feature_matrix: Kalei tin sinartisi feature_matrix gia
% na swsei ton pinaka features enos arxeiou ixou ston disko se ena arxeio
% *.sfm.

function [] = save_feature_matrix(savingAddress,filename,featureMatrix)

sheet = 1;
n=1;
fileAddress = strcat(savingAddress,filename,'.txt');
fileID = fopen(fileAddress,'w');
fprintf('Extracting features for %s \n', fileAddress);
for i = 1 : size(featureMatrix,1) % for the number of name of files
    for j = 1 : size(featureMatrix,2)
        if j == size(featureMatrix,2)
            fprintf(fileID,'%8.16f ',featureMatrix(i,j));
        else
            fprintf(fileID,'%8.16f , ',featureMatrix(i,j));
        end
    end
    fprintf(fileID,' \n');
end
 fclose(fileID);
end
