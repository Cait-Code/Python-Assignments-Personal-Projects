function outputStructArray = fEPSP_analysis(Filename)
%% outputStructArray = fEPSP_analysis(Filename) imports and analyses wcp data, where filename is a string containing the filename. 
 % Input: Filename, a string containing the filename of the chosen data
 % To run the function for the chosen data, enter into the command line : S1_660043595('notebook.xlsx')
 
 % outputStructArray is the output structure containing the fields: 
 % File_Names    A cell array containing the name of the file/experiment imported as a wcp file. 
 % Traces        A structure containing the trace data for each experiment
 % Trace_Figures A structure containing the figures for each experiment
 % Average_Peak  The average peak amplitude of the 1st fEPSP in each of the drug conditions

% A png file containing example traces of drug conditions and a time-course plot of an individual experiment saved as 'Traces.png' 
% A png file containing a box plot summarising the average peak amplitude across the four experimental conditions is saved as 'BoxplotDrugs.png' 
% A png file containing the results of a Multiple Comparisons of Means test is saved as 'MultipleComparisons.png'
% A statement is generated based on the p-value significance of a 1 way ANOVA test/Kruskall-Wallis test, depending on normality of the data.  


%% Import and edit raw data

% Read the excel file (.xlsx file) 
t = readtable(Filename);

% Determine the number of files to analyse using information stored in the excel file.
numOfFiles = size(t,1);

% Initiate a list of zeros to be filled by the average peak data required for the Boxplot
CtrlMatrix = zeros(1,numOfFiles);
CADOMatrix = zeros(1,numOfFiles);
DPCPXMatrix = zeros(1,numOfFiles);
NBQXMatrix = zeros(1,numOfFiles);

% Initiate a structure for the trace data
traces = struct([]);

% Initiate a structure for the trace figure handles
traceFigures = struct([]);

%% Generate a for-loop to batch-analyse files
for n = 1:numOfFiles 
% load files
    out = import_wcp(t.Filename{n});
   
% Make a time axis for the example traces and add the time axis to the structure called out
     Fs = 1/out.t_interval;
     [out(:).timeAxis] = 0:(1/Fs):(1/Fs)*(length(out.T)-(1/Fs));
     
%% Generate baseline
% Set the baseline to 0mV across all experimental replicates

% Create an index for the baseline region
     ind=out.T<=0.009; 
     
% Calculate the mean baseline 
     mean_base = mean(out.S{1,1}(ind, : )); 
     
% Reset the baseline in the original array
     out.S{1,1}=out.S{1,1} - mean_base;
     
%% Define the analysis window
% Define the window of time between 0.013 and 0.05(s) corresponding to the
% first signal
     windowTime = out.T>0.013 & out.T<0.05;
     
%% Find the minimum peak value within the pre-defined window
% Calculate and add the minimum peak value to the structure called out
     [out(:).Minimum] = min(out.S{1,1}(windowTime,:));
     
%% Plot an individual experiment

% Generate baselines for the Control, CADO, DPCPX and NBQX conditions
     windowFileBaseline = (out.S{1,1}(windowTime,(t.CADO(n)-1))); %baseline of Control
     windowFileCADO = out.S{1,1}(windowTime,(t.CADO_DPCPX(n)-1)); % baseline of CADO
     windowFileDPCPX = out.S{1,1}(windowTime,(t.CADO_DPCPX_NBQX(n)-1)); % baseline of DPCPX
     windowEND = size(out.S{1,1},2); 
     windowFileNBQX = out.S{1,1}(windowTime,(windowEND)); % baseline of NBQX
     
% Generate subplot figure and plot an example trace for each of the four drug conditions 
     figure;
     Baseplot = subplot(2,4,1); % Example trace: Control
     plot(Baseplot,out.T(windowTime), windowFileBaseline, 'black'),title('Control'),xlabel('time(S)'),ylabel('Amplitude of 1st fEPSP(mV)');
     hold on
     plot(Baseplot,out.T(windowTime), smoothdata(windowFileBaseline), 'red'); % Smoothed line
     Cadoplot = subplot(2,4,2); % Example trace: CADO
     plot(Cadoplot,out.T(windowTime), windowFileCADO, 'black'),title('CADO'),xlabel('time(S)'),ylabel('Amplitude of 1st fEPSP(mV)');
     hold on
     plot(Cadoplot,out.T(windowTime), smoothdata(windowFileCADO), 'red') % Smoothed line
     Dpcpxplot = subplot(2,4,3); % Example trace: DPCPX
     plot(Dpcpxplot,out.T(windowTime), windowFileDPCPX, 'black'),title('CADO + DPCPX'),xlabel('time(S)'),ylabel('Amplitude of 1st fEPSP(mV)'); 
     hold on
     plot(Dpcpxplot,out.T(windowTime), smoothdata(windowFileDPCPX), 'red') % Smoothed Line
     Nbqxplot = subplot(2,4,4); % Example trace : NBQX
     plot(Nbqxplot,out.T(windowTime), windowFileNBQX, 'black'), title('CADO + DPCPX + NBQX'),xlabel('time(S)'),ylabel('Amplitude of 1st fEPSP(mV)');
     hold on
     plot(Nbqxplot,out.T(windowTime), smoothdata(windowFileNBQX), 'red') % Smoothed Line
       
%Set axes so that plots are comparable
     linkaxes([Baseplot Cadoplot Dpcpxplot Nbqxplot],'xy')
     
%% Plot a time course for an individual experiment (a plot of time vs 1st fEPSP amplitude)
% Generate a plot of the 1st fEPSP indicating points at which the drugs
% were added

