### False Stereo pairs - UP42 SDK

This python tool provides a way to discover false stereo pairs against Airbus satellite catalog data using the UP42 SDK. It can contains two python files.
 - find_false_stereo_for_terminal.py: this file can be run using a terminal.
 - find_false_stereo.py: best run directly in a code editor.

Please note that this tool might also return true stereo pairs. The logic is as follows:
 -  step-1: check that two scenes have 80% to 100% overlap
 -  step-2: confirm they are on opposite orbits or if on same orbit that they have opposing look agnles.

Side note, at the moment this tool will also identify true stereo pairs as false stereo.
