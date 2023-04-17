# Olympus DM correction batch

## Purpose
This ImageJ plugin corrects the alignment of channels in Olympus oir files. It can process batches in which all images were acquired using the same combination of dichroic mirrors. Individual files can be processed using [Olympus DM correction](https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/docs/single_file_plugin.md).

## 1. Preparation
**Please note the following prerequisites for batch processing:**

* **All image files in a batch must contain the same number of channels.**
* **The same combination of dichroic mirrors should have been used to acquire all images in the batch.**

The batch of Olympus oir files should be placed in the same directory. There should be no other oir files in this directory.

![input folder](img/batch_input_folder.png)

## 2. Launch plugin
**Plugins -> Zoology Imaging Facility -> Olympus DM correction**

N.B. If you have large image files to process it is best not to have any images open in ImageJ/Fiji, to maximize the memory available to the plugin.

## 3. Choose directory containing Olympus oir files
On starting the plugin you will be prompted to select the folder containing the batch of Olympus oir files. The plugin will process all oir files in this directory. Files without the **.oir** extension will be ignored.

![choose input folder](img/batch_choose_input_folder.png)

## 4. Match image channels to DMs
The plugin uses [BioFormats](https://www.openmicroscopy.org/bio-formats/) to extract almost all of the metadata (*e.g.* objective lens, pixel size, rotation of field of view, rotation of region of interest) it needs to process the image file. However, as far as I can tell, BioFormats doesn't report which DM was used to acquire each channel. This means we have to manually match each channel to its DM. Channels are numbered from 1 following the Olympus convention.

![match channel to DM dialog](img/match_channel_to_DM.png)

The channel and DM pairings specified here will be used in the processing of all images. This is why it is essential that all images in the batch have been acquired using the same combination of DMs.

If you would like composite files to be output (*i.e.* files containing all channels), tick the **Merge channels** checkbox. Otherwise the plugin will output one tif file per channel, for each of the Olympus oir files.

**Lateral offsets changed on 30th October 2020 when the dichroic mirrors were realigned. Please ensure that you specify when your images were acquired by checking the appropriate radio button.**

Click **OK** to proceed.


## 5. Choose colour for each channel
If you asked the plugin to output a composite image, by ticking the **Merge channels** checkbox in the previous dialog, you will be prompted to select a lookup table (LUT) colour for each channel.

![merge channels](img/merge_channels.png)

Match each of your channels to one of the seven available colours and then click **OK**.

## 6. Choose output directory
Next you will be prompted to choose the directory into which the aligned channel images should be output.
![choose output folder dialog](img/choose_output_folder.png)

Once you have selected an output directory, all oir files in the batch will be processed, using the settings defined in the preceding steps.

***N.B. The plugin does not display images at any stage of processing.***


## 7. Log
Progress is reported in the ImageJ/Fiji log.

![log](img/batch_log.png)

The log reports the version of the plugin and provides a summary of each file processed, including the translation applied to each channel. The log is updated as each oir file is processed and so it is useful for monitoring the progress of long running jobs.

To keep the log for your records, select the log window, then from the ImageJ/Fiji **File** menu choose **Save As...***.



## 8. Inspect output
Go to the directory you selected for output.
### Composite images
If you chose the **Merge channels** option a composite tif file (containing all channels) will be output for each Olympus oir file.
![output directory](img/batch_output_directory.png)

### File for each channel
If you opted not to merge channels into a composite file you will find one directory for each Olympus oir file.
![output directory no merge](img/batch_output_directory_no_merge.png)

Within each of these directories are the tif files for each channel.
![output subdirectory no merge](img/batch_output_subdirectory_no_merge.png)

