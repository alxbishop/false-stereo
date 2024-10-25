### False Stereo pairs - UP42 SDK

This python program provides a way to discover false stereo pairs against Airbus satellite catalog data using the UP42 SDK. It contains two python files.
 - find_false_stereo_program.py: this file can be run using a terminal.
- find_false_stereo_notebool.ipynb: best run directly in a code editor.


The logic is as follows:
 -  step-1: check that two scenes have 80% to 100% overlap
 -  step-2: confirm they are on opposite orbits or if on the same orbit that they have opposing look angles.

Please note that this tool might also return true stereo pairs.

This tool only work with the following collections:
 - pneo
 - phr
 - spot

Search dates format are as follows:
 - "Y-M-D" '2022-01-01'

Cloud cover is a percentage:
 - 0 to 100

The results can be loaded into a GIS software. Each output geojson vector file contains the potential stereo pairs, therefore each file written should have two features in the layer.

Future next steps in you scene selection process.
 - Pull and plot quicklooksfor visual cloud validation
 - Credit cost veofr purchase

Please note this program and notebook are not being actively maintained and are not official UP42 products.

Have fun with this, best of luck! :)

Alex