% Generate subplot for the time-course plot
     timeplot = subplot(2,4,5:8);
     sizeNum = size(out.S{1,1},2); %for the number of columns in the S array
     
% Make the time and amplitude axes for the time-course plot
     yplot=  out.Minimum; 
     xplot = linspace(0,sizeNum-1,sizeNum)*10;
    
% Plot time-course plot of an individual experiment
     scatter(timeplot,xplot,yplot,'black'),title('Time Course Plot'),xlabel('Time(s)'),ylabel('Amplitude of 1st fEPSP(mV)')
     hold on
     plot(timeplot,xplot,smoothdata(yplot),'red') % Smooth data
     xline((t.CADO(n)-1)*10,'magenta'); % Line indicating the addition of CADO drug
     xline((t.CADO_DPCPX(n)-1)*10,'blue'); % Line indicating the addition of DPCPX drug
     xline((t.CADO_DPCPX_NBQX(n)-1)*10,'green'); % Line indicating the addition of NBQX drug
     legend('Time Course Plot','Smoothed Plot','Addition of CADO','Addition of DPCPX','Addition of NBQX')

% Save the trace figures as a png file
     saveas(gcf,'Traces.png')
     
%% Preparation of data for the output structure
% Allocate data to necessary structures

% Structure of traces to be entered into the final output structure,'outputStructArray'
    traces(n).wcpFilename = t.Filename{n};
    traces(n).Baseline =[out.T(windowTime)',windowFileBaseline];
    traces(n).CADO = [out.T(windowTime)', windowFileCADO];
    traces(n).DPCPX = [out.T(windowTime)', windowFileDPCPX];
    traces(n).NBQX = [out.T(windowTime)', windowFileNBQX];
    
% traceFigures to be entered into the final output structure,'outputStructArray'
    traceFigures(n).wcpFilename = t.Filename{n};
    traceFigures(n).figure = gcf;   

%% Determine the average peak amplitude of the 1st response in the 4 conditions across all the experimental replicates  
    CtrlMatrix(n) = min(windowFileBaseline);
    CADOMatrix(n) = min(windowFileCADO);
    DPCPXMatrix(n)= min(windowFileDPCPX);
    NBQXMatrix(n) = min(windowFileNBQX);
       
end

%% Statistical analyses and generation of the Boxplot
%Test if there is a significant difference in peak amplitude of the 1st response in the 4 conditions across all the experimental replicates

% Generate matrices for the statistical analyses
 CtrlMatrix = CtrlMatrix*-1;
 CADOMatrix = CADOMatrix*-1;
 DPCPXMatrix= DPCPXMatrix*-1;
 NBQXMatrix = NBQXMatrix*-1;
 AnoMatrix = [CtrlMatrix;CADOMatrix;DPCPXMatrix;NBQXMatrix];
 AnoMatrix = AnoMatrix';
 
% Kolmogorov-Smirnov test to check if data is normally distributed
 o = kstest(AnoMatrix);
 
% -- Determination of statistical method and generation of the Boxplot: --
% Kruskal Wallis for non-normal data,1-way anova for normally distributed data
 if o == 1
    disp(['The data is not normally distributed']) 
    
% Kruskal Wallis test
    [p,tbl,stats] = kruskalwallis(AnoMatrix); 
    title('Drug Conditions against Average Peak Amplitude of the First Response'),ylabel(' Average Peak Amplitude (mV)');
    if p <0.05 
        disp(['The p-value is ' num2str(p) ', there is a significant difference between the average peak amplitude(mV) of the 1st response across experimental conditions']) 
    else 
        disp(['The p-value is ' num2str(p), ', there is no significant difference between the average peak amplitude(mV) of the 1st response across experimental conditions']) 
    end
 else 
    disp(['The data is normally distributed']) 
    
% One-way Anova test
 [p,tbl,stats] = anova1(AnoMatrix); 
 title('Drug Conditions against Average Peak Amplitude of the First Response'),ylabel(' Average Peak Amplitude (mV)');
    if p <0.05 
    disp(['The p-value is ' num2str(p) ', there is a significant difference between the average peak amplitude(mV) of the 1st response across experimental conditions']) 
    else 
    disp(['The p-value is ' num2str(p), ', there is no significant difference between the average peak amplitude(mV) of the 1st response across experimental conditions']) 
    end
 end
 
% Rename Boxplot labels
xticklabels({'Control','CADO','DPCPX','NBQX'});
 
% Create Legend for the Boxplot 
hLegend = legend(findall(gca,'Tag','Box'), {'Box plot displaying upper and lower Quartiles, median and whiskers.'});

% Remove Outliers
Outlier=findobj(gca,'tag','Outliers');
delete(Outlier)
 
% Save the Boxplot as a png file
saveas(gcf,'BoxplotDrugs.png')

%% Conduct a Multiple Comparison of means test

% Create a cell array containing identifiers for the four conditions.
 drug_names = {'Control','CADO','CADO+DPCPX','CADO+DPCPX+NBQX'};
 
% Tukey-Kramer Multiple Comparisons Test
 figure()
 [~,~,hMult,~]=multcompare(stats,'Alpha',0.05,'CType','hsd');
 
% Sort axes labels for the multiple comparisons graph 
 hMult.Children.YTickLabel = flipud(drug_names); 
 
% Save the Multiple Comparison test output as a png file
 saveas(gcf,'MultipleComparisons.png')

 %% Create output structure array containing the results of the analyses of all the .wcp files.
outputStructArray.File_Names = t.Filename;
outputStructArray.Traces = traces;
outputStructArray.Trace_Figures = traceFigures;
outputStructArray.Average_Peak = AnoMatrix;

end


