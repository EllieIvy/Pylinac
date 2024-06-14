# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:37:57 2024

@author: ellie

Program to take the central axis of two 10cm x 10cm fields with orthogonal collimator angles, find the average of the two central axes and then feed this into the picket fence test.

Plan:
1. Check whether images are orthogonal - test this
2. Test whether central coords are being detected correctly x (Tested on HBB images)
3. Calc average of coords for two images x
4. Input these coords into picket fence test x 
5. Incorporate into main program

"""
from pylinac import PicketFence, FieldAnalysis
from pylinac.core.geometry import Point
import pydicom

#Read in 10cm x 10cm image 1 and find the collimator angle.
dicom_file_path1 = r'C:\Users\ellie\OneDrive\Documents\WPy64-31230\Picket Fence Test\Images\HBB1.dcm'
ds1 = pydicom.dcmread(dicom_file_path1)
# Print the collimator angle(s)
try:
    if 'BeamLimitingDeviceAngle' in ds1:
        collimator_angle1 = ds1.BeamLimitingDeviceAngle
        print(f"Collimator Angle: {collimator_angle1} degrees")
    else:
        # For some RT Plan files, the angle might be in the Beam Sequence
        for beam in ds1.BeamSequence:
            if 'BeamLimitingDeviceAngle' in beam:
                collimator_angle1 = beam.BeamLimitingDeviceAngle
                print(f"Collimator Angle: {collimator_angle1} degrees")
            else:
                print("Collimator Angle not found in Beam Sequence.")
except AttributeError:
    print("Collimator Angle not found in the DICOM file.")

#Read in 10cm x 10cm image 2 and find the collimator angle.
dicom_file_path2 = r'C:\Users\ellie\OneDrive\Documents\WPy64-31230\Picket Fence Test\Images\HBB2.dcm'
ds2 = pydicom.dcmread(dicom_file_path2)
# Print the collimator angle(s)    
try:
    if 'BeamLimitingDeviceAngle' in ds2:
        collimator_angle2 = ds2.BeamLimitingDeviceAngle
        print(f"Collimator Angle: {collimator_angle2} degrees")
    else:
        # For some RT Plan files, the angle might be in the Beam Sequence
        for beam in ds2.BeamSequence:
            if 'BeamLimitingDeviceAngle' in beam:
                collimator_angle2 = beam.BeamLimitingDeviceAngle
                print(f"Collimator Angle: {collimator_angle2} degrees")
            else:
                print("Collimator Angle not found in Beam Sequence.")
except AttributeError:
    print("Collimator Angle not found in the DICOM file.")

#Check that coll angles are orthogonal.  Round to nearest integer and check difference is 90 or 270 degrees.
if abs(round(collimator_angle1)-round(collimator_angle2)) == 90 or abs(round(collimator_angle1)-round(collimator_angle2)) == 270:
    print("Angles are orthogonal")
else:
    print("Angles are not orthogonal") # in program, reset and ask for new file input

#Determine CAX coords for field 1
fa1 = FieldAnalysis(dicom_file_path1)
fa1.analyze()
data=fa1.results_data()
CAX1=data.beam_center_index_x_y

#Determine CAX coords for field 2
fa2 = FieldAnalysis(dicom_file_path2)
fa2.analyze()
data=fa2.results_data()
CAX2=data.beam_center_index_x_y

#Find average of two coord sets
x_avg=(CAX1[0] + CAX2[0]) / 2
y_avg=(CAX1[1] + CAX2[1]) / 2

#Define new point as the average of the two central axes.  Z will default to 0.
CAX_AVG=Point(x_avg,y_avg)
print(CAX_AVG)

# Load a Picket Fence image and analyze it with the new average central axis location
pf = PicketFence(r'C:\Users\ellie\OneDrive\Documents\WPy64-31230\Picket Fence Test\Images\PicketFence.dcm')
pf.analyze(central_axis= (CAX_AVG))
print(pf.results())
