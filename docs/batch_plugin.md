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

## 5. Choose colour for each channel

## 6. Choose output directory

## 7. Log

## 8. Inspect output

