# Plugin to align images collected using different dichroic mirrors on the Olympus FV3000
pluginVersion = "0.0.4"

from ij import IJ 
from ij.io import OpenDialog 
from ij.io import DirectoryChooser
from ij.io import FileSaver
from ij.gui import GenericDialog  
from ij.plugin import RGBStackMerge
import math
import sys
import os
from loci.plugins import BF
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.plugins.in import ImporterOptions
from ome.units import UNITS
from datetime import datetime

dichroicDict = {'DM1':1, 'DM2':2, 'DM3':3, 'DM4':4, 'DM5':5}

# lookup offset
def getOffset(obj, dm):
	if obj=="UPLFLN 4X":
		if dm==2:
			return({'x':2.1086, 'y':14.6492})
		if dm==3:
			return({'x':-2.3306, 'y':7.1026})
		if dm==4:
			return({'x':-6.2148, 'y':-13.2065})
		if dm==5:
			return({'x':-5.438, 'y':-11.6528})
	if obj=="UPLSAPO 10":
		if dm==2:
			return({'x':0.6659, 'y':5.8153})
		if dm==3:
			return({'x':-0.9322, 'y':2.7967})
		if dm==4:
			return({'x':-2.4859, 'y':-5.2826})
		if dm==5:
			return({'x':-2.0864, 'y':-4.6611})
	if obj=="UPLSAPO 20":
		if dm==2:
			return({'x':0.3773, 'y':2.9076})
		if dm==3:
			return({'x':-0.4661, 'y':1.3983})
		if dm==4:
			return({'x':-1.243, 'y':-2.6413})
		if dm==5:
			return({'x':-1.0654, 'y':-2.3306})
	if obj=="UPLSAPO 30":
		if dm==2:
			return({'x':0.2338, 'y':1.8792})
		if dm==3:
			return({'x':-0.3167, 'y':0.9145})
		if dm==4:
			return({'x':-0.8286, 'y':-1.7786})
		if dm==5:
			return({'x':-0.7073, 'y':-1.5596})
	if obj=="UPLSAPO 60":
		if dm==2:
			return({'x':0.1381, 'y':0.9667})
		if dm==3:
			return({'x':-0.1381, 'y':0.4735})
		if dm==4:
			return({'x':-0.4143, 'y':-0.8977})
		if dm==5:
			return({'x':-0.3453, 'y':-0.7596})

# rotate offset (https://en.wikipedia.org/wiki/Rotation_matrix)
def rotateOffset(x,y,angle):
	angle = angle * math.pi/180
	x1 = x*math.cos(angle) - y*math.sin(angle)
	y1 = x*math.sin(angle) + y*math.cos(angle)
	return({'x':x1, 'y':y1})

# extract channel from oir file
def extractChannel(oirFile, ch):
	options = ImporterOptions()
	options.setColorMode(ImporterOptions.COLOR_MODE_GRAYSCALE)
	options.setId(oirFile)
	options.setCBegin(0, ch)
	options.setCEnd(0, ch)  
	#options.setSeriesOn(1,True)
	imps = BF.openImagePlus(options)
	ip = imps[0]
	return(ip)

def readSingleChannelImg(imgFile):
	options = ImporterOptions()
	options.setColorMode(ImporterOptions.COLOR_MODE_GRAYSCALE)
	options.setId(imgFile)
	imps = BF.openImagePlus(options)
	ip = imps[0]
	return(ip)

