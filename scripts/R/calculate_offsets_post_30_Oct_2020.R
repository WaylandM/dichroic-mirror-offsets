# Calculate dichroic mirror offsets using data collected on 1st December 2020.
# Alignment of DMs was corrected on 30th October 2020.

# load required functions and libraries
source("E:/Matt/dichroic-mirror-offsets-master/scripts/R/lateral_offset_tools.R")
library(doParallel)

# How many cores does this computer possess?
numCores <- detectCores()

# Setup parallel processing backend
registerDoParallel(cores=numCores-2)

# get list of files
filelist <- read.csv("E:/Matt/dichroic-mirror-offsets-master/tables/dm_offset_file_list_20201201.csv", stringsAsFactors = F)

# define function to process each file
processFile <- function(filename){
  img <- read.image(filename)
  ch2Offset <- calculateOffsets(img=img, refImg=1, offImg=2, imgCrop=40)
  ch3Offset <- calculateOffsets(img=img, refImg=1, offImg=3, imgCrop=40)
  output <- list(ch2=ch2Offset, ch3=ch3Offset)
}

# apply processFile function in parallel
results <- foreach(i=1:dim(filelist)[1], .packages=c("EBImage", "RBioFormats", "stringr"), .inorder=T) %dopar% processFile(filelist$filepath[i])

# save results list to file
saveRDS(results, file="E:/Matt/dichroic-mirror-offsets-master/tables/results_post_20201030.RDS")

# convert results list to table
offsetResults <- as.data.frame(matrix(nrow=dim(filelist)[1]*2, ncol=5))
names(offsetResults) <- c("filepath", "objective","dm","x","y")
offsetResults$filepath <- rep(filelist$filepath, each=2)
offsetResults$objective <- rep(filelist$objective, each=2)
offsetResults$dm <- as.vector(t(filelist[,5:6]))

outIdx = 1
for (resIdx in 1:length(results)){
  offsetResults$x[outIdx] <- results[[resIdx]]$ch2[1]
  offsetResults$y[outIdx] <- results[[resIdx]]$ch2[2]
  outIdx = outIdx+1
  offsetResults$x[outIdx] <- results[[resIdx]]$ch3[1]
  offsetResults$y[outIdx] <- results[[resIdx]]$ch3[2]
  outIdx = outIdx+1
}

write.csv(offsetResults, "E:/Matt/dichroic-mirror-offsets-master/tables/offsetResults_post_20201030.csv", row.names=F, quote=F)

offsetTable <- as.data.frame(matrix(nrow=20, ncol=4))
names(offsetTable) <- c("objective","dm","x","y")
offsetTable$objective <- rep(c("4x", "10x", "20x", "30x", "60x"), each=4)
offsetTable$dm <- rep(c("dm2", "dm3", "dm4", "dm5"), 5)

for (i in 1:dim(offsetTable)[1]){
  m <- offsetResults[offsetResults$objective==offsetTable$objective[i] & offsetResults$dm==offsetTable$dm[i],]
  offsetTable$x[i] <- mean(m$x)
  offsetTable$y[i] <- mean(m$y)
}

write.csv(offsetTable, "E:/Matt/dichroic-mirror-offsets-master/tables/offsetTable_post_20201030.csv", row.names=F, quote=F)
