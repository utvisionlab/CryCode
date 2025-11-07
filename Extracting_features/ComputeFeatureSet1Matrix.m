function featureSelectedMatrix = ComputeFeatureSet1Matrix( directory, fileName)

% Initialize
% waveread changed to audio read in matlab 2015 and then raedwav in voicebox
% toolbox
% As file name is stored in cell type of data I used filename{1} istead of
% filename 

%% Aida changes
filename = strcat(directory,'/', fileName);
[A2,B] = readwav(filename{1});% [y,Fs: samplerate,bits in sample] 
A = A2(:,1);
sampleNum = 882; % 20 ml second 
% frameNum = floor(size(A)/sampleNum);

%% changed by Aida


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Energy %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % AE
    AudioPower = AP(A,size(A),B, sampleNum); % Aida changes
    %meanAE = mean(AudioPower);% Aida changes
    covAE = cov(AudioPower); % Aida changes
    %meanDiffAE = mean(diff(AudioPower));% Aida changes
    diffAE = diff(AudioPower);
    covDiffAE = cov(diffAE); % Aida changes
    clear AudioPower;
    clear diffAE;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Harmonic %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % AFF
    standvar = h_mpeg7init(B,[],[],[],[]);
    f_num = size(A,1)/standvar.hopsize;       %hamid changes
    f0 = AFF(A,standvar,ceil(f_num)-1);      %hamid changes
    %[f0,fc]=AFF(A,B);                      %hamid changes
    meanf0 = mean(f0);
    covf0 = cov(f0);
    %meanDifff0 = mean(diff(f0)); % Aida changes
    diffF0 = diff(f0);
    covDifff0 = cov(diffF0);
    clear f0;



    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Perceptual %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % TL_SONE
    p = struct('fs',B,'do_visu',0,'do_sone',1,'do_spread',1,'outerear','terhardt','fft_size',882,'hopsize',441,'bark_type','table','dB_max',96);
    [sone, Ntot, p] = TL_SONE(A(:,1),p);
    %meanTL = mean(Ntot); %Removd by Aida
    covTL = cov(Ntot);
%     meanDiffTL = mean(diff(Ntot));  %Removd by Aida
    covDiffTL = cov(diff(Ntot));
    
    meanSONE = mean(sone,2); meanSONE = meanSONE(1:8);
    for i=1:8 covSONE(i) = cov(sone(i,:)); end
%     for i=1:8 meanDiffSONE(i) = mean(diff(sone(i,:))); end % Aida changes
    for i=1:8 covDiffSONE(i) = cov(diff(sone(i,:))); end

    clear Ntot;
    clear sone;


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Spectral %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % ASC
    AudioSpectrumCentroid = ASC(filename{1},'PT10N1000F',0,[]);
    meanASC = mean(AudioSpectrumCentroid);
    covASC = cov(AudioSpectrumCentroid);
%     meanDiffASC = mean(diff(AudioSpectrumCentroid)); % Aida changes
    covDiffASC = cov(diff(AudioSpectrumCentroid));

    clear AudioSpectrumCentroid;


    % ASR
    AudioSpectrumRolloff = ASR(filename,0.020);
    meanASR = mean(AudioSpectrumRolloff);
    covASR = cov(AudioSpectrumRolloff);
%     meanDiffASR = mean(diff(AudioSpectrumRolloff)); % Aida changes
    covDiffASR = cov(diff(AudioSpectrumRolloff));
    
    clear AudioSpectrumRolloff;


    % ASS
    AudioSpectrumSpread = ASS(filename{1},'PT10N1000F',0,[]);
    meanASS = mean(AudioSpectrumSpread);
    covASS = cov(AudioSpectrumSpread);
%     meanDiffASS = mean(diff(AudioSpectrumSpread)); % Aida changes
    covDiffASS = cov(diff(AudioSpectrumSpread));

    clear AudioSpectrumSpread;


    % MFCC
    [ceps,freqresp,fb,fbrecon,freqrecon] = MFCC(A, B);
    [C1 C2] = size(ceps);
    for i=1:C1 for j=1:C2 if(isinf(ceps(i,j)) || isnan(ceps(i,j))) ceps(i,j) = 0; end; end; end;
    meanMFCC = mean(ceps(2:end,:),2); %removing first coefficient of MFCC % Aida changes
    for i=2:C1 covMFCC(i-1) = cov(ceps(i,:)); end
