==============================
ConnectomeViewer Release Notes
==============================

Version 0.2.0 (DATE)

Version 0.1.9 - BETA (August 11th 2010)

* Changed to numpy.distutils for packaging
* Update installation scripts for Ubuntu and Fedora
* Added Network Based Statistics Plugin. Thanks goes to Andrew Zalesky.
* Update documentation and added tutorials
** Dipy tutorial: From Diffusion to tracks
** NBS: Computing network based statistics
** Update Matlab Interfacing tutorial
** Added Red Button Tutorial
** Added BlenderExporter tutorial
* Addition of libraries folder for external packages (cviewer.libs)
** PyEEG, Tomoviz, DiPy. PyConto.
* Added for external packages corresponding documentation (externals/)
 * Restructured folders (examples, externals)
* Bugfixes

Version 0.1.8 - BETA (July 16th 2010)

* Replaced Gifti support by a pure Python solution (to be integrated into Nibabel)
* Improvements on the installation scripts and dependency management
* Dropped installation support for Windows
* Minor bugfixes

Version 0.1.7 - BETA (May 25th 2010)

* Updated installation script for Ubuntu and Fedora
* Addition of WelcomePerspective
* Better checking for dependency
* Bugfixes for Windows

Version 0.1.6 - BETA

* Added more tutorials to the documentation.
* Added node label interactivity to the 3D View. Toggle label upon pressing 'g'
* Inclusion of the developmental Diffusion in Python (DiPy) project to
the ConnectomeViewer namespace (track visualization, segmentation, measures, IO)
* Inclusion of updated IO routines of image data from the NiPy project
* Addition of a Matrix Viewer to readily inspect connectivity matrices
* Edge Visualization Parameter dialog box added that allows easy change of
edge attribute and thresholding (absolute, proportional, counting)
* Text Editor uses default Script Path to open files
* sLORETA Converter Plugin to convert EEG data (lagged coherences, statistics etc.)
analysed with sLORETA into the Connectome File Format (not yet)
* The ConnectomeDatabase plugin is working again, now using PyMySQL, a pure python MySQL client
* Bugfix and Updates in PreferenceManager. Added Use IPython field.
* Bugfix for Windows XP, interpolating scalar values automatically

Version 0.1.4 - BETA

* Integrated a Volume Slicer by Gael Varoquaux
* Scheduler to Run Scripts which remembers the Script Path

Version 0.1.3 - BETA

* Supporting the Connectome File Format (CFF). It includes data in standardized formats:
GraphML (networks), Gifti (surfaces), Nifti (volumes), .trk (tracks) and XML (metadata)
* 3D View: Visualization of Networks and Surfaces in 3D. Picking functionality to select nodes and edges.
Link to the ConnectomeWiki knowledge-base. See Help->Key Bindings for more details.
* Mayavi2 Plugin: Visualization Tree and Visualization Object Editor to create VTK-Based pipelines
for visualization
* Python Shell Plugin for interactive scripting
* Text Editor Plugin for writing and executing scripts
* Storing metadata in networks. Consult the connectome.xsd file
<http://www.connectomics.org/connectome.xsd>
* ConnectomeDatabase Plugin for connection to a SQL database containing connectome files.
* Bindings Plugin: Binds the currently loaded Connectome File in the console to cfile,
allowing access to all the data
* Analysis Perspective: Selection of Network or selected Subnetwork and carry out Network
Analysis using the NetworkX library.
* Interface to TrackVis <http://www.trackvis.org> for visualization of individual tracts.
Region of Interest are automatically generated for selected nodes.
* Launchpad.net for development: Feature Requests, Bug Tracker, Source Code Repository
