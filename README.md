# ragali_prototype

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cchwala/ragali_prototype/main)

`ragali` should make it easy to handle and plot data from weather radar, rain gauges (also PWS) and links (CML and SML). Main features should be:
* plot data on map (including a simple way to plot lines with a colormap)
* find neigbhouring or intersecting sensor data
* do standard validation of results
* use `xarray.Dataset` as data model throughout all functions
* enforce the usage of [OPENSENSE data format conventions](https://github.com/OpenSenseAction/OS_data_format_conventions) and provide a function to check these
* basic uncertainty estimation method e.g. via cross-validation of reference gauges


Important notes:
* This is a early prototype of potential functions of `ragali`. There might be errors in the code and naming of functions and variables might change later.
* Current implementations are focused mostly on CMLs because plotting lines is not as easy as plotting points and because getting radar values along CMLs is harder then getting radar values at a certain point.
