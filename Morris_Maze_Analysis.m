function outputStruct = Morris_Maze_Analysis(folderPath)
% A function to plot the path trajectory of a mouse in a Morris Water Maze experiment over successive training days and plot the cumulative path length.
% > Call the function in the command line as S2_660043595('Your Path Directory')
% > When calling the function with no input, a manual selection of files is required. This assumes the user locates the directory and the files selected are sequential training days.
%
%     folderPath = input: a character array of the file directory containing all...
%                   of the .tif files to be analysed. 
%     outputStruct = output: a structure containing the following fields:
%        o	File_Names         : The filename of each experimental trial.
%        o  Mouse_Coordinates  : X- and Y-axis pixel coordinates for each...
%                                of the positions that the mouse travelled...
%                                through in the water maze in each trial.  
%        o	Distance_Per_Trial : The distance travelled by the mouse in...
%                                each trial of the experiment in metres(m).
%        o	Path_Length_Slopes : Slope of the plotted line between days.
%
%     A png file containing path trajectories of the mouse during experimental...
%     trials is saved as 'TrajectoryPathOverlays.png'
%     A png file containing cumulative path length in metres(m) of the mouse...
%     during experimental trials is saved as 'TrialLearning.png'

    %% Evaluate the input provided
    if nargin < 1 % Test case for no input given when the function is called
        [files, folderPath] = askUserFileName(); % Subfunction for manual selection of files
    else
        files = getFileNames(folderPath); % Subfunction for one directory input
    end

    %% Defining some parameters
    nFiles = numel(files); % Number of files to analyse
    
    if nFiles == 1
        subplotRows = 1; % Index for number of subplot rows for 1 file
    else
        subplotRows = 2; % Index for number of subplot rows for >1 files 
    end
    
    subplotColumns = ceil(nFiles/subplotRows); % Index for number of...
    % subplot columns, accounting for an odd number of plots
    
    % -- Conversion for pixels to metres 
    %imgPool = imread('watermaze_7182_day1.tif'); % Read in an example file
    %imagesc(imgPool);[X,Y] = ginput(2); % Display image and select ROI	
    %Xi = round(X); Yi = round(Y); % convert X and Y coordinates to integers
    %PixelsX = Xi(2)-Xi(1); PixelsY = Yi(2)-Yi(1); % Find the number of pixels...
    % in X/Y axes corresponding to 1m
    %PoolSizePixels = mean(PixelsX,PixelsY); % Account for variability/manual...
    % error in selecting pool edges
    %PixelToMetre = 1/PoolSizePixels; % Each pixel represents PixelToMetre(m)
    PixelToMetre = 0.006; % Constant for pixel to metre conversion
    
    %% Pre-allocation
    listCumulativeMetre = zeros(1,nFiles); % Pre-allocate cumulative metres...
    % for each file as an array
    Mouse_Coordinates = struct([]); % Create a structure to hold mean X and...
    % Y coordinates per file
         
    %% Make a loop to batch process every frame of the TIF movie file.
    for i = 1:nFiles 
        fn = [folderPath '\' files(i).name]; % Name of current file to be analysed

        % Read image file 
        info = imfinfo(fn); % Obtain file info
        nFrames = numel(info); % Number of frames in TIF file

        % Pre-allocation for frames
        I = [];         % Pre-allocate image array
        meanX = zeros(1,nFrames); % Pre-allocate for X-coordinates of the...
        % mouse in each frame of the .TIF files.
        meanY = zeros(1,nFrames); % Pre-allocate for Y-coordinates of the...
        % mouse in each frame of the .TIF files.
        

        for k = 1:nFrames
            frame = imread(fn,k); % Read frame k
            I = cat(3,I,frame); % Concatenate frame k to array I

            %% Detect the mouse based on contrast to the background 
            I1 = I(:,:,k); % Stack image
            Ic = imcomplement(I1); % Complement of image 
            framebin = imbinarize(Ic,0.746); % Convert image to black and white,...
            % find mouse by thresholding pixel intensity values

            %% Find the coordinates for the perimeter of the mouse
            coords = bwboundaries(framebin); % Find coordinates for the perimeter...
            % of mouse for each frame (k)
            % Find the central position of the mouse in X(columns) and Y(rows).
            meanY(k) = mean(coords{1}(:,1)); % Mean (Y) Coordinates
            meanX(k) = mean(coords{1}(:,2)); % Mean (X) Coordinates
                
        end
        
        % for each file(i) append X/Y coordinates of the mouse for each frame
        Mouse_Coordinates(i).File_Name = fn;
        Mouse_Coordinates(i).meanX = meanX;  
        Mouse_Coordinates(i).meanY = meanY; 
        
        %% Calculate the distance moved by the mouse from one frame to the next 
        % Calculate the difference between the Y coordinates in frames n-1
        diffY = diff(meanY);
        % Calculate the difference between the X coordinates in frames n-1
        diffX = diff(meanX);
        % Find the distance moved between frames 
        DistBetweenFrames = hypot(diffX,diffY); 

        %% Find the cumulative length of the path swam by the mouse per file
        CumulativeLength = sum(DistBetweenFrames,'all'); 
        % Convert the path length from pixels to metres(pool diameter = 1m)
        CumulativeMetre = CumulativeLength*PixelToMetre; 
        listCumulativeMetre(i) = CumulativeMetre; % Append the cumulative...
        % distance(m) for each file

        %% Plot the Path Trajectory of the mouse per trial
        subplot(subplotRows,subplotColumns,i); % Generate subplots of (i)files
        imshow(I1,[]); % Display maze     
        hold on 
        plot(meanX,meanY,'r') % Plot mouse path trajectories
        plot(Mouse_Coordinates(i).meanX(1),Mouse_Coordinates(i).meanY(1),...
            'Marker','o','color','b') % Marker to indicate starting position
        title(append('Day',' ',int2str(i)));
    end
    
    %% Give legends, titles etc to the plot(s)
    overallTitle = sgtitle('Path Trajectories on Successive Training Days','Color','red');
    overallTitle.FontSize = 15;
    legend('Path Trajectory','Starting Position','position',[.5 .07 .0 .0],'Orientation','horizontal');
    % Save the figure as a png file
    saveas(gcf,'TrajectoryPathOverlays.png')
 

    %% Plot a graph illustrating the cumulative path length for each successive trial
    figure
    plot(1:nFiles,listCumulativeMetre,'-o','MarkerFaceColor','blue'); % Plot...
    % cumulative length (m) per Training Day
    slopes = diff(listCumulativeMetre)./diff(1:nFiles); % Determine line slopes...
    % between points
    xlabel('Training Day')
    ylabel('Path Length(m)')
    title('Cumulative Path Lengths Across Successive Training Days')
    % Save the figure as a png file
    saveas(gcf,'TrialLearning.png')
    

    %% Create an output argument containing the results of the analyses
    outputStruct.File_Names = files;
    outputStruct.Mouse_Coordinates = Mouse_Coordinates;
    outputStruct.Distance_Per_Trial = listCumulativeMetre;
    outputStruct.Path_Length_Slopes = slopes;
end

%% Make a local subfunction to get file names in the case of no path input
function [files, folderPath] = askUserFileName() 
    % Select file(s) manually using GUI    
    message = sprintf('You have not entered an input.\nLocate your directory and select sequential training day .tif files.');
    uiwait(msgbox(message)); 
    [fileList, folderPath] = uigetfile('\*.tif','Multiselect','on'); 
    
    % Initiating an empty struct for file names
    files = struct([]);    
    % For number of manually selected files being 1
    if isa(fileList, 'char') 
        files(1).name = fileList; 
    else
        % For number of manually selected files >1
        for i = 1:length(fileList) 
            files(i).name = fileList{i}; % append to struct
        end
    end
    
    files = sortFileName(files); % Call subfunction to sort given file names 
end 

%% Make a local subfunction to get files from the directory
function files = getFileNames(folderPath)   
    % Files to analyse 
    files = dir([folderPath '\*.tif']); % List of .tif file names in parent directory
end

%% Make a local subfunction to sort given file names into chronological days if not selected in order by the user
function files = sortFileName(inputfiles)
    t = struct2table(inputfiles); % convert files struct into a table to sort
    t = sortrows(t,'name'); % sort selected files by name
    files = table2struct(t); % convert table back to struct for analyses
end