 function [ACcoefs] = AC(signal) 
%
% Estimate the auto-correlation of a signal
% and keeps the first 12 coefficients from the symmetrized correlation
%
% Example: 
% [A,B,C] = wavread('BaCl.mf.C4B4_3.wav');
% [ACcoefs] = AC(A);

%[ar,e,k] = lpcauto(signal);


c = xcorr(signal);
[A1 A2] = size(signal);

ACcoefs = c(A1:A1+12);
if size(ACcoefs,2)==1
    ACcoefs = ACcoefs';
end