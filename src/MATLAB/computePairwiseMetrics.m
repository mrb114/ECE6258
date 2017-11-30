function [ tableOut ] = computePairwiseMetrics( im1, im2 )
%computePairwiseMetrics Computes objective image quality metrics for a pair of images.

% MSE
mserr = immse(im1,im2);

% PSNR
[psnrval,snrval] = psnr(im1,im2);

% SSIM
[ssimval,ssimmap] = ssim(im1,im2);

% UNIQUE
uniqueval = mslUNIQUE(im1,im2);

% MS-UNIQUE
msuniqueval = mslMSUNIQUE(im1,im2);

%% Build results table
tableOut = table();
tableOut.mse = mserr;
tableOut.psnr = psnrval;
tableOut.snr = snrval;
tableOut.ssim = ssimval;
tableOut.unique = uniqueval;
tableOut.msunique = msuniqueval;

end

