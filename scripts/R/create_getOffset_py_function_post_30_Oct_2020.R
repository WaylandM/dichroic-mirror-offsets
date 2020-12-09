# create python function to output lateral offset for a particular DM and objective lens combination
library(stringr)

# python script name
py_script_filename <- "E:/Matt/dichroic-mirror-offsets-master/scripts/py/lateral_offset_lookup_post_20201030.py"

# read table containing lateral offset data
offsetTable <- read.csv("E:/Matt/dichroic-mirror-offsets-master/tables/offsetTable_post_20201030.csv", stringsAsFactors = F)

objLens <- as.data.frame(cbind(c("4x", "10x", "20x", "30x", "60x"), c("UPLFLN 4X","UPLSAPO 10","UPLSAPO 20","UPLSAPO 30","UPLSAPO 60")))
names(objLens) <- c("short", "long")

fileConn<-file(py_script_filename, open="wt")

writeLines("# lookup offset", fileConn)
writeLines(c('def getOffset(obj, dm):'), fileConn)

for (i in 1:length(objLens$short)){
  m <- offsetTable[offsetTable$objective==objLens$short[i],]
  writeLines(str_c('\tif obj=="',objLens$long[i],'":'), fileConn)
  for (j in 1:length(m$objective)){
    writeLines(str_c('\t\tif dm==',j+1,':'), fileConn)
    writeLines(str_c("\t\t\treturn({'x':", format(round(m$x[j], digits=4), scientific=F), ", 'y':", format(round(m$y[j], digits=4), scientific=F), "})"), fileConn)
  }
}

close(fileConn)
