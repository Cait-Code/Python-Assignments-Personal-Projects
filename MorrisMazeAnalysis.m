function outputStruct = MorrisMazeAnalysis(path) 
% A function to plot the path trajectory of a mouse in a Morris Water Maze...
%over successive trials and plot the cumulative path length.
    % path = input: a character array of the file directory containing...
    %all of the .tif files to be analysed. 
    % OutputStruct = output: a structure containing the fields:
        %o	File_Name           : The filename of each experiment.
        %o  Mouse_Coordinates  : row (i.e. Y-axis) and column (i.e. X-axis)...
        %pixel coordinates for each of the positions that the mouse ...
        %travelled through in the water maze in each trial of the experiment. 
        %o	Distance_Per_Trial  : The distance travelled by the mouse in...
        %each trial/training day of the experiment.
    %
    % A png file containing path trajectories of the mouse during...
    %experimental trials 1-6 is saved as 'TrajectoryPathOverlays.png'
    % A png file containing cumulative path length in (m) of the mouse...
    %during experimental trials 1-6 is saved as 'TrialLearning.png'

    % -- files to analyse -- %
    files = dir([path '\*.tif']); %list of file names in parent directory
    nFiles = numel(files); % number of files to analyse
    
    
    listCumMetre = zeros(1,nFiles); % pre-allocate cumulative metres for each trial as an array
    Mouse_Coordinates = struct([]); % create a structure to hold mean X and Y coordinates per file
    
    
    %% Make a loop to batch process every frame of the TIF movie file.
    for i = 1:nFiles %open batch for loop
        fn = files(i).name; %name of current file to be analysed

        % -- Read image file -- %
        info = imfinfo(fn); %file info : 8-bit grayscale
        nFrames = numel(info); % number of frames in TIF file

        I = [];         % pre-allocate image array
        meanX = zeros(1,nFrames); % pre-allocate for X-coordinates of the...
        %mouse in each frame of the .TIF files.
        meanY = zeros(1,nFrames); % pre-allocate for Y-coordinates of the...
        %mouse in each frame of the .TIF files.
        ax = axes;

        for k = 1:nFrames
            frame = imread(fn,k);   % read frame k
            I = cat(3,I,frame); % concatenate frame k to array I

            %--Detect the mouse based on contrast to background--%
            I1 = I(:,:,k);
            Ic = imcomplement(I1); % Conversion of image
            framebin = imbinarize(Ic,0.746); % Convert image to black and...
            %white, then find mouse by thresholding pixel intensity

            %-- Find the position of the mouse in X(columns) and Y(rows). --%
            % Find the coordinates for the perimeter of the mouse
            coords = bwboundaries(framebin); % find coords for the ...
            %perimeter of mouse for each frame (k)
            % Find the center of the mouse in each frame
            meanY(k) = mean(coords{1}(:,1)); % mean (y) Coordinates
            meanX(k) = mean(coords{1}(:,2)); % mean (x) Coordinates
            
        end
        
        Mouse_Coordinates(i).File_Name = fn;
        Mouse_Coordinates(i).meanX = meanX;  % For each file (i), save X...
        %coordinates of the mouse for each frame
        Mouse_Coordinates(i).meanY = meanY;  % For each file (i), save Y...
        %coordinates of the mouse for each frame
        
        
        %--Calculate the distance moved by the mouse from one frame to the
        %next (length of hypoteneuse = distance between 2 positions).--%
        % Calculate the difference between the Y coordinates in each frame
        diffY = diff(meanY);
        % Calculate the difference between the X coordinates in each frame
        diffX = diff(meanX);
        % Find distance moved between frames, where abs changes negatives...
        %to positives so they do not subtract from path length
        DistBetweenFrames = hypot(diffX,diffY); 

        % Find the cumulative length of the path swam by the mouse to reach the escape platform.

        CumLength = sum(DistBetweenFrames,'all'); % Cumulative Distance in Pixels

        %--Convert the path length from pixels to metres (pool diameter = 1 metre).--%
        % Find the length of the pool
        % figure% new figure	
        % imgPool = imread('watermaze_7182_day1.tif');	% Read in an example movie to observe size of pool	
        % imagesc(imgPool)			% display image
        % [X,Y] = ginput(2); 		% select vertex coordinates of ROI	
        % Xi = round(X);		% convert X coordinates to integers 
        % Yi = round(Y);		% convert Y coordinates to integers
        % Xi = [6;167], Yi = [4;171]
        % 167-6 = 161 pix by 171-4 = 167 pix
        % 1m = mean(161,167) = 164 pix
        % 1 / 164 =  each pixel = 0.006m
        CumMetre = CumLength*0.006; % Cumulative Distance in Metres

        listCumMetre(i) = CumMetre; % Saved the cumulative distance (m) for each file

        subplotRows = 2; %create index
        subplotColumns = ceil(nFiles/subplotRows); %create index
        subplot(subplotRows,subplotColumns,i); % Generating number of ...
        %subplots needed, accounting for an odd number of plots
        imshow(I1,[]) % Display mouse in maze image    
        hold on
        plot(meanX,meanY,'r') 
        subplot(subplotRows,subplotColumns,i), title(append('Day',' ',int2str(i)));
     

    end
    
    % Give titles etc
    overallTitle = sgtitle('Path Trajectories on Successive Trial Days','Color','red');
    overallTitle.FontSize = 20;
    %% Save the figure as a png file
    saveas(gcf,'TrajectoryPathOverlays.png')
 

    %% --- Plot a graph illustrating the swim path length for each successive experiment
    figure
    plot(1:nFiles,listCumMetre,'-o','MarkerFaceColor','blue')
    xlabel('Training Day')
    ylabel('Path Length(m)')
    title('Spatial Learning Across Successive Trials')
    %% Save the figure as a png file
    saveas(gcf,'TrialLearning.png')
    

    %% Create an output argument as a structure 
    outputStruct.File_Names = files;
    outputStruct.Mouse_Coordinates = Mouse_Coordinates;
    outputStruct.Distance_Per_Trial = listCumMetre;
end
