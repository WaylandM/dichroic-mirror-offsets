# functions for computing lateral shift
library(EBImage)
library(RBioFormats)
library(stringr)

# sum of absolute differences
sad <- function(a, b){
  sum(abs(a-b))
}

# img and template are channels from the same multicolor image and so have same dimensions
# crop - crop all four edges of template by this number of pixels
matchTemplate <- function(img, template, crop){
  dblCrop <- crop*2
  colorMode(img) <- colorMode(template) <- Grayscale
  imgDim <- dim(img)
  croppedTemplate <- template[(crop+1):(imgDim[1]-crop), (crop+1):(imgDim[2]-crop)]
  coord <- as.data.frame(cbind(rep(1:dblCrop, dblCrop), rep(1:dblCrop, each=dblCrop)))
  names(coord) <- c("x", "y")
  xAdd <- imgDim[1]-dblCrop-1
  yAdd <- imgDim[2]-dblCrop-1
  sadOutput <- sapply(1:length(coord$x), function(i){
    sad(img[coord$x[i]:(coord$x[i]+xAdd),
            coord$y[i]:(coord$y[i]+yAdd)],
        croppedTemplate)
  })
  sadOutput <- cbind(coord,sadOutput)
  names(sadOutput)[3] <- "sad"
  return(sadOutput)
}

# img = multichannel image
# refImg = index of reference image (i.e. DM1)
# offImg = index of channel offset from reference
calculateOffsets <- function(img, refImg, offImg, imgCrop){
  latOff <- matchTemplate(img[,,offImg],img[,,refImg], crop=imgCrop)
  latOff <- latOff[which.min(latOff$sad),]
  pxWidth <- globalMetadata(img)$`- Pixel Length X`
  pxWidth <- str_sub(pxWidth,str_locate(pxWidth,"\\[")[1]+1,str_locate(pxWidth,"\\]")[1]-1)
  pxWidth <- as.numeric(pxWidth)
  x <- latOff$x - imgCrop
  y <- latOff$y - imgCrop
  x <- x * pxWidth
  y <- y * pxWidth
  output <- c(x,y)
  return(output)
}