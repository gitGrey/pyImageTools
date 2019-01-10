#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os     # some path operations
import sys    #
import shutil # for file copy

# Python Image Library (pillow)
# pip install Pillow
from PIL import Image

# JPG EXIF readout
from PIL.ExifTags import TAGS

# for color conversions
import colorsys

global goodFiles

goodFiles=[]

# a debug option (extended output)
deb=1
deb=0

def writeHeaderLine():
    ret=[]
    
    ret.append("fn")
    ret.append("img-width")
    ret.append("img-height")
   
    ret.append("p1-x")
    ret.append("p1-y")
    
    ret.append("p1-r")
    ret.append("p1-g")
    ret.append("p1-b")    

    ret.append("p1-h")
    ret.append("p1-l")    
    ret.append("p1-s")    
    
    ret.append("p1-h")
    ret.append("p1-s")    
    ret.append("p1-v")        
    
   
    ret.append("p2-x")
    ret.append("p2-y")
    
    ret.append("p2-r")
    ret.append("p2-g")
    ret.append("p2-b")    
    
    ret.append("p2-h")
    ret.append("p2-l")    
    ret.append("p2-s")    
    
    ret.append("p2-h")
    ret.append("p2-s")    
    ret.append("p2-v")        
    
    sep=";"
    resultStr= ';'.join(ret)
    
    return resultStr

def getImgInfo(theImg):

    ret=[]        
    
    global goodFiles
    
    fn=theImg
    
    im = Image.open(fn).convert('RGBA')
    #im.show()

    width, height = im.size
    
    ret.append(fn) 
    ret.append(str(width))
    ret.append(str(height))
    
    pixels = im.load()
    
    if 1:
        # analyze certain position / point 1
        # in the image and get color values
        # specifiy location here
        x=212
        y=143
        ret.append(str(x))
        ret.append(str(y))    

        col = pixels[x, y]
        
        r=col[0]
        g=col[1]
        b=col[2]
        
        # RGB Values
        ret.append(str(r)) #R
        ret.append(str(g)) #G   
        ret.append(str(b)) #B 
    
        # HLS (Hue Lightness Saturation)
        hls=colorsys.rgb_to_hls(r, g, b)
        ret.append(str(hls[0]))
        ret.append(str(hls[1]))
        ret.append(str(hls[2]))
        
        
        #
        # specify something you look for here
        # like a certain color / lightness value 
        lightness=hls[1]
        # if lightness>=100: # a fixed value
        if 100 <= lightness <= 120 : # Python interval comparison
            goodFiles.append(fn)
        
        
        # HSV (Hue Saturation Value)
        hsv=colorsys.rgb_to_hsv(r, g, b)
        ret.append(str(hsv[0]))
        ret.append(str(hsv[1]))
        ret.append(str(hsv[2]))
    
    if 1:
        # analyze certain position / point 2
        # in the image and get color values
        # specifiy location here
        x=217
        y=146
        ret.append(str(x))
        ret.append(str(y))    
        
        col = pixels[x, y]
        
        r=col[0]
        g=col[1]
        b=col[2]
        
        # RGB Values
        ret.append(str(r)) #R
        ret.append(str(g)) #G   
        ret.append(str(b)) #B 
    
        # HLS (Hue Lightness Saturation)
        hls=colorsys.rgb_to_hls(r, g, b)
        ret.append(str(hls[0]))
        ret.append(str(hls[1]))
        ret.append(str(hls[2]))
    
        # HSV (Hue Saturation Value)
        hsv=colorsys.rgb_to_hsv(r, g, b)
        ret.append(str(hsv[0]))
        ret.append(str(hsv[1]))
        ret.append(str(hsv[2])) 
        
        
    sep=";"
    resultStr= ';'.join(ret)
    if deb:
        print ("%s" % resultStr)
    
    return resultStr

    
def get_exif(fn):
    
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
        
    if info is None:
        return ""
        
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
        
    return ret


def create_dir(d):
    
    #d = os.path.dirname(f)
    
    if not os.path.exists(d):
        os.makedirs(d)
        if deb:
            print("Output Dir (created): " + d) 
    else:
        if deb:
            print("Output Dir (existing): " + d)



# *******************************************************
# *******************************************************
# Program starts here, let's roll
# *******************************************************
# *******************************************************

