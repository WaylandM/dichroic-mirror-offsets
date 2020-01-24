# Olympus DM correction 

## Use
This ImageJ plugin corrects the alignment of channels in indvidual Olympus oir image files. For batch processing see [Olympus DM correction batch](https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/docs/batch_plugin.md).

## Example image sequence
To demonstrate use of the plugin we will take the example of the following fluoresent bead image:
![misaligned channels](img/misaligned_channels.png)

The image comprises 3 channels (captured with DMs 1-3) and six slices. The field of view was rotated through 90 degrees. Furthermore, a region of interest within the field of view was rotated through a further 90 degrees. The plugin uses a [rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix) to adjust the offsets for rotated images.

## 1. Launch plugin
**Plugins -> Zoology Imaging Facility -> Olympus DM correction**

**N.B. The Olympus oir file doesn't need to be open when you start the plugin. If you have large image files to process it is best not to have any images open in ImageJ/Fiji, to maximize the memory available to the plugin.**

## 2. Choose Olympus oir file 
On starting the plugin you will be prompted to select the Olympus oir file to be processed.
![choose olympus image file dialog](img/choose_olympus_oir_file.png)

The plugin will not make any changes to the Olympus oir file. The aligned channel images will be output as new tif files.

## 3. Match image channels to DMs
The plugin uses [BioFormats](https://www.openmicroscopy.org/bio-formats/) to extract almost all of the metadata (*e.g.* objective lens, pixel size, rotation of field of view, rotation of region of interest) it needs to process the image file. However, as far as I can tell, BioFormats doesn't report which DM was used to acquire each channel. This means we have to manually match each channel to its DM. Channels are numbered from 1 following the Olympus convention.

![match channel to DM dialog](img/match_channel_to_DM.png)

If you would like the plugin to output a single tif file containing all changes, tick the

When you have matched each channel to its DM, click **OK**. 

## 3. Choose output directory
Next you will be prompted to choose the directory into which the aligned channel images should be output.
![choose output folder dialog](img/choose_output_folder.png)

Once you have selected an output directory the oir file will be processed.

***N.B. The plugin does not display images at any stage of processing.***

## 5. Log
Progress is reported in the ImageJ/Fiji log.

![log](img/log.png)

The log reports the version of the plugin used along with details of the translation applied to each channel. To keep the log for your records, select the log window, then from the ImageJ/Fiji **File** menu choose **Save As...***.

## 6. Inspect output
Go to the directory you selected for output. Within this directory you will find a subdirectory with the same name as your Olympus oir file, but with the *.oir* extension removed:
![output folder](img/output_folder.png)

Inside the subdirectory you will find several tif files, one for each of the channels in your original Olympus oir file.
![new image files created](img/files_created.png)

Open and merge channel images in ImageJ/Fiji. All channels should be correctly aligned.

![aligned_channels](img/aligned_channels.png)
