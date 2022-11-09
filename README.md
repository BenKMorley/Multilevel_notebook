This notebook lays out the code used for an investigation into the effect of the correlation
length on the performance of the multilevel algorithm. This investigation was presented at the
annual lattice physics conference (https://indico.cern.ch/event/1006302/contributions/4381218/) with the proceedings published here: https://doi.org/10.22323/1.396.0133. This research is described in the (in preparation at the time of writing) thesis of Ben Kitching-Morley.

To use this notebook, one needs to change the line in the second cell

base_directory = ""

to an appropriate directory in the users system where the data produced by this notebook will be reproduced if you re-run the code.

To avoid the run-time costs (~1-2 days for single threaded) of generating the configurations, extract the "data" folder from this DOI 10.5281/zenodo.7303520 into the base_directory folder.

All the figures of the notebook are already produced in the output cells, so the user can choose to simply read the notebook if they wish.

Code Author:
------------
Ben Kitching-Morley

Project Authors:
----------------
Ben Kitching-Morley  \
Andreas Jüttner
