### False Stereo pairs - UP42 SDK

This python tool provides a way to discover false stereo pairs in Airbus satellite catalog data using the UP42 SDK. It can contains teo python files.
 - find_false_stereo_for_terminal.py: this file can be run using a terminal.
 - find_false_stereo.py: best run directly in a code editor.

Please note that this tool might also retunr true stereo pairs. The logic is as follows:
 -  step-1: check that two scenes have 80% to 100% overlap
 -  step-2: confirm they are on opposite orbits or if on same orbit that they have opposing look agnles.


