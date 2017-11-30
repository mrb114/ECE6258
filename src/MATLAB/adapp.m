classdef adapp < handle

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                        matlab.ui.Figure
        ImFigure
        OriginalorCompositeButtonGroup  matlab.ui.container.ButtonGroup
        OriginalImconfidentButton       matlab.ui.control.RadioButton
        OriginalImnottooconfidentButton  matlab.ui.control.RadioButton
        CompositeImnottooconfidentButton  matlab.ui.control.RadioButton
        CompositeImconfidentButton      matlab.ui.control.RadioButton
        HowobnoxiousaretheartifactsLabel  matlab.ui.control.Label
        HowobnoxiousaretheartifactsSlider  matlab.ui.control.Slider
        SubmitButton                    matlab.ui.control.Button
        ImageXofYLabel                  matlab.ui.control.Label
    end

    % User-set properties
    properties (Access = public)
        imagedir = '\\prism.nas.gatech.edu\cseng3\vlab\documents\GitHub\ECE6258\Images\IQDev';
        metafilename = '\\prism.nas.gatech.edu\cseng3\vlab\documents\MATLAB\project\GUI\imageinfo.xlsx';
        resultsfilename = '\\prism.nas.gatech.edu\cseng3\vlab\documents\MATLAB\project\GUI\results.xlsx';
        resultsTable = table;
    end
    
    properties (Access = private)
        image % Description
        imageFilename
        userName = {'test123'};
        isGreyscale
        metatable
        currentTestIndex
        currentEntry
        testOrder
        resultsHeaders = {'UserName','Timestamp','SetIndex',...
                'SetName','ImageIndex','IsComposite','ParentIndex','Filename','Response'};
    end

    % Callback functions
    methods (Access = private)

        % Button pushed function: SubmitButton
        function SubmitButtonPushed(app, event, handles)
            if strcmp(app.OriginalorCompositeButtonGroup.Visible,'on') && ~app.originalSelected
                app.OriginalorCompositeButtonGroup.Visible = 'off';
                app.HowobnoxiousaretheartifactsLabel.Visible = 'on';
                app.HowobnoxiousaretheartifactsSlider.Visible = 'on';
            else
                writeResponse(app);
                app.HowobnoxiousaretheartifactsLabel.Visible = 'off';
                app.HowobnoxiousaretheartifactsSlider.Visible = 'off';
                close(app.ImFigure);
                app.OriginalorCompositeButtonGroup.Visible = 'on';
                showNextImage(app);
            end
        end
        
    end

    % Helper functions
    methods (Access = private)
        
        % determines if the user selected one of the "original" radio buttons
        function result = originalSelected(app)
            result = app.OriginalImconfidentButton.Value || ...
                app.OriginalImnottooconfidentButton.Value;
        end
        
        % assigns value 1-4 for radio button selection
        function result = response1Value(app)
            result = find([app.OriginalImconfidentButton.Value,... % 1
                           app.OriginalImnottooconfidentButton.Value,... % 2
                           app.CompositeImnottooconfidentButton.Value,... % 3
                           app.CompositeImconfidentButton.Value... % 4
                         ]);
        end
    end
    
    % App initialization and construction
    methods (Access = private)

        % Select the images to show in the assessment
        function composeTest(app)
            nSets = max(app.metatable.SetIndex);
            setOrder = randperm(nSets);
            
            imOrder = [];
            for k = 1:nSets
                theSet = setOrder(k);
                nIm = max(app.metatable.ImageIndex(app.metatable.SetIndex == theSet));
                iidx = randi([1 nIm]);
                imOrder = cat(1,imOrder,find(app.metatable.SetIndex == theSet & app.metatable.ImageIndex == iidx));
            end
            
            app.testOrder = imOrder;
        end
        
        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure
            app.UIFigure = uifigure;
            app.UIFigure.Position = [100 100 288 194];
            app.UIFigure.Name = 'UI Figure';
            app.UIFigure.Resize = 'off';
            app.UIFigure.Visible = 'off';

            % Create OriginalorCompositeButtonGroup
            app.OriginalorCompositeButtonGroup = uibuttongroup(app.UIFigure);
            app.OriginalorCompositeButtonGroup.Title = 'Original or Composite?';
            app.OriginalorCompositeButtonGroup.Position = [14 51 252 117];

            % Create OriginalImconfidentButton
            app.OriginalImconfidentButton = uiradiobutton(app.OriginalorCompositeButtonGroup);
            app.OriginalImconfidentButton.Text = 'Original, I''m confident';
            app.OriginalImconfidentButton.Position = [11 71 139 15];
            app.OriginalImconfidentButton.Value = true;

            % Create OriginalImnottooconfidentButton
            app.OriginalImnottooconfidentButton = uiradiobutton(app.OriginalorCompositeButtonGroup);
            app.OriginalImnottooconfidentButton.Text = 'Original, I''m not too confident';
            app.OriginalImnottooconfidentButton.Position = [11 49 179 15];

            % Create CompositeImnottooconfidentButton
            app.CompositeImnottooconfidentButton = uiradiobutton(app.OriginalorCompositeButtonGroup);
            app.CompositeImnottooconfidentButton.Text = 'Composite, I''m not too confident';
            app.CompositeImnottooconfidentButton.Position = [11 27 196 15];

            % Create CompositeImconfidentButton
            app.CompositeImconfidentButton = uiradiobutton(app.OriginalorCompositeButtonGroup);
            app.CompositeImconfidentButton.Text = 'Composite, I''m confident';
            app.CompositeImconfidentButton.Position = [11 5 155 15];

            % Create HowobnoxiousaretheartifactsLabel
            app.HowobnoxiousaretheartifactsLabel = uilabel(app.UIFigure);
            app.HowobnoxiousaretheartifactsLabel.HorizontalAlignment = 'right';
            app.HowobnoxiousaretheartifactsLabel.Position = [47 128 186 15];
            app.HowobnoxiousaretheartifactsLabel.Text = 'How obnoxious are the artifacts? ';
            app.HowobnoxiousaretheartifactsLabel.Visible = 'off';

            % Create HowobnoxiousaretheartifactsSlider
            app.HowobnoxiousaretheartifactsSlider = uislider(app.UIFigure);
            app.HowobnoxiousaretheartifactsSlider.Limits = [0 10];
            app.HowobnoxiousaretheartifactsSlider.MinorTicks = [];
            app.HowobnoxiousaretheartifactsSlider.Position = [16 105 247 3];
            app.HowobnoxiousaretheartifactsSlider.Value = 5;
            app.HowobnoxiousaretheartifactsSlider.Visible = 'off';

            % Create SubmitButton
            app.SubmitButton = uibutton(app.UIFigure, 'push');
            app.SubmitButton.ButtonPushedFcn = @app.SubmitButtonPushed;
            app.SubmitButton.Position = [13 15 100 22];
            app.SubmitButton.Text = 'Submit';

            % Create ImageXofYLabel
            app.ImageXofYLabel = uilabel(app.UIFigure);
            app.ImageXofYLabel.HorizontalAlignment = 'center';
            app.ImageXofYLabel.Position = [195.5 19 74 15];
            app.ImageXofYLabel.Text = 'Image X of Y';
        end
        
        function result = loadImage(app)
            app.image = imread(app.imageFilename);
            app.isGreyscale = size(size(app.image)) < 3;
            result = true;
        end
        
        function result = loadMetadata(app)
            app.metatable = readtable(app.metafilename);
            result = true;
        end
        
        function showNextImage(app)
            app.currentTestIndex = app.currentTestIndex+1;
            app.ImageXofYLabel.Text = [num2str(app.currentTestIndex),' of ',num2str(length(app.testOrder))];
            if app.currentTestIndex <= length(app.testOrder)
                theEntry = app.metatable(app.testOrder(app.currentTestIndex),:);
                app.currentEntry = theEntry;
                app.imageFilename = fullfile(app.imagedir,theEntry.Filename{:});
                loadImage(app);
                displayImage(app);
                uistack(app.ImFigure,'bottom');
            else
                msgbox('Assessment completed!','Done');
                app.UIFigure.Visible = 'off';
                writeResultsTableToFile(app);
                % delete(app);
            end
        end
        
        function result = displayImage(app)
            hFig = figure('Toolbar','none','Menubar','none');
            if app.isGreyscale
                hIm = imshow(app.image,[0 255]);
            else
                hIm = imshow(app.image);
            end
            hSP = imscrollpanel(hFig,hIm); % Handle to scroll panel.
            set(hSP,'Units','normalized','Position',[0 .1 1 .9])
            
            hMagBox = immagbox(hFig,hIm);
            pos = get(hMagBox,'Position');
            set(hMagBox,'Position',[0 0 pos(3) pos(4)])
            imoverview(hIm)
            app.ImFigure = hFig;
            
            result = true;
        end
        
        function writeResponse(app)
            % User name
            app.resultsTable{app.currentTestIndex,'UserName'} = app.userName;
            % Timestamp
            app.resultsTable{app.currentTestIndex,'Timestamp'} = {datestr(now)};
            % Image-specific variables
            app.resultsTable{app.currentTestIndex,'SetIndex'} = app.currentEntry.SetIndex;
            app.resultsTable{app.currentTestIndex,'SetName'} = app.currentEntry.SetName;
            app.resultsTable{app.currentTestIndex,'ImageIndex'} = app.currentEntry.ImageIndex;
            app.resultsTable{app.currentTestIndex,'IsComposite'} = app.currentEntry.IsComposite;
            app.resultsTable{app.currentTestIndex,'ParentIndex'} = app.currentEntry.ParentIndex;
            app.resultsTable{app.currentTestIndex,'Filename'} = app.currentEntry.Filename;
            % User-response variables
            app.resultsTable{app.currentTestIndex,'Response1'} = response1Value(app);
            if ~originalSelected(app)
                app.resultsTable{app.currentTestIndex,'Response2'} = ...
                    round(app.HowobnoxiousaretheartifactsSlider.Value);
            end
        end
        
        function writeResultsTableToFile(app)
            if exist(app.resultsfilename,'file') % a file already exists - append to it
                existingFile = readtable(app.resultsfilename);
                % if the column names match
                if isequal(existingFile.Properties.VariableNames,...
                           app.resultsTable.Properties.VariableNames)
                    combinedResults = [existingFile;app.resultsTable];
                    writetable(combinedResults,app.resultsfilename);
                else
                    idx = 1;
                    [filepath,name,ext] = fileparts(app.resultsfilename);
                    namei = [name,num2str(idx)];
                    while exist([fullfile(filepath,namei),ext],'file')
                        idx = idx+1;
                        namei = [name,num2str(idx)];
                    end
                    warning(['There is already a file at ',app.resultsfilename,...
                        ' whose columns don''t match the output format. Writing to ',...
                        fullfile(filepath,namei),ext, ' instead.']);
                    oldFilename = app.resultsfilename;
                    app.resultsfilename = [fullfile(filepath,namei),ext];
                    writeResultsTableToFile(app);
                    app.resultsfilename = oldFilename;
                end
            else % create a new file
                writetable(app.resultsTable,app.resultsfilename);
            end
        end
        
    end

    methods (Access = public)

        % Construct app
        function app = adapp
            warning('off','all');

            % Create and configure components
            createComponents(app);
            
            % Load the metadata file
            loadMetadata(app);
            
            % Run the app
            % run(app);
            
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
        
        % Run app
        function result = run(app)
            
            % Select and order the test images
            composeTest(app);
            
            % Show instruction dialog
            message = ['Judge the images. Are they unaltered "original" photos, or have they been constructed from multiple images (a "composite")? Don''t spend too much time on any one image. 20 seconds, tops.'];
            button = questdlg(message, 'Instructions', 'I''m ready', 'Quit', 'OK');
            drawnow;	% Refresh screen to get rid of dialog box remnants.
            if strcmpi(button, 'Quit')
                delete(app);
                return
            end
            
            % Ask for tester ID
            prompt = {'Enter your name:'};
            dlg_title = 'User name entry';
            num_lines = 1;
            defaultans = app.userName;
            app.userName = inputdlg(prompt,dlg_title,num_lines,defaultans);

            % Set up test to run
            app.currentTestIndex = 0;
            showNextImage(app);
            app.UIFigure.Visible = 'on';
            
            result = true;
        end
        
    end
end