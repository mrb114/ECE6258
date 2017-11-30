function runIQMetrics( inputFilename, imageDir, outputFilename )
%runIQAssessment Runs FaceSwapper IQ metrics

addpath(genpath(pwd)) % Adds the current file directory and subfolders to path, assuming you're running from the directory of this file.

tbl = readtable(inputFilename);
outtbl = table();

nSets = max(tbl.SetIndex);

fprintf('Beginning processing of %d sets...\n',nSets);
for si = 1:nSets % for each set
    subTbl = tbl(tbl.SetIndex == si,:);
    nIm = max(subTbl.ImageIndex);
    for imi = 1:nIm
        % calculate characteristic metrics
        entry = subTbl(subTbl.ImageIndex == imi,:);
        theImage = imread(fullfile(imageDir,entry.Filename{:}));
        mets = computeIndividualMetrics(theImage);
        if entry.IsComposite
            % calculate pairwise metrics, too
            pii = entry.ParentIndex;
            piEntry = subTbl(subTbl.ImageIndex == pii,:);
            parentImage = imread(fullfile(imageDir,piEntry.Filename{:}));
            doubleMets = computePairwiseMetrics(parentImage,theImage);
            mets = cat(2,mets,doubleMets);
        end
        newEntry = cat(2,entry,mets);
        col1missing = setdiff(newEntry.Properties.VariableNames, outtbl.Properties.VariableNames);
        if ~isempty(col1missing)
            outtbl = cat(2,outtbl,array2table(nan(height(outtbl), numel(col1missing)), 'VariableNames', col1missing));
        end
        col2missing = setdiff(outtbl.Properties.VariableNames, newEntry.Properties.VariableNames);
        if ~isempty(col2missing)
            newEntry = cat(2,array2table(nan(height(newEntry), numel(col2missing)), 'VariableNames', col2missing),newEntry);
        end
        outtbl = cat(1,outtbl,newEntry);
        fprintf('Completed image %d of %d in set %d of %d.\n',imi,nIm,si,nSets);
    end
    fprintf('Completed image set %d of %d.\n',si,nSets);
end

writetable(outtbl,outputFilename);

end

