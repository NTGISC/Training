import arcpy
import os

# Example setup
aprx = arcpy.mp.ArcGISProject("CURRENT")
gdb = aprx.defaultGeodatabase
fc_name = "PeopleLocations"
fc = os.path.join(gdb, fc_name)

# Output feature class name
copy_fc_name = "PeopleLocations_Copy"
copy_fc = os.path.join(gdb, copy_fc_name)

# Copy the feature class
arcpy.Copy_management(fc, copy_fc)

print(f"Copied {fc} to {copy_fc}")