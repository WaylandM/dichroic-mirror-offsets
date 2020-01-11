# Measurement of dichroic mirror offsets

CALCULATION OF OFFSETS

All images, associated data and R scripts can be found in:
https://www.dropbox.com/sh/gpkpwprc5z501oc/AACEOOcWMWLTbZL-wso4zSZqa?dl=0

1. Image acquisition

Images of fluorescent microspheres (beads) were acquired using 
sequential scans using the 405nm laser and each objective in turn. Two 
sequential scan configurations were used: (i) DMs 1, 2 and 3; (ii) DMs 
1, 4 and 5. For further information on imaging parameters, please 
consult image file metadata.

| Date | DOI |
|---|---|
| 2019-07-29 | https://doi.org/10.6084/m9.figshare.11512338.v1 |
| 2019-12-16 | https://doi.org/10.6084/m9.figshare.11512431.v1 |
| 2020-01-02 | https://doi.org/10.6084/m9.figshare.11512452.v1 |

2. Object detection

In Fiji (ImageJ) I used the "3D objects counter" to detect the beads and 
report their coordinates (centroids).


3. Offset calculation

R was used to calculate offsets between pairs of beads (see R scripts 
for details).

