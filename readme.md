### False Stereo pairs - UP42 SDK

This python program provides a way to discover false stereo pairs against Airbus satellite catalog data using the UP42 SDK. It contains two python files.
 - The program only run on geojson vector files as input
 - find_false_stereo_program.py : 
    - this file can be run using a terminal
    - this file can run on aoi that have multiple features of type "Polygon" in the geojson file but each feature will need to have a unique feature id. 
    { "type": "Feature", "properties": {"site":"DC", "id":"1"}, "geometry": { "type": "Polygon", .....

 - find_false_stereo_notebook.ipynb : best run directly in a code editor.


The logic is as follows:
 -  step-1 : check that two scenes have 80% to 100% overlap
 -  step-2 : confirm they are on opposite orbits or if on the same orbit that they have opposing look angles.

Please note that this tool might also return true stereo pairs.

This tool only works with the following collections:
 - pneo
 - phr
 - spot

Search dates format are as follows:
 - "Y-M-D" for example '2022-01-01'

Cloud cover is a percentage:
 - 0 to 100

The results can be loaded into a GIS software. Each output geojson vector file contains the potential stereo pairs, therefore each file written should have two features in the layer.

Future next steps for reviewing and selecting scenes:
 - Pull and plot quicklooks for visual cloud validation
 - Credit cost before purchasing

Please note, this program and notebook are not actively maintained and are not official UP42 products.

Have fun, best of luck! :)

Alex

