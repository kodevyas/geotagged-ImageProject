# About

This piece of code is the solution for the problem statement in the ProblemStatment.txt
The entire source code is in Python 3

### Requirments

It uses two Python libraries that you might need to install first.
- piexif
- geopy
- srt
- simplekml

You can install both the libraries through pip
  $ pip install <package_name>

### File Structure

The file structure for this package is:

              project
                    |_ images                 # contains all the exif tagged images
                    |_ output                 # contains all the output files generated by the program       
                    |_ videos                 # contains all the assets and video files
                    |_ ProblemStatment.txt    # problem statement for which this package is written
                    |_ config.py              # a simple configuration file to coustomize the software according to Requirments
                    |_ main.py                # Contains all the source code for the software
                    |_ Reamdme.md             # a readme file

### Assumptions

This software runs is under following assumptions:
- All the video files are of *'SRT'* file and all the assets file are of *'csv'* files and with a fixed format of data representation.
- All the distance will be either one of these formates: *kilometers*, *meters* or in *miles*
- The program also dosen't considers *altitude* for calculating the distance. It evaluates all distances with altitude *'0'*
