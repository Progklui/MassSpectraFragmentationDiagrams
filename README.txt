ReAdW version 4.3.1
 Thermo Xcalibur raw file to mzXML converter

Natalie Tasman, primary developer
  with Jimmy Eng, Brian Pratt, and Matt Chambers,
  based on orignal work by Patrick Pedriolli.

September 9, 2009


please see also:
 http://tools.proteomecenter.org/wiki/index.php?title=Software:ReAdW
 http://groups.google.com/group/spctools-discuss
 http://groups.google.com/group/spctools-announce



DISCLAIMER
==========

Output from this program tries to replicate information from the
original input to the best of the authors' ability; however, please do
not use output from the converter for any work which requires
verfication (pharmaceutical, medical research, etc.)



Installing ReAdW
================

ReAdW requires a valid installation of the Thermo XCalibur software
system, as it relies on the XCalibur libraries.


Using ReAdW
===========

ReAdW is run from the command line, and outputs mzXML (3.1).


Usage: ReAdW [options] <raw file path> [<output file>]

 Options
  --mzXML:         mzXML mode (default)
  --mzML:          mzML mode (will use msconvert)
      one of --mzXML or --mzML must be selected

  --centroid, -c: Centroid all scans (MS1 and MS2)
      meaningful only if data was acquired in profile mode;
      default: off
  --compress, -z: Use zlib for compressing peaks
      default: off
  --verbose, -v:   verbose
  --gzip, -g:   gzip the output file (independent of peak compression)

  output file: (Optional) Filename for output file;
      if not supplied, the output file will be created
      in the same directory as the input file.


Example: convert input.raw file to output.mzXML, centroiding MS1 and MS2 scans

      ReAdW --mzXML -c C:\test\input.raw c:\test\output.mzXML

Author: Natalie Tasman (SPC/ISB), with Jimmy Eng, Brian Pratt, and Matt Chambers,
      based on orignal work by Patrick Pedriolli.



Getting the code
================

The code for this program is released under the LGPL.  It can be found
in our SVN repository, specifically from the directories

  http://sashimi.svn.sourceforge.net/svnroot/sashimi/tags/release_4-3-0/trans_proteomic_pipeline/src/mzXML/common
  http://sashimi.svn.sourceforge.net/svnroot/sashimi/tags/release_4-3-0/trans_proteomic_pipeline/src/mzXML/converters/ReAdW
  
Code was build under Visual Studio 2005 (use the ReAdW project from within the TPP.sln.)


Note you will need zlib header and lib files; a compatable version can be found under

  http://sashimi.svn.sourceforge.net/svnroot/sashimi/tags/release_4-3-0/win_lib

and will be automatically used if building with the TPP solution (recommended.)


Known ReAdW Issues
==================

Source and Analyzer Instrument information is currently set from first scan's filter line.  This certainly fails for LTQ-FT, which has two detectors.

Centroiding should be recorded on a scan-by-scan basis but is
currently only recorded in the header if the user sets it.  Thus, a
file accquired in centroid and convertered without -c will not record
the "centroid" info correctly.

Both issues will be fixed in future releases.



Thermo/Xcalibur API Issues
==========================

Instrument serial number is always returned as blank

Detector: I don't know how to extract instrument detector info,
if it's in the raw file.  I've currently set detetor to the dummy
value of "electron multiplier tube".

In general, error status is unreliable for at least some important
calls.



Feedback
========

Comments and suggestions are welcome.  You are encouraged to contact
the TPP team, preferrably through the spctools-discuss newsgroup
(see the link at the top of this file).


--Natalie Tasman, September 9, 2009
