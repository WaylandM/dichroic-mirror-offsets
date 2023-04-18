# Plugin to align images collected using different dichroic mirrors on the Olympus FV3000
pluginVersion = "0.0.6"

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
dateOptions = ["2nd Jan 2020", "30th Oct 2020", "22nd Mar 2023"]  

# lookup offset for images collected before 30th October 2020
def getOffset0(obj, dm):
	if obj=="UPLFLN 4X":
		if dm==2:
			return({'x':1.3317, 'y':13.8723})
		if dm==3:
			return({'x':-3.1074, 'y':6.3258})
		if dm==4:
			return({'x':-6.9917, 'y':-13.9833})
		if dm==5:
			return({'x':-6.2148, 'y':-12.4296})
	if obj=="UPLSAPO 10":
		if dm==2:
			return({'x':0.3551, 'y':5.5045})
		if dm==3:
			return({'x':-1.243, 'y':2.4859})
		if dm==4:
			return({'x':-2.7967, 'y':-5.5933})
		if dm==5:
			return({'x':-2.3971, 'y':-4.9718})
	if obj=="UPLSAPO 20":
		if dm==2:
			return({'x':0.222, 'y':2.7523})
		if dm==3:
			return({'x':-0.6215, 'y':1.243})
		if dm==4:
			return({'x':-1.3983, 'y':-2.7967})
		if dm==5:
			return({'x':-1.2208, 'y':-2.4859})
	if obj=="UPLSAPO 30":
		if dm==2:
			return({'x':0.1361, 'y':1.7816})
		if dm==3:
			return({'x':-0.4143, 'y':0.8168})
		if dm==4:
			return({'x':-0.9263, 'y':-1.8763})
		if dm==5:
			return({'x':-0.805, 'y':-1.6573})
	if obj=="UPLSAPO 60":
		if dm==2:
			return({'x':0.0691, 'y':0.8977})
		if dm==3:
			return({'x':-0.2072, 'y':0.4045})
		if dm==4:
			return({'x':-0.4834, 'y':-0.9667})
		if dm==5:
			return({'x':-0.4143, 'y':-0.8286})

# lookup offset for images collected after 30th October 2020
def getOffset1(obj, dm):
	if obj=="UPLSAPO 4X":
		if dm==2:
			return({'x':0.6215, 'y':3.7289})
		if dm==3:
			return({'x':5.9041, 'y':-5.438})
		if dm==4:
			return({'x':-0.3107, 'y':1.5537})
		if dm==5:
			return({'x':0.7769, 'y':3.1074})
	if obj=="UPLSAPO 10":
		if dm==2:
			return({'x':0.3729, 'y':1.4916})
		if dm==3:
			return({'x':2.5481, 'y':-2.2995})
		if dm==4:
			return({'x':0.3107, 'y':0.6215})
		if dm==5:
			return({'x':0.6215, 'y':1.243})
	if obj=="UPLSAPO 20":
		if dm==2:
			return({'x':0.0259, 'y':0.6474})
		if dm==3:
			return({'x':1.243, 'y':-1.2171})
		if dm==4:
			return({'x':0, 'y':0.3107})
		if dm==5:
			return({'x':0.1554, 'y':0.6215})
	if obj=="UPLSAPO 30":
		if dm==2:
			return({'x':0.0414, 'y':0.5179})
		if dm==3:
			return({'x':0.8286, 'y':-0.7458})
		if dm==4:
			return({'x':0, 'y':0.1864})
		if dm==5:
			return({'x':0.1036, 'y':0.4143})
	if obj=="UPLSAPO 60":
		if dm==2:
			return({'x':0.0276, 'y':0.2624})
		if dm==3:
			return({'x':0.4143, 'y':-0.4005})
		if dm==4:
			return({'x':0, 'y':0.0829})
		if dm==5:
			return({'x':0.0691, 'y':0.2072})

