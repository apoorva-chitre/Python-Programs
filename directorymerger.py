__author__ = 'Apoorva Chitre'

# Program to copy and merge the contents of two directories into a new destination directory, without modifying the source directories
# and Display the contents of both source directories and then destination directory.

import sys
import os
import shutil


latestFiles = [] # list to hold latest copy of a file existing in both sources

# function to find list of files that exist in both source directories

def sameNameFiles(src1,src2) :

    src1Contents = os.listdir(src1)
    src2Contents = os.listdir(src2)

    files1 = [] # list to hold all files of source1
    files2 = [] # list to hold all files of source2

    # Extract only files from source 1
    for item in src1Contents :
        if os.path.isfile(os.path.join(src1, item)):
            files1.append(item)

    # Extract only files from source 2
    for item in src2Contents :
        if os.path.isfile(os.path.join(src2, item)):
            files2.append(item)

    for item in files1 :
        src1Contents.remove(item)

    for item in files2:
        src2Contents.remove(item)

    # Determine which version of the file existing in both sources is the newest/latest using getmtime()
    for item in files1:
        if item in files2:
            if os.path.getmtime(os.path.join(src1,item)) > os.path.getmtime(os.path.join(src2,item)) :
                latestFiles.append(os.path.join(src1, item))
            elif os.path.getmtime(os.path.join(src1,item)) < os.path.getmtime(os.path.join(src2,item)) :
                latestFiles.append(os.path.join(src2, item))

    # Recursively traverse other files and subdirectories in source 1
    for item in src1Contents :
        if item not in src2Contents :
            traverse(os.path.join(src1, item))

    # Recursively traverse other files and subdirectories in source 2
    for item in src2Contents :
        if item not in src1Contents :
            traverse(os.path.join(src2,item))

    # Recursively traverse subdirectories and find and process files common to sources 1 and 2
    for item in src1Contents :
        if item in src2Contents :
            sameNameFiles(os.path.join(src1, item), os.path.join(src2, item))

# function to recursively process subdirectories
def traverse(src) :
    list1 = []
    list2 = []


    srcContents = os.listdir(src)

    for item in srcContents :
        data = os.path.join(src, item)
        if os.path.isfile(data):
            list1.append(data)

        elif os.path.isdir(data):
            list2.append(data)

    for item in list2 :
        traverse(item)

# function to copy contents of source to destination

def copyContents(src,dest,symlinks=True):
    if not os.path.exists(dest):
        os.makedirs(dest)
    errors = []
    for item in os.listdir(src) :
        s = os.path.join(src,item)
        d = os.path.join(dest,item)
        try:
            #if item is a symbolic link
            if symlinks and os.path.islink(s):
                    linkto = os.readlink(s)
                    os.symlink(linkto, d)

            #if item is a file
            if os.path.isfile(s):
                shutil.copy2(s,d)

            #if item is a directory
            if os.path.isdir(s):
                copyContents(s,d,symlinks=True)
        except OSError as why :
            errors.append((s,d,str(why)))



# Conditions to check if there are missing or extra directory names in the command line

if len(sys.argv) > 4 :
    print("Too many arguments provided to program.")
    sys.exit()

elif len(sys.argv) < 4:
    print("One or more arguments missing in the program input.")
    sys.exit()

# conditions to check whether invalid directory names provided, file names rather than directory names, same directory names
# or if destination directory already exists

if len(sys.argv) == 4 :
    if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):     # if names are valid

        if os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]):   # if both are directories

            if os.path.samefile(sys.argv[1],sys.argv[2]) :     # if both have different names
                print("Both source directories should have different names.")
                sys.exit()
            else:
                if os.path.exists(sys.argv[3]) :    # if destination directory already exists
                    print("Destination directory already exists, provide a new directory.")
                    sys.exit()
                else:
                    os.mkdir(sys.argv[3]) # create destination directory
                    copyContents(sys.argv[1],sys.argv[3]) # call function to copy source1 files to destination
                    copyContents(sys.argv[2],sys.argv[3]) # call function to copy source1 files to destination
                    sameNameFiles(sys.argv[1],sys.argv[2]) # call function to merge common files in source1 and source2 to destination



        else:
            print("Both sources should be directories, not files.")
            sys.exit()
    else:
        print("One or both source directory names are invalid.")
        sys.exit()

