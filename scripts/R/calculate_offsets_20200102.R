# Calculate dichroic mirror offsets using data collected up to 2nd January 2020

# Data collection dates:
# 29th July 2019
# 16th December 2019
# 2nd January 2020 (5 replicates for each objective and DM combination)

# load required functions and libraries
source("E:/matt/olympus/scripts/R/lateral_offset_tools.R")
library(doParallel)

# How many cores does this computer possess?
numCores <- detectCores()

# Setup parallel processing backend
registerDoParallel(cores=numCores-2)

# get list of files
filelist <- read.csv("E:/matt/olympus/DM_offset_data/dm_offset_file_list.csv", stringsAsFactors = F)

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
saveRDS(results, file="E:/matt/olympus/DM_offset_data/results_20200102.RDS")

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

write.csv(offsetResults, "E:/matt/olympus/DM_offset_data/offsetResults_20200102.csv", row.names=F, quote=F)

offsetTable <- as.data.frame(matrix(nrow=20, ncol=4))
names(offsetTable) <- c("objective","dm","x","y")
offsetTable$objective <- rep(c("4x", "10x", "20x", "30x", "60x"), each=4)
offsetTable$dm <- rep(c("dm2", "dm3", "dm4", "dm5"), 5)

for (i in 1:dim(offsetTable)[1]){
  m <- offsetResults[offsetResults$objective==offsetTable$objective[i] & offsetResults$dm==offsetTable$dm[i],]
  offsetTable$x[i] <- mean(m$x)
  offsetTable$y[i] <- mean(m$y)
}

write.csv(offsetTable, "E:/matt/olympus/DM_offset_data/offsetTable_20200102.csv", row.names=F, quote=F)
