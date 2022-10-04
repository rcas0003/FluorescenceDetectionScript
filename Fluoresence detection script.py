from ij import WindowManager, IJ
from ij.gui import OvalRoi, WaitForUserDialog, GenericDialog
from ij.measure import ResultsTable
from ij.io import OpenDialog

# Author: Rachel Cass
# Under supervision of Jennifer Payne
# Valid for TrackMate version 7.5.1

# Get currently selected image
imp = WindowManager.getCurrentImage()
frame = imp.getNFrames()
# get frame interval
# Create results table
fluorescenceData = ResultsTable()

# Input how many ovals of interest will need to be input for this image
# 1 is the default value, returned if the user inputs an invalid number
gd = GenericDialog("ROI required: ")
gd.addNumericField("Number of oval ROI required", 1, 0)
gd.showDialog()
roiNumber = int(gd.getNextNumber())

# Select ovals of interest
for j in range(0, roiNumber):
    yolk = OvalRoi(0, 0, 350,350)
    #Monash size: 180,180
    #Boston size: 350,350
    imp.setRoi(yolk)
    WaitForUserDialog("Place oval " + str(j+1) + ":").show()

    # Set timeframe
    for i in range(1, frame+1):
        imp.setT(i)
        # Duplicate
        crop = imp.crop("slice")
        if i==1 or i==frame:
            crop.show()
        # Ensure 8 - bit
        IJ.run(crop, "8-bit", "")

        # Set threshold (triangle, B&W, Dark background) - Apply
        IJ.setAutoThreshold(crop, "Triangle dark")  # sets method as triangle & dark background setting
        IJ.run(crop, "Convert to Mask", "")  # sets mode as B&W
        # IJ.setThreshold(imp, 30, 255, "black & white")

        # Return the ROI so that the area measured is of the yolk, not the entire cropped square
        yolk = OvalRoi(0, 0, 350,350)
        crop.setRoi(yolk)

        # Measure
        roiStat = yolk.getStatistics()
        area = roiStat.area
        areaFraction = roiStat.areaFraction
        fluoroArea = (area*areaFraction)/100
        minColour = roiStat.min
        maxColour = roiStat.max

        # Load data into results table
        fluorescenceData.addRow()
        fluorescenceData.addValue('ROI', j + 1)
        fluorescenceData.addValue('TimePoint', i)
        fluorescenceData.addValue('Roi Area', area)
        fluorescenceData.addValue('White Area', fluoroArea)
        fluorescenceData.addValue('% White Area ', areaFraction)
        fluorescenceData.addValue('Min Colour', minColour)
        fluorescenceData.addValue('Max Colour', maxColour)

fluorescenceData.getResultsTable()
fluorescenceData.show('Results')

# Close and reopen file when user is done
WaitForUserDialog("Click ok when done to close file.").show()
imp.close()
# Open file again so next series can be selected
# path = OpenDialog.getLastDirectory()
# filename = OpenDialog.getLastName()
# file = path + filename
# imp = IJ.openImage(file)
# imp.show()
