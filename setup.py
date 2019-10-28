#import statements
import os, sys

#list of the required modules to be installed via PIP
requiredModules = [
    'pillow', #needed for image editing
    'pygame', #needed for screen resolution sensing
]

#install the required modules
for module in requiredModules:
    print('Installing the module "{}" via PIP.'.format(module))
    os.system('{} -m pip install {}'.format(sys.executable, module))

#list of directories to create
directoriesToMake = [
    './outputs', #for the output files made with pillow
]

#make the directories
for directory in directoriesToMake:
    print('Creating the directory "{}".'.format(directory))
    try:
        os.mkdir(str(directory))
    except Exception as err:
        print('Could not create the directory "{}". Error: "{}".'.format(directory, err))

#list of files to create ([NAME, CONTENTS])
filesToMake = [
    ['./screenSize.json', '[1920, 1080]'], #for setting the size of the wallpaper
]

#make the files
for file in filesToMake:
    print('Creating the file "{}".'.format(file[0]))
    try:
        fileObject = open(str(file[0]), 'w')
        fileObject.write(str(file[1]))
        fileObject.close()
    except Exception as err:
        print('Could not create the file "{}". Error: "{}".'.format(file[0], err))

#tell the user that the program is done
print('Finished setting up the program.')