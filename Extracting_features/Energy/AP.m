function AudioEnergy = AP(auData,totalSampleNum,samplingRate, sampleNum) 

%% File: AudioEnergyType.m
%%


%% Example: AudioPower_SeriesOfScalar = AP(A,size(A),B,4,64,[]);
%%          plot(AudioPower_SeriesOfScalar);
                


sampleNum = 882;
frameNum = floor(totalSampleNum/sampleNum);

% sumElement = sum(elementNum);
% AudioPower_SeriesOfScalar = zeros(frameNum, sumElement);
for i = 1:frameNum
   signal = auData(1+(i-1)*sampleNum:i*sampleNum);
   audioPowerData = signal.^2;
   meanValues(i,:) = mean(audioPowerData); % changed By Aida
end

AudioEnergy = meanValues;