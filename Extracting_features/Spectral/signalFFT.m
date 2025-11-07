function fastTrans = fftransform(auData,totalSampleNum,sampleNum, coefNum) 

%% File: signalFFT.m
%%
%% ------------- FFT of segments of signal--------------------

frameNum = floor(totalSampleNum/sampleNum);

% sumElement = sum(elementNum);
% AudioPower_SeriesOfScalar = zeros(frameNum, sumElement);
for i = 1:frameNum
   signal = auData(1+(i-1)*sampleNum:i*sampleNum);% chanded by Aida
   fftransforms(i,:) = abs(fft(signal,coefNum)); % changed By Aida
end

fastTrans = fftransforms;