if __name__ == '__main__':
    
    fn       = os.path.basename(__file__)     # name des scripts holen
    fn_noExt = os.path.splitext(fn)[0]
    
    pfad1 = os.path.realpath(__file__)
    pfad2 = os.path.dirname(pfad1)    # pfad wo dieses script läuft
    
    print("Current script: %s" % fn)
    print("Current script: %s" % fn_noExt)
    print("Current dir   : %s" % pfad1)
    print("Current dir   : %s" % pfad2)
    
    file_id1 = 0
    reportFn = fn_noExt + "-report.txt"
    file_id1 = open(reportFn, "w")
    
    ret=writeHeaderLine()
    file_id1.write(ret + "\n")    
    
    # Linux Path Separator: /
    # Windows Path Separator \
    
    searchDir = "." # current dir
    searchDir = "./avz" 
    #searchDir = r"C:\tmp\xqsv\images\"
    #searchDir="/home/pi/pictures"
    #searchDir="/home/nuc/Pictures"
    
    print("OS: " , sys.platform )
    if sys.platform.lower()=="win32":
        
        if "\\" in searchDir:
            # this is a windows path
            pass
      
        if "/" in searchDir:
            # this is Linux Path
            searchDir=searchDir.replace("/","\\")
                
    elif sys.platform.lower()=="linux":
    
        if "\\" in searchDir:
            # this is a windows path
            searchDir=searchDir.replace("\\","/")    
      
        if "/" in searchDir:
            # this is Linux Path
            pass
    
    
    myImages = [] # list of image filenames
    
    dirFiles = os.listdir(searchDir) # list of directory files

    dirFiles.sort()  # good initial sort but doesnt sort numerically very well

    sorted(dirFiles, reverse=False) # sort numerically in ascending order
    
    print("")
    print("Only *.png and *.jpg Files allowed")
    print("Image Search Dir : %s" % searchDir)
    print("Initial scan     : %s files found" % len(dirFiles))
    print("sorting out files")

    #print(dirFiles)

    # below iterates through all entries in a folder
    # it returns file and folder names
    i=0
    isImage=0
    
    for theFile in dirFiles:

        # here we have folders and files
        i+=1

        ffn = os.path.join(searchDir, theFile)
        #print("%s --> %s" % (i, theFile))
        #print("%s --> %s" % (i, ffn))
        #name, ext = os.path.splitext('file.txt')

        if os.path.isdir(ffn):
            # folder / directory     
            pass
            #print("Directory found : %s" % theFile)

        if os.path.isfile(ffn):
            #print("File found : %s" % theFile)
            #print("Full Name  : %s" % os.path.dirname(theFile))
            #os.path.join(path, file)):

            isImage=0
            
            theFileName=theFile.lower()
                
            if '.jpg' in theFileName:
                isImage=1

            if '.png' in theFileName:
                pass # currently no png because they have no EXIF
                #isImage=1
                
            if isImage==1:
                #im = Image.open(ffn)
                #width, height = im.size
                            
                myImages.append(theFile)                  
                

    print("")               
    print("%s images found " % len(myImages))
    print("")

    #myimages.sort(reverse=True)
    myImages.sort(key=str.lower)
    
    i=0
    # print image names and index
    for theImg in myImages:
   
        i+=1
        print("%03d/%03d: %s" % (i, len(myImages), theImg))
       
        ffn = os.path.join(searchDir, theImg)
        ret = getImgInfo(ffn)
        
        exif_inf =""
        
        if 0: # set 1 for EXIF data in output
            #
            # print EXIF content
            #
           
            ret_exif=get_exif(ffn)
            #print(ret_exif)
            
            exif_inf =""
            for val in ret_exif:
                print("%s %s" % (val, ret_exif[val]) )
                exif_inf = exif_inf + ";" + str(val) + ";" + str(ret_exif[val]) 
        
        ret = ret + exif_inf
        file_id1.write(ret + "\n")    
                    
    file_id1.close()    

    outP = 'out'
    create_dir(outP)
    # copy good files to a new directory    
    print("")
    print("copy files to new directory")
    i=0
    for goodFile in goodFiles:
        i+=1
        print("goodFile %s/%s --> %s" % (i, len(goodFiles), goodFile))
        fn  = os.path.basename(goodFile) 
        ffn = os.path.join(searchDir, fn)
        
        #newFfn = os.path.join(outP,"good-" + fn) 
        #shutil.copy2(ffn, newFfn) # complete new target filename given
        shutil.copy2(ffn, outP)   # only output/ target path = keep source filename

    print("")
    print("%s good files copied to folder:" % len(goodFiles))
    print("   %s" % os.path.join(pfad2 , outP))

    print("")
    print("your image color report is here:")
    print("   %s" % reportFn)
    print("   %s" % pfad2)
    print("   %s" % os.path.join(pfad2 , reportFn))
    
    print("")
    print("analyze this report with MS-Excel")
    print("use the R,G,B values from the report to color")
    print("a cell and check lightness values")
    print("use min/max functions to analyze lightness")
    
    print("")
    print("example Excel VBA Code below (hint, to be adjusted)")    
    print("For i = 6 To 300")
    print("  r = Cells(i, 6)")
    print("  g = Cells(i, 7)")
    print("  b = Cells(i, 8)")
    print("  Cells(i, 3).Interior.Color = RGB(r, g, b)")
    print("next")
          
    print("")
    print("Ready")
