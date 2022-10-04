# FluorescenceDetectionScript

This script has been developed as a Python Macro for FIJI, to assist with the process of data collection from light microscopy images of microfluidic infection-on-a-chip devices. It detects the area of bacterial fluorescence (from GFP or pHrodo) observed in the microchamber, via the following steps:
- Duplicates the area selected by the ROI
- Converts this duplicate to an 8 bit image
- Creates a binary mask of fluorescence/background
- Determines the area of the mask which is fluorescent 
- Calcualtes the percentage of the ROI which contained fluorescence

The following factors can be adjusted:
- Size of the ROI
  
  *yolk = OvalRoi(0, 0, 180, 180)*
  
  The height and width of the ROI is determined by the 3rd and 4th numbers listed. This can be altered by adjusting the 180 up or down. 
  Note: this line appears twice in the code to reset the ROI on the duplicated image and needs to be the same in both instances.
- Threshold colour which is determined to be fluorescent
  
  *IJ.setThreshold(crop, 60, 255, "black & white")*
  
  This line is added for manual thresholding and commented out for automatic thresholding. To manually change the thresholding value, edit the minimum and maximum value from 60 and 255 respectively.
  Once converted to an 8-bit image the maximum colour value is 255. Note: the validity of manual thresholding is still being validated as it is impacted by the brightness and contrasting of the image, unlike automatic thresholding. 
