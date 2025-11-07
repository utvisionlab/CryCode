function AudioPower_SeriesOfScalar = AP2(auData,totalSampleNum,samplingRate, sampleNum) 

%% File: AudioPowerType.m
%%
%% ------------- AudioPowerType--------------------

frameNum = floor(totalSampleNum/sampleNum);

% sumElement = sum(elementNum);
% AudioPower_SeriesOfScalar = zeros(frameNum, sumElement);
for i = 1:frameNum
   signal = auData(1+(i-1)*sampleNum:i*sampleNum);% chanded by Aida
   meanValues(i,:) = mean(signal); % changed By Aida
end

AudioPower_SeriesOfScalar = meanValues;