# function for processing an Olympus oir file
def processFile():
	# start logging
	IJ.log("\n______________________________\n\n\t\tOlympus DM correction\n\t\tVersion " + pluginVersion +"\n______________________________\n")

	# ask user for file
	ofd = OpenDialog("Choose a file", None)  
	filename = ofd.getFileName()  
  
	if filename is None:  
  		IJ.log("User canceled the dialog!\nImage processing canceled!\n")
  		return

  	directory = ofd.getDirectory()  
  	filepath = directory + filename  
  	IJ.log("File path: " + filepath)

	if not filename.endswith(".oir"):
		IJ.log("Not an Olympus (.oir) file.\nNo image to process.\n")
		return

	filenameExExt = os.path.splitext(filename)[0]
      
	# parse metadata
	reader = ImageReader()
	omeMeta = MetadataTools.createOMEXMLMetadata()
	reader.setMetadataStore(omeMeta)
	reader.setId(filepath)
	numChannels = reader.getSizeC()
	numSlices = reader.getSizeZ()
	numFrames = reader.getSizeT()
	seriesCount = reader.getSeriesCount()

	globalMetadata = reader.getGlobalMetadata()
	seriesMetadata = reader.getSeriesMetadata()

	objLensName = globalMetadata['- Objective Lens name #1']

	areaRotation = float(seriesMetadata['area rotation #1'])
	acquisitionValueRotation = float(seriesMetadata['acquisitionValue rotation #1'])
	if 'regionInfo rotation #1' in seriesMetadata:
		regionInfoRotation = float(seriesMetadata['regionInfo rotation #1'])
	else:
		regionInfoRotation = float(0)

	totalRotation = areaRotation + regionInfoRotation
	physSizeX = omeMeta.getPixelsPhysicalSizeX(0)
	physSizeY = omeMeta.getPixelsPhysicalSizeY(0)
	pxSizeX = physSizeX.value(UNITS.MICROM)
	pxSizeY = physSizeY.value(UNITS.MICROM)

	# log metadata
	IJ.log("\nMETADATA")
	#IJ.log("Filename: " + filepath)
	IJ.log("Number of series: " + str(seriesCount))
	IJ.log("Number of channels: " + str(numChannels))
	IJ.log("Number of frames: " + str(numFrames))
	IJ.log("Number of slices: " + str(numSlices))
	IJ.log("Objective lens: " + objLensName)
	IJ.log("FOV rotation: " + str(areaRotation))
	IJ.log("ROI rotation: " + str(regionInfoRotation))
	IJ.log("Total rotation: " + str(totalRotation))
	IJ.log("Pixel size:")
	IJ.log("\t\tX = " + str(physSizeX.value()) + " " + physSizeX.unit().getSymbol())
	IJ.log("\t\tY = " + str(physSizeY.value()) + " " + physSizeY.unit().getSymbol())

	# ask user to identify dichroic mirror used for each channel  
	gdDM = GenericDialog("Dichroic mirrors")
	DMs = ["DM1", "DM2", "DM3", "DM4", "DM5"] 
	for i in range(numChannels):
		gdDM.addChoice("Channel " + str(i+1), DMs, DMs[0])
	gdDM.addCheckbox("Merge channels", False) 
	gdDM.showDialog()
	if gdDM.wasCanceled():
		IJ.log("User canceled the dialog!\nImage processing canceled!\n")
		return
	dichroics = []
	for i in range(numChannels):
		dichroics.append(gdDM.getNextChoice())
	merge = gdDM.getNextBoolean()
	IJ.log("\nUser selected dichroic mirrors")
	for i in range(numChannels):
		IJ.log("\t\tChannel " + str(i+1) + ": " + dichroics[i])	

	if merge:
		channels = []
		chDict = {}
		for i in range(numChannels):
			chName = "Channel"+str(i+1)
			channels.append(chName)
			chDict[chName] = i
		channels.append("NONE")
		colourChoices = ["red", "green", "blue", "gray", "cyan", "magenta", "yellow"]
		gdMerge = GenericDialog("Merge channels")
		for c in colourChoices:
			gdMerge.addChoice(c + ":", channels, channels[numChannels])
		gdMerge.showDialog()
		if gdMerge.wasCanceled():
			IJ.log("User canceled the dialog!\nImage processing canceled!\n")
			return
		IJ.log("\nUser selected channel colours")
		mergeList = []
		for i in range(len(colourChoices)):
			ch = gdMerge.getNextChoice()
			if ch == "NONE":
				mergeList.append(None)
			else:
				mergeList.append(chDict[ch])
				IJ.log("\t\t" + colourChoices[i] + ": " + ch)

	# ask user for an output directory
	dc = DirectoryChooser("Choose folder for output")  
	od = dc.getDirectory()    
	if od is None:  
		IJ.log("User canceled the dialog!\nImage processing canceled!\n")  
		return  
  
	if merge:
		tifDir = od + "." + str(datetime.now()).replace(" ", "").replace(":", "") + "/"
		if not os.path.exists(tifDir):
			os.makedirs(tifDir)
			IJ.log("\nCreated temporary folder: " + tifDir + "\n")
		else:
			IJ.log("Unable to create temporary folder!\n")
	else:
		tifDir = od + filenameExExt + "/"
		if not os.path.exists(tifDir):
			os.makedirs(tifDir)
			IJ.log("\nCreated subfolder: " + tifDir + "\n")
		else:
			IJ.log("\nSubfolder " + tifDir +  " already exists")

	# correct images
	tifFilePaths = []
	for i in range(numChannels):
		ip = extractChannel(oirFile=filepath, ch=i)
		if dichroics[i] == "DM1":
			IJ.log("Channel " + str(i+1) + " was imaged using DM1, so no correction required.")
		else:
			offsets = getOffset(obj=objLensName,dm=dichroicDict[dichroics[i]])
			xom = offsets['x']
			yom = offsets['y']
			if abs(totalRotation) > 0.1:
				rotOff = rotateOffset(x=xom, y=yom, angle=-totalRotation)
				xom = rotOff['x']
				yom = rotOff['y']
			xop = int(round(xom/pxSizeX))
			yop = int(round(yom/pxSizeY))
			IJ.log("Channel " + str(i+1) + " offsets")
			IJ.log("\t\tMicrometres")
			IJ.log("\t\t\t\tx = " + str(xom))
			IJ.log("\t\t\t\ty = " + str(yom))
			IJ.log("\t\tPixels")
			IJ.log("\t\t\t\tx = " + str(xop))
			IJ.log("\t\t\t\ty = " + str(yop))
			IJ.run(ip, "Translate...", "x=" + str(-xop) + " y=" + str(-yop) + " interpolation=None stack")

		tifFilePath = tifDir + filenameExExt + "_ch_"+str(i+1)+".tif"
		tifFilePaths.append(tifFilePath)
		if os.path.exists(tifFilePath):
			IJ.log("\nOutput file exists: " + tifFilePath)
			IJ.log("Rerun plugin choosing a different output folder")
			IJ.log("or delete file and then rerun plugin.")
			IJ.log("Image processing terminated!\n")
			return
		FileSaver(ip).saveAsTiff(tifFilePath)

	if merge:
		for i in range(len(mergeList)):
			if mergeList[i] != None:
				mergeList[i] = readSingleChannelImg(tifFilePaths[mergeList[i]])
		merged = RGBStackMerge.mergeChannels(mergeList, False)
		mergedChannelFilepath = od + filenameExExt + ".tif"
		if os.path.exists(mergedChannelFilepath):
			IJ.log("\nOutput file exists: " + mergedChannelFilepath)
			IJ.log("Rerun plugin choosing a different output folder")
			IJ.log("or delete file and then rerun plugin.")
			IJ.log("Image processing terminated!\n")
		FileSaver(merged).saveAsTiff(mergedChannelFilepath)
		for tf in tifFilePaths:
			os.remove(tf)
		os.rmdir(tifDir)
			
	IJ.log("\nFinished processing file:\n" + filepath + "\n")
	if merge:
		IJ.log("Image file with channels aligned:\n" + od + filenameExExt + ".tif\n")
	else:
		IJ.log("Aligned images (one tiff file for each channel) can be found in:\n" + tifDir + "\n")

processFile()
