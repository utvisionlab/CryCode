function plotfft(fftSignal,fs)
% By Aida
close all;
%N =length(signal);
%Define signal
t = 0:1/fs:1-1/fs;
%apply fftshift to put it in the form we are used to (see documentation)
fftSignal2 = fftshift(fftSignal);
%xdft = xdft(1:length(s)/2+1);
%Next, calculate the frequency axis, which is defined by the sampling rate
%f = (fs/2)*linspace(-1,1,fs);
f = linspace(0,pi,length(fftSignal));
%Since the signal is complex, we need to plot the magnitude to get it to
%look right, so we use abs (absolute value)
figure;
plot(f, abs(fftSignal2));
title('magnitude FFT of sine');
xlabel('Frequency (Hz)');
ylabel('magnitude');