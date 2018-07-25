close all
clear all
clc

filename = 'C:\Users\KarlP\Documents\IR\Tiffs\Vids\test3pi.tiff';

file_info=imfinfo(filename);

numOfFrames=length(file_info);
Im = squeeze(double(imread(filename,[1:numOfFrames])));
%comment out this line if tiff file has proper dimensions
Im = permute(Im,[3,1,2]);
numOfFrames = size(Im,3);
Im = Im./100 - 273.15;

for i=1:9%numOfFrames
  figure('visible','off');
  colormap(jet);
  image(Im(:,:,i),'CDataMapping','scaled');
  maxVal = max(max(Im(:,:,i)));
  minVal = max(max(Im(:,:,i)));
  %[x,y]=find(Im(:,:,i)==maxVal);
  %text((y + 3),x,num2str(maxVal));
  text(0,-5,['Max Temp: ', num2str(maxVal), ' C']);
  xlabel('Pixel Count Horizontal');
  ylabel('Pixel Count Vertical');
  h = colorbar;
  title(h,'Celsius');
  set(gca,'clim',[20 100]);
  print(sprintf("C:/Users/KarlP/Documents/IR/output4/%05d.png",i));
  fprintf('Frame %1.0f of %4.0f\n',i,numOfFrames);
end

system("ffmpeg -framerate 9 -i C:/Users/KarlP/Documents/IR/output4/%05d.png -y -framerate 9 C:/Users/KarlP/Documents/IR/output4/movie.avi");
system("C:/Users/KarlP/Documents/IR/output4/movie.avi");