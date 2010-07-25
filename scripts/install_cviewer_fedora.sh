#!/bin/sh

echo "Welcome to the Installation Script for ConnectomeViewer BETA"
echo "============================================================"
echo "Do you want to download the example datasets ? [Y]es / [N]o "
read exdata
case "$exdata" in
# Note variable is quoted.

  "Y" | "y" | "yes" | "Yes" )
  echo "========================================="
  echo "Download Connectome File Example datasets"
  echo "========================================="
  echo "Type the full path to store ConnectomeViewer datasets:"
  read fullp
  mkdir -p $fullp
  cd $fullp
  wget http://www.connectomeviewer.org/datasets/homo_sapiens_01.cff
  wget http://www.connectomeviewer.org/datasets/homo_sapiens_02.cff
  wget http://www.connectomeviewer.org/datasets/homo_sapiens_03.cff
  wget http://www.connectomeviewer.org/datasets/macaca_mulatta_01.cff
  cd ..
  ;;

          * )
   # Default option.	  
   # Empty input (hitting RETURN) fits here, too.
   echo
   echo "Not downloading Connectome File example datasets."
  ;;

esac

echo "===================================================================="
echo "Add required Fedora packages, including header files for compilation"
echo "===================================================================="
sudo yum install python-pip numpy scipy python-devel ipython vtk vtk-devel swig python-configobj libXtst libXtst-devel freeglut freeglut-devel python-matplotlib python-lxml Cython qscintilla-python python-sphinx wxPython wxPython-devel subversion gcc gcc-c++ libXt libXt-devel libX11-devel hdf5 hdf5-devel python-setuptools-devel python-h5py python-AppTools python-EnvisageCore python-EnvisagePlugins python-Traits python-TraitsBackendQt python-TraitsGUI

#echo "========================================================"
echo "Install/Update required packages for the ConnectomeViewer"
echo "========================================================="

echo "============"
echo "... NetworkX"
echo "============"
sudo pip install networkx

echo "=========="
echo "... Cython"
echo "=========="
sudo pip install Cython

echo "==========="
echo "... PyMySQL"
echo "==========="
sudo pip install http://pymysql.googlecode.com/files/PyMySQL-0.2-py2.6.egg

echo "========================================="
echo "Download and install the ConnectomeViewer"
echo "========================================="

sudo pip install -e git://github.com/unidesigner/connectomeviewer.git@dev-restruct#egg=ConnectomeViewer

echo "==================================================="
echo "The installation script is finished. It may well be that errors have occured."
echo "Test your ConnectomeViewer installation by typing in the terminal:
echo "-----------
echo "connectomeviewer -v
echo "-----------
echo ""
echo "If there are problems, rerun the installation script with:"
echo "-----------
echo "sh ./install_cviewer_ubuntu.sh > logfile.txt"
echo "-----------
echo "Send the logfile.txt together with ConnectomeViewer startup logfile (automaticall generated) to info@connectomics.org."
echo "============================================================="