%     for i=1:C1 meanDiffMFCC(i) = mean(diff(ceps(i,:))); end % Aida changes
    for i=2:C1 covDiffMFCC(i-1) = cov(diff(ceps(i,:))); end

    clear ceps;
    clear freqresp;
    clear fb;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Temporal %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % AC
    ACcoefs = AC(A);

    % LAT
    energy_bp = h_energy(A, B, 2000, 2);
    LogAttackTime = LAT(energy_bp, 20); % changed from 50 to 20 by Aida;based on its paper

    % TC
    TemporalCentroid = TC(energy_bp);

    clear energy_bp;

    % ZCR
    [ZCR1 avZCR] = ZCR(A(:,1),0.020); %changed by Aida from 16ms to 20
%     meanZCR = mean(ZCR1); % Aida changes
    covZCR = cov(ZCR1);
    %meanDiffZCR = mean(diff(ZCR1));% Aida changes
    %covDiffZCR = cov(diff(ZCR1));% Aida changes

    clear ZCR1;


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Various %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % ASF
    [AudioSpectrumFlatness ,lo_edge, hi_edge, XMLFile ] = ASF(A,B,'PT10N1000F',250,500,0,[]); % for 20 ms
    [AudioSpectrumFlatness2 ,lo_edge, hi_edge, XMLFile ] = ASFTwo(A,B,'PT10N1000F',125,250,0,[]); % for 20 ms
    [ASF1 ASF2] = size(AudioSpectrumFlatness);
    [ASF3 ASF4] = size(AudioSpectrumFlatness2);
    meanASF = mean(AudioSpectrumFlatness,1);
    meanASF2 = mean(AudioSpectrumFlatness2,1);
    for i=1:ASF2 
        covASF(i) = cov(AudioSpectrumFlatness(:,i)); 
    end
    for i=1:ASF2 
        covDiffASF(i) = cov(diff(AudioSpectrumFlatness(:,i))); 
    end
    for i=1:ASF4
        covASF2(i) = cov(AudioSpectrumFlatness2(:,i)); 
    end
    for i=1:ASF4 
        covDiffASF2(i) = cov(diff(AudioSpectrumFlatness2(:,i))); 
    end

    clear AudioSpectrumFlatness;
    clear AudioSpectrumFlatness2;
    
    % AudioPower
    AudioAmplitude = AP2(A,size(A),B,sampleNum); % chanded by Aida
    %meanAP = mean(AudioAmplitude);% chanded by Aida
    covAP = cov(AudioAmplitude);% chanded by Aida
    diffAP = diff(AudioAmplitude);
    covDiffAP = cov(diffAP); % chanded by Aida
    
    clear AudioAmplitude;
    clear diffAP;

    featureMatrix = [];
    featureMatrix = [featureMatrix covAE covDiffAE]; % meanAE, meanDiffAE and other similar features removed by Aida
    featureMatrix = [featureMatrix meanf0 covf0 covDifff0];
    featureMatrix = [featureMatrix covTL covDiffTL];
    featureMatrix = [featureMatrix covSONE covDiffSONE];
    featureMatrix = [featureMatrix meanASC covASC covDiffASC];
    featureMatrix = [featureMatrix meanASR covASR covDiffASR];
    featureMatrix = [featureMatrix meanASS covASS covDiffASS];
    featureMatrix = [featureMatrix meanMFCC' covMFCC covDiffMFCC];
    featureMatrix = [featureMatrix ACcoefs];
    featureMatrix = [featureMatrix LogAttackTime];
    featureMatrix = [featureMatrix TemporalCentroid];
    featureMatrix = [featureMatrix covZCR];% meanZCR removed by Aida
    featureMatrix = [featureMatrix meanASF covASF covDiffASF];
    featureMatrix = [featureMatrix meanASF2 covASF2 covDiffASF2]; % By Aida
    featureMatrix = [featureMatrix covAP covDiffAP];


    clear meanAP covAP meanDiffAP covDiffAP;
    clear meanf0 covf0 meanDifff0 covDifff0;
    clear meanTL covTL meanDiffTL covDiffTL;
    clear meanSONE covSONE meanDiffSONE covDiffSONE;
    clear meanASC covASC meanDiffASC covDiffASC;
    clear meanASR covASR meanDiffASR covDiffASR;
    clear meanASS covASS meanDiffASS covDiffASS;
    clear meanMFCC covMFCC meanDiffMFCC covDiffMFCC;
    clear ACcoefs LogAttackTime TemporalCentroid;
    clear meanZCR covZCR meanDiffZCR covDiffZCR;
    clear meanASF covASF meanDiffASF covDiffASF;
    clear meanAE covAE meanDiffAE covDiffAE;
    
    featureSelectedMatrix = featureMatrix;

end



