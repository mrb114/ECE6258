function [ tableOut ] = computeIndividualMetrics( im )
%computeIndividualMetrics computes image characteristic metrics for a single image

% Contrast (as a percentage of dynamic range)
cval = max(im(:))-min(im(:));

% Entropy 
E = entropy(im);
% 

%% Build results table
tableOut = table();
tableOut.contrast = cval;
tableOut.entropy = E;


end