# lookup offset for images collected around March 2023
def getOffset2(obj, dm):
	if obj=="UPLSAPO 4X":
		if dm==2:
			return({'x':0.7769, 'y':3.1074})
		if dm==3:
			return({'x':0.7769, 'y':0.7769})
		if dm==4:
			return({'x':0, 'y':0.7769})
		if dm==5:
			return({'x':0.3107, 'y':2.3306})
	if obj=="UPLSAPO 10":
		if dm==2:
			return({'x':0.0621, 'y':0.9944})
		if dm==3:
			return({'x':0.4972, 'y':0.1243})
		if dm==4:
			return({'x':0, 'y':0.3107})
		if dm==5:
			return({'x':0.2486, 'y':0.9322})
	if obj=="UPLSAPO 20":
		if dm==2:
			return({'x':0.0621, 'y':0.4661})
		if dm==3:
			return({'x':0.1554, 'y':0.1554})
		if dm==4:
			return({'x':0, 'y':0.1554})
		if dm==5:
			return({'x':0.0932, 'y':0.4661})
	if obj=="UPLSAPO 30":
		if dm==2:
			return({'x':0.0414, 'y':0.3315})
		if dm==3:
			return({'x':0.1036, 'y':0.1036})
		if dm==4:
			return({'x':0, 'y':0.1036})
		if dm==5:
			return({'x':0, 'y':0.3107})
	if obj=="UPLSAPO 60":
		if dm==2:
			return({'x':0.0138, 'y':0.1795})
		if dm==3:
			return({'x':0.0552, 'y':0.0691})
		if dm==4:
			return({'x':-0.0138, 'y':0.0552})
		if dm==5:
			return({'x':0.0138, 'y':0.1381})

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
def processFile(filename, inDir, outDir, dichroics, mergeList, collectionDate):

	if mergeList is None:
		merge = False
	else:
		merge = True
	
	filenameExExt = os.path.splitext(filename)[0]
	filepath = inDir + filename
      
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

	objLensName = globalMetadata['- Objective Lens name']

	areaRotation = float(seriesMetadata['area rotation'])
	acquisitionValueRotation = float(seriesMetadata['acquisitionValue rotation'])
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
  
	if merge:
		tifDir = outDir + "." + str(datetime.now()).replace(" ", "").replace(":", "") + "/"
		if not os.path.exists(tifDir):
			os.makedirs(tifDir)
			IJ.log("\nCreated temporary folder: " + tifDir + "\n")
		else:
			IJ.log("Unable to create temporary folder!\n")
	else:
		tifDir = outDir + filenameExExt + "/"
		if not os.path.exists(tifDir):
			os.makedirs(tifDir)
			IJ.log("\nCreated subfolder: " + tifDir + "\n")
		else:
			IJ.log("\nSubfolder " + tifDir +  " already exists.\n")

	# correct images
	tifFilePaths = []
	for i in range(numChannels):
		ip = extractChannel(oirFile=filepath, ch=i)
		if dichroics[i] == "DM1":
			IJ.log("Channel " + str(i+1) + " was imaged using DM1, so no correction required.")
		else:
			if collectionDate == dateOptions[0]:
				offsets = getOffset0(obj=objLensName,dm=dichroicDict[dichroics[i]])
			elif collectionDate == dateOptions[1]:
				offsets = getOffset1(obj=objLensName,dm=dichroicDict[dichroics[i]])
			else:
				offsets = getOffset2(obj=objLensName,dm=dichroicDict[dichroics[i]])
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
		mergedChannelFilepath = outDir + filenameExExt + ".tif"
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
		IJ.log("Image file with channels aligned:\n" + outDir + filenameExExt + ".tif\n")
	else:
		IJ.log("Aligned images (one tiff file for each channel) can be found in:\n" + tifDir + "\n")


def processDirectory():
	# start logging
	IJ.log("\n______________________________\n\n\t\tOlympus DM correction\n\t\tVersion " + pluginVersion +"\n______________________________\n")

	# ask user for an input directory
	dc = DirectoryChooser("Choose folder containing Olympus (.oir) files")  
	inputDir = dc.getDirectory() 
	if inputDir is None:  
		IJ.log("User canceled the dialog!\nImage processing canceled!\n")  
		return  
	IJ.log("\nInput directory: " + inputDir + "\n")

	oirFiles = []
	for f in os.listdir(inputDir):
		if f.endswith(".oir"):
			oirFiles.append(f)

	if len(oirFiles) < 1:
		IJ.log("Input directory does not contain any Olympus (.oir) files.\nNo images to process.\n")
		return
  	
	# find out how many channels are in first file (we will assume all files have same number of channels and were acquired using same DMs)
	reader = ImageReader()
	omeMeta = MetadataTools.createOMEXMLMetadata()
	reader.setMetadataStore(omeMeta)
	reader.setId(inputDir + oirFiles[0])
	numChannels = reader.getSizeC()

	# ask user to identify dichroic mirror used for each channel  
	gdDM = GenericDialog("Dichroic mirrors")
	DMs = ["DM1", "DM2", "DM3", "DM4", "DM5"] 
	for i in range(numChannels):
		gdDM.addChoice("Channel " + str(i+1), DMs, DMs[0])
	gdDM.addCheckbox("Merge channels", False) 
	gdDM.addRadioButtonGroup("Offset data collected:", dateOptions, 3, 1, "22nd Mar 2023")
	gdDM.showDialog()
	if gdDM.wasCanceled():
		IJ.log("User canceled the dialog!\nImage processing canceled!\n")
		return
	dichroics = []
	for i in range(numChannels):
		dichroics.append(gdDM.getNextChoice())
	merge = gdDM.getNextBoolean()
	collectionDate = gdDM.getNextRadioButton()
	IJ.log("\n\nImages collected " + collectionDate + ".\n")
	IJ.log("\nUser selected dichroic mirrors")
	for i in range(numChannels):
		IJ.log("\t\tChannel " + str(i+1) + ": " + dichroics[i])	
	IJ.log("\n")


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
		IJ.log("User selected channel colours")
		usersMergeList = []
		for i in range(len(colourChoices)):
			ch = gdMerge.getNextChoice()
			if ch == "NONE":
				usersMergeList.append(None)
			else:
				usersMergeList.append(chDict[ch])
				IJ.log("\t\t" + colourChoices[i] + ": " + ch)
		IJ.log("\n\n")

	# ask user for an output directory
	dc = DirectoryChooser("Choose folder for output")  
	outputDir = dc.getDirectory()    
	if outputDir is None:  
		IJ.log("User canceled the dialog!\nImage processing canceled!\n")  
		return  

	counter = 0
	totalFiles = len(oirFiles)
	for o in oirFiles:
		counter +=1
		IJ.log("Processing file " + str(counter) + " of " + str(totalFiles) + "\n")
		IJ.log("File path: " + inputDir + o)
		if merge:
			ml = usersMergeList[:]
		else:
			ml = None
		processFile(o, inputDir, outputDir, dichroics, ml, collectionDate)
		IJ.log("\n--------------------------\n")
	
processDirectory()