SourceDir1 = sys.argv[1]
SourceDir2 = sys.argv[2]
destDir = sys.argv[3]

# to keep the files in destination updated

for item in latestFiles :
    if item in SourceDir1 :
        destPath = destDir + item[len(SourceDir1):]
        shutil.copy2(item,destPath)

    if item in SourceDir2 :
        destPath = destDir + item[len(SourceDir2):]
        shutil.copy2(item,destPath)

# function to display contents of a directory
def displayContents(dir) :
    path = dir
    for (path,dirs,files) in os.walk(path):
        print(path)
        for file in files:
            print(file,"Last Modified:",os.path.getmtime(path),"Last Accessed: ",os.path.getatime(path),sep="\t")
        print("-----------------------------------------------------------------")

print("Directory Merger Success!",end="\n")
print("Contents of first Source Directory : ",end="\n")
displayContents(sys.argv[1])
print(end="\n")
print(end="\n")
print("Contents of second Source Directory : ",end="\n")
displayContents(sys.argv[2])
print(end="\n")
print(end="\n")
print("Contents of Destination Directory : ",end="\n")
displayContents(sys.argv[3])


# Result of Program with detailed directory listings

#C:\Users\lg\PycharmProjects\CSCI6651>py directorymerger.py D:/source1 D:/source2
# D:/destDir
#Directory Merger Success!
#Contents of first Source Directory :
#D:/source1
#abc.txt Last Modified:  1477798350.6754851      Last Accessed:  1477798350.67548
#51
#def.txt Last Modified:  1477798350.6754851      Last Accessed:  1477798350.67548
#51
#-----------------------------------------------------------------
#D:/source1\alpha
#alpha.txt       Last Modified:  1477795520.1559322      Last Accessed:  14777955
#20.1559322
#-----------------------------------------------------------------
#D:/source1\alpha\beta
#beta.txt        Last Modified:  1477795562.2847798      Last Accessed:  14777955
#62.2847798
#-----------------------------------------------------------------
#D:/source1\alpha\gamma
#gamma.txt       Last Modified:  1477795583.7308805      Last Accessed:  14777955
#83.7308805
#-----------------------------------------------------------------
#
#
#Contents of second Source Directory :
#D:/source2
#def.txt Last Modified:  1477798382.0332787      Last Accessed:  1477798382.03327
#87
#-----------------------------------------------------------------
#D:/source2\delta
#delta.txt       Last Modified:  1477795722.2125678      Last Accessed:  14777957
#22.2125678
#-----------------------------------------------------------------
#D:/source2\gamma
#alpha.txt       Last Modified:  1477795694.1064117      Last Accessed:  14777956
#94.1064117
#gamma.txt       Last Modified:  1477795694.1064117      Last Accessed:  14777956
#94.1064117
#-----------------------------------------------------------------
#
#
#Contents of Destination Directory :
#D:/destDir
#abc.txt Last Modified:  1477803023.5047557      Last Accessed:  1477803023.50475
#57
#def.txt Last Modified:  1477803023.5047557      Last Accessed:  1477803023.50475
#57
#-----------------------------------------------------------------
#D:/destDir\alpha
#alpha.txt       Last Modified:  1477803023.493755       Last Accessed:  14778030
#23.493755
#-----------------------------------------------------------------
#D:/destDir\alpha\beta
#beta.txt        Last Modified:  1477803023.4927552      Last Accessed:  14778030
#23.4927552
#-----------------------------------------------------------------
#D:/destDir\alpha\gamma
#gamma.txt       Last Modified:  1477803023.4947553      Last Accessed:  14778030
#23.4947553
#-----------------------------------------------------------------
#D:/destDir\delta
#delta.txt       Last Modified:  1477803023.5027556      Last Accessed:  14778030
#23.5027556
#-----------------------------------------------------------------
#D:/destDir\gamma
#alpha.txt       Last Modified:  1477803023.508756       Last Accessed:  14778030
#23.508756
#gamma.txt       Last Modified:  1477803023.508756       Last Accessed:  14778030
#23.508756
#-----------------------------------------------------------------

