# Measurement of dichroic mirror (DM) offsets

## Image acquisition

Images of fluorescent microspheres (beads) were acquired using sequential scans using the 405nm laser and each objective in turn. Two sequential scan configurations were used: (i) DMs 1, 2 and 3; (ii) DMs 1, 4 and 5. Images were saved in Olympus oir format (one file per sequential scan). For further information on imaging parameters, please consult image file metadata.

All images used to measure DM offsets are available on figshare.

| Date | DOI |
|---|---|
| 2019-07-29 | https://doi.org/10.6084/m9.figshare.11512338.v1 |
| 2019-12-16 | https://doi.org/10.6084/m9.figshare.11512431.v1 |
| 2020-01-02 | https://doi.org/10.6084/m9.figshare.11512452.v1 |


## Lateral offset calculation

The image acquired using DM1 was treated as the reference. Lateral offsets of the images acquired using other mirrors are relative to DM1. Lateral offset was computed using the template matching method:

1. The image from DM1 is used as the reference.
2. The image whose offset is to be measured is cropped to create a template.
3. The template is slid over the reference image and its similarity to the patch of the reference image it covers is quantified using the sum of absolute differences (SAD) (https://en.wikipedia.org/wiki/Sum_of_absolute_differences).
4. Once the region of the reference image that is the best match to the template has been identified, the offset in pixels can easily be calculated.
5. Offset is converted from pixels to micrometres using pixel size information provided in Olympus oir file metadata.

For more details of lateral offset calculations please see the R scripts:
https://github.com/WaylandM/dichroic-mirror-offsets/tree/master/scripts/R

Functions implementing SAD, template matching and calculation of offsets are provided by the following R script:
https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/scripts/R/lateral_offset_tools.R

R script used to process all image files collected to date:
https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/scripts/R/calculate_offsets_20200102.R


## Data

### Full data set
All lateral offset measurements collected to date can be found in the following table:
https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/tables/offsetResults_20200102.csv

### Offsets used for correcting alignment of channels
Average offsets for each DM and objective combination can be found in the following table:
https://github.com/WaylandM/dichroic-mirror-offsets/blob/master/tables/offsetTable_20200102.csv

These average offsets are used for correcting the alignment of channels collected using different DMs.

