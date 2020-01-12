# Olympus DM correction: ImageJ plugin

**N.B. This plugin requires the BioFormats plugins (https://imagej.net/Bio-Formats)**

[Fiji](https://imagej.net/Fiji) comes with the BioFormats plugins pre-installed. If you are using regular [ImageJ](https://imagej.net) you will need to install the BioFormats plugins (see https://docs.openmicroscopy.org/bio-formats/5.8.2/users/imagej/installing.html).

## Installation
1. Close ImageJ/Fiji

2. Download zip file: [zoo_img_fac_plugins.zip](https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/fiji_plugins/zoo_img_fac_plugins.zip?raw=true)

3. Unzip zoo_img_fac_plugins.zip to the plugins directory of ImageJ/Fiji.

When you restart ImageJ/Fiji you should see **Olympus DM correction** on the plugins menu under **Zoology Imaging Facility**:
![screenshot of plugins menu](img/plugin_menu_item.png)

## Use

### Example image sequence
To demonstrate use of the plugin we will take the example of the following fluoresent bead image:
![misaligned channels](img/misaligned_channels.png)

The image comprises 3 channels (captured with DMs 1-3) and six slices. The field of view was rotated through 90 degrees. Furthermore, a region of interest within the field of view was rotated through a further 90 degrees. The plugin uses a [rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix) to adjust the offsets for rotated images.

### 1. Launch plugin
**Plugins -> Zoology Imaging Facility -> Olympus DM correction**

**N.B. The Olympus oir file doesn't need to be open when you start the plugin. If you have large image files to process it is best not to have any images open in ImageJ/Fiji, to maximize the memory available to the plugin.**

### 2. Choose Olympus oir file 
On starting the plugin you will be prompted to select the Olympus oir file to be processed.
![choose olympus image file dialog](img/choose_olympus_oir_file.png)

The plugin will not make any changes to the Olympus oir file. The aligned channel images will be output as new tif files.

### 3. Choose output directory
Next you will be prompted to choose the directory into which the aligned channel images should be output.
![choose output folder dialog](img/choose_output_folder.png)

### 4. Match image channels to DMs
The plugin uses [BioFormats](https://www.openmicroscopy.org/bio-formats/) to extract almost all of the metadata (*e.g.* objective lens, pixel size, rotation of field of view, rotation of region of interest) it needs to process the image file. However, as far as I can tell, BioFormats doesn't report which DM was used to acquire each channel. This means we have to manually match each channel to its DM. Channels are numbered from 1 following the Olympus convention.

![match channel to DM dialog](img/match_channel_to_DM.png)

When you have matched each channel to its DM, click **OK**. 

**N.B. The plugin does not display images at any stage of processing.**

### 5. Log
Progress is reported in the ImageJ/Fiji log.

![log](img/log.png)

The log reports the version of the plugin used along with details of the translation applied to each channel. To keep the log for your records, select the log window, then from the ImageJ/Fiji **File** menu choose **Save As...***.

### 6. Inspect output
Go to the directory you selected for output. Within this directory you will find a subdirectory with the same name as your Olympus oir file, but with the *.oir* extension removed:
![output folder](img/output_folder.png)

Inside the subdirectory you will find several tif files, one for each of the channels in your original Olympus oir file.
![new image files created](img/files_created.png)

Open and merge channel images in ImageJ/Fiji. All channels should be correctly aligned.

![aligned_channels](img/aligned_channels.png)

## Test data
Image data used to test this plugin are available on figshare:

| Date | DOI |
|---|---|
| 2019-07-25 | https://doi.org/10.6084/m9.figshare.11586930.v1 |
| 2020-01-02 | https://doi.org/10.6084/m9.figshare.11586984.v1 |
