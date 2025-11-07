function [f0,fc] = f0est(sig,fs,framesize,npartials,minlevel,debug);
%F0EST  Estimate fundamental frequency F0 from spectral peaks
%
% [f0,fc] = f0est(sig,fs,framesize,npartials,minlevel);
%
% Computes fundamental frequency estimate f0 (Hz) and spectral cut-off
% frequency fc (Hz) from spectral peaks for npartials partials in
% signal sig.  The frame size used in the fft is specified in
% framesize which is rounded up to the next odd number if necessary.
% The sampling rate is passed in fs (default = 1).  Peaks are rejected
% minlevel dB below the highest peak.  fc is returned as the frequency
% (Hz) of the highest partial.  A Blackman window is used.

len = length(sig);

if (nargin<2),
 fs = 1;
end;

if (nargin<3),
 framesize = 512;
end;

if (nargin<5),
 minlevel = -60; % dB
end;

if (nargin<6),
 debug = 0;
end;

if (len < framesize),
 disp(sprintf('*** f0est: signal too short  for fft (%d samples)',len));
 framesize = len;
end;

if mod(framesize,2)==0, 
 framesize = framesize - 1;
 disp(sprintf('f0est: framesize -> next odd number = %d',framesize));
end;

minzpadfactor = 5;  % min zero-padding factor (for accurate freqs)
%nfft = pwr2(framesize*minzpadfactor);      %hamid changes
nfft = power(framesize*minzpadfactor,2);
nspec = nfft/2 + 1;
[fkHz fxlab fylab] = freqlabs(nspec,fs);
nzpad = nfft - framesize;
padding = zeros(1,nzpad);
zpadfactor = nfft/framesize;
locscl = (fs/2) / nfft;		% Converts bin to freq

if (nargin<4),
 npartials = framesize/2;	% i.e., no upper limit
end;

window = blackman(framesize)';

% Parameters established.
% Compute FFT.

minpeakwidth = zpadfactor*5; % 5 for generalized Blackman family
maxpeakwidth = minpeakwidth*2; % reject too much modulation/interf.

forigin = 1;
frame = [window .* sig(forigin:forigin+framesize-1), padding];
if debug>1, plot(frame); title(sprintf('Signal Frame')); end;
spec = fft(frame);  
specdb = db(spec(1:nspec));
minval = max(specdb) + minlevel;
if debug, plot(fkHz,specdb); 
  title('Signal Frame Spectrum'); 
  xlabel(fxlab); ylabel(fylab); 
end;

[peakamps peaklocs peakwidths] = ...
  findpeaks(specdb,npartials,minpeakwidth,maxpeakwidth,minval,debug);

[peaklocs,sorter] = sort(peaklocs);
amps = zeros(size(peakamps));
widths = zeros(size(peakamps));
npeaks = length(peaklocs);
for col=1:npeaks, 
	amps(:,col) = peakamps(:,sorter(col)); 
	widths(:,col) = peakwidths(:,sorter(col)); 
end;

freqs = (peaklocs - ones(size(peaklocs))) * fs / nfft;
if npeaks>1,
  fspacings = diff(freqs);
  medianfspacing = median(fspacings);
  avgfspacing = mean(fspacings);
else
  fspacings = freqs(1);
  medianfspacing = freqs(1);
  avgfspacing = freqs(1);
end;
  
f0a = medianfspacing;
harmonic_numbers = round(freqs/f0a);

subharms = find(harmonic_numbers < 0.75);
msh = max(subharms);
if msh > 0 % delete subharmonics, dc peak, etc.
  disp(sprintf(...
    '*** Tossing out the following %d peaks below F0',msh));
  format bank;
  disp('	freqs	amps	widths:'); 
  [freqs(1:msh)', amps(1:msh)', widths(1:msh)']
  disp('*** PAUSING (RETURN to continue) ***'); 
  pause;
  freqs = freqs(msh+1:npeaks);
  amps = amps(msh+1:npeaks);
  widths = widths(msh+1:npeaks);
  harmonic_numbers = harmonic_numbers(msh+1:npeaks);
  npeaks = npeaks - msh;
end

if debug,
	format bank;

	disp('	freqs	amps	widths:'); [freqs', amps', widths']
	disp('partial frequency intervals:'); fspacings

	bar(freqs(1:end-1),fspacings-f0a);
	title('Partial Frequency Spacings minus fundamental');
	ylabel('Frequency Spacing (Hz)');
	xlabel('Frequency (Hz)');
        disp('PAUSING - RETURN to continue'); pause;

	disp(sprintf('Median partial frequency interval = %f',medianfspacing));
	disp(sprintf('Average partial frequency interval = %f',avgfspacing));
	disp(sprintf('Fundamental frequency estimate = %f',f0a));
	disp(sprintf('Harmonics versus peaks:')); 
		[f0a*harmonic_numbers',freqs']
	disp(sprintf('Relative deviation:'));
	disp(sprintf('Relative deviation (%%):'));
	f0a_error = 100*(freqs - f0a*harmonic_numbers)./freqs

	bar(freqs,f0a_error*1200);
	title('Relative Partial Frequency Deviations (measured - harmonic)');
	ylabel('Cents');
	xlabel('Frequency');
        disp('PAUSING - RETURN to continue'); pause;

	disp(sprintf('Saved output format:'));
	nfreqs = length(freqs);
        [sprintf('partial_freqs = {%f',freqs(1)), ...
		sprintf(', %f',freqs(2:nfreqs)),sprintf('};')]
        [sprintf('partial_numbers = {%d',harmonic_numbers(1)),...
		sprintf(', %d',harmonic_numbers(2:nfreqs)),sprintf('};')]
end;

%
% Optimize fit of f0 * harmonic_numbers to measured peak frequencies.
%
R = harmonic_numbers * harmonic_numbers';
P = harmonic_numbers * freqs';
f0 = R\P;
if debug > 1,
	disp('Refined F0 estimate via harmonic regression:'); f0
	disp('refined harmonics versus peaks:'); [f0*harmonic_numbers',freqs']
	disp('relative deviation (%%):'); 
        f0_error=100*(f0*harmonic_numbers-freqs)./freqs
	stem(f0_error); 
	title('Relative Harmonic Deviation: Harmonic Minus Peak Over Peak');
end;

fc = max(freqs);

specdbc = max(specdb,minval);
if debug, 
	ttl = 'Signal Frame Spectrum with F0 and Cut-Off Marked';
        clf;
        hold on;
        f = fkHz * 1000;
	plot(f,specdbc,'-k');
        markline = [min(specdbc),max(specdbc)];
	plot([f0 f0], markline);
	plot([fc fc], markline);
        title(ttl);
        xlabel(fxlab);
        ylabel(fylab);
        disp('PAUSING (CUTOFFS) - RETURN to continue'); pause;
        hold off;
end;

% ----------------------------------------------------------------

function [f,fxlab,fylab] = freqlabs(nspec,fs);
%FREQLABS returns freq axis f (kHz), x label, and y label, given 
%         max FFT bin number spec and sampling rate fs (in Hz)
fxlab = 'Frequency (kHz)';
fylab = 'Amplitude (dB)';
f = (fs/2000)*[0:nspec-1]/nspec; % frequency axis for spectral plots

