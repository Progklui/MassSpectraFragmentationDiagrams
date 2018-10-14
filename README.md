# Fragmentation Diagrams

This project helps creating fragmentation diagrams of mass spectrometer data collected with an XCalibur ready device.

## Getting Started - plotting the first diagram

### I - convert XCalibur .raw into readable .mzXML:

On a windows machine open cmd.exe in the folder where ReAdw.exe and zlib1.dll are installed (hold Strg-Tab and right click on folder - open folder with cmd.exe). Type in the following command (replace capital letters with your settings):

```
ReAdw --mzXML RawFiles\DDMMYYYY\PLANTNAME\FILENAME.raw
```

Of course the corresponding .raw ought to be in that folder first. After successful conversion you will have a FILENAME.mzXML file in this folder. It is important to keep this structure of folders for the next steps. So - we are ready for the next step.

### II - select parts of file to extract:

In OS where the emzed2 environment is installed (e.g. Ubuntu 14.04) open a terminal and type:

```
source ~/emzed2/bin/activate
```
then
```
emzed.workbench
```

Open peak_extraction.py and edit the following variables:

* date = 'DDMMYYYY' - corresponding to date of measurement which is also set in RawFiles and previous step
* plant = 'PLANTNAME' - in accordance with folder structure of .mzXML file (like date variable!!)
* filename = 'FILENAME' - without .mzXML extension
* compound_to_analyse = 'MASSFragmentationmode' - e.g. '777PQD' or '645CID'
* version = 'VERSION' - e.g. 'Version1' - making multiple versions of one compound is recommended (e.g. isomer detection)
* beginID = SCAN - where isolation/measurement started - derive from XCalibur programm
* endID = SCAN - where isolation/measurement ended

Run programm with F5 or similar. Maybe repeat for different versions.

### III - plotting and analysing (where the fun begins):

In OS where python 3.x environment is installed open folder where fragmentationDiagrams.py is located. Run the following:

```
python3.5 fragmentationDiagrams.py
```

A list of options opens - the rest should be self-explanatory. Just experiment a bit. Also with the peak tables generated and stored into a .csv file (bear in mind that everything you create is stored but can easily be overwritten by plotting again!)

```
Note on good practice: 
```
```
This repo contains all necessary programs - keep them in this folder and simply add/create folders RawFiles/DATEOFMEASUREMENT/PLANTNAME . Only ReAdW.exe needs to be run on a Windows machine. The rest works on e.g. Ubuntu 14.04 fine. If you want to use different file structures you are encouraged to change a bit of the code. It is just optimized for specific analyis so far!
```

## Prerequisites

### plotting and analysis of diagrams 

File: fragmentationDiagrams.py

The plotting code should run in any python 3.x environment with standard scientific libraries installed:

* [matplotlib](https://matplotlib.org/users/installing.html) - for plotting editable diagrams
* [scipy](https://www.scipy.org/)
* [numpy](http://www.numpy.org/)
* [pandas](https://pandas.pydata.org/) - data manipulation
* [sklearn](http://scikit-learn.org/) - for filtering data with savitzky-golay filter

However in the developing process some errors occured with specific versions of the tools used. All the testing and development took place in a python 3.5.4 environment using matplotlib 2.1.0. 

### extracting of peaks and preparation for plotting

The code for extracting the peaks out of the .mzXML files received from ReAdW.exe is run in an emzed2 environment using python 2.7.

## Keeping updated

If you want to keep updated with this repo run the following:

### Clone fork

```
git clone https://github.com/Progklui/MassSpectraFragmentationDiagrams.git
```

## Add remote from this repo in your forked repo
 
```
cd into/forked_repo
git remote add upstream https://github.com/Progklui/MassSpectraFragmentationDiagrams.git
git fetch upstream
```

## Updating

```
git pull upstream master
```

Done!

## Built With

* [Jupyter](http://jupyter.org/) - part of the programming environment used
* [emzed](http://emzed.ethz.ch/) - other part of programming environment used
* [IonSource](http://www.ionsource.com/functional_reviews/readw/t2x_update_readw.htm) - used for file conversion

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


