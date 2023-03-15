#!/usr/bin/env python 

import os
import sys
import glob
import bisect 
import subprocess

fnList=[]



for filename in glob.iglob('./out/*.jpg'):
    # if (filename.startswith( 's-')):
    bisect.insort(fnList,filename)
    #print('%s' % filename)

#print(fnList)

if 1:
    for theFile in fnList:
        print("%s" %  theFile)
        
        fn       = os.path.basename(theFile) # name des scripts holen
        fn_noExt = os.path.splitext(fn)[0]
        
        ffn  = os.path.realpath(theFile)     # ffn
        pfad = os.path.dirname(ffn)   # path where this script runs
        
        print("Current file name no ext   : %s" % fn_noExt)
        print("Current file name with ext : %s" % fn)
        print("Current file dir           : %s" % pfad)
        print("Current file full name     : %s" % ffn)
        
        
        cmd="convert " + ffn + " -write histogram:" + "histA-" + fn_noExt +".gif" + \
                    " -equalize -write histogram:" + "histB-" + fn_noExt + ".gif" + \
                    " E-" + fn_noExt + ".jpg"
        
        cmd = "./redist.sh -s gaussian 60,60,60  " + ffn + " " + \
              "gauss-" + fn_noExt + ".jpg"
        
        
        # best choice so far 
        # for color correction
                
        # modulate works in HSL (hue-saturation-lightness) colorspace
        # It takes three values (though later values are optional) 
        # as a percentage such that 100 will make no change to an image.
        # modulate option:   - modulate brightness satuartion hue
        # http://www.imagemagick.org/Usage/color_mods/#hist_redist
        #   < 100 = darker
        #   = 100 = no change
        #   > 100 = brighter
        cmd = "convert " + ffn + " -modulate 100 " + "mod-" + fn_noExt + ".jpg"
        
        # crop image (cut out a certain section)
        # new image: widthxheight+x0+y0
        #   width, height of new resulting image
        #   x0,y0 = origin starting point from top left corner of the image
        cmd = "convert " + ffn + " -crop 704x240+0+0 +repage " + "crop-" + fn_noExt + ".jpg"
                
        print("The Command: %s" % cmd)
        subprocess.call(cmd, shell=True)



    sys.exit()

# create a vide now with the folowing ffmpeg command
# ffmpeg -framerate 10 -pattern_type glob -i '*.jpg'  -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
# ffmpeg -framerate 10 -pattern_type glob -i '*.jpg' out2.mp4

#print("The Command: %s" % cmd)
#subprocess.call(cmd, shell=True)




# specify time in sec
delaySec =  0.2
#delaySec =  2
#delaySec = 10

shellCmd = ""
shellCmd = "convert -delay " + str(delaySec) + "x1 -dispose Background \\"
print(shellCmd)

for fn in fnList:
   print("%s" %  fn)
   #shellCmd = shellCmd + fn + "\\"
   shellCmd = shellCmd + fn + " "

shellCmd = shellCmd + " -loop 0 slideshow_" + str(delaySec) + ".gif"

print("%s" % shellCmd)
subprocess.call(shellCmd, shell=True)

print("")
print("#")
print("# Ready")
print("#")
