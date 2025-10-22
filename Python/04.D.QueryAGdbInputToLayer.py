# Recommend running in ArcGIS Pro Python Notebook
# Clear previous notebook if opening with previous cell code, by closing notebook and reopening
import arcpy
import os

try:
    # Try to connect to the CURRENT project (works in ArcGIS Pro, including notebooks)
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    print("Using CURRENT project (inside ArcGIS Pro).")
except Exception:
    # Fall back to using a specific project path (external script environment)
    # ALWAYS Replace aprx filepath with your project's path
    project_path = r"C:\Code\Clients\TribalGIS\Ecourses\PythonLive\ArcGISProProjects\03GeoCode\03GeoCode.aprx"
    arcpy.env.workspace = project_path
    aprx = arcpy.mp.ArcGISProject(project_path)
    print("Using saved project file (external editor).")

# Get the first map in the project
m = aprx.listMaps()[0]

# Get feature class
gdb = aprx.defaultGeodatabase
fc_name = "PeopleLocations"
fc = os.path.join(gdb, fc_name)

# 1) Find a map layer that points to the same feature class
lyr = None
for L in m.listLayers():
    try:
        # Describe(L).catalogPath equals the dataset path for feature layers
        # print(arcpy.Describe(L).catalogPath)
        if arcpy.Describe(L).catalogPath == fc:
            lyr = L
            print(f"Found layer: {lyr.name}")
            break
    except Exception:
        # some layer types may not have catalogPath; ignore those
        pass

# 2) If not found, add the feature class to the map
if lyr is None:
    m.addDataFromPath(fc)
    # refresh our reference to the newly-added layer
    for L in m.listLayers():
        try:
            if arcpy.Describe(L).catalogPath == fc:
                lyr = L
                break
        except Exception:
            pass

if lyr is None:
    raise RuntimeError(f"Could not find or add a layer for {fc}")
    exit()

# Get field names
desc = arcpy.Describe(lyr)  # Describe returns metadata about the layer/feature class
oid_field = desc.OIDFieldName
geom_field = desc.shapeFieldName
field_names = [f.name for f in arcpy.ListFields(fc)]
print(f"Field names: {field_names}")
# create index lookup once
idx = {fname: i for i, fname in enumerate(field_names)}

arcpy.management.SelectLayerByAttribute(lyr, "CLEAR_SELECTION")

# Query the fc
# Ask user to enter a name to query
user_entered_name = input("Enter the name (or part of it) to query: ")
# Ensure the name is properly formatted for the query
user_entered_name = user_entered_name.strip().replace("'", "''")  # Escape single quotes
query = f"UPPER(Name) LIKE '%{user_entered_name.upper()}%'"  # LIKE % for partial match
print(f"{query=}")
with arcpy.da.SearchCursor(fc, "*", where_clause=query) as cursor:  # using "*" to get all fields
    for row in cursor:
        geometry = row[idx[geom_field]]
        name = row[idx["Name"]]
        city = row[idx["City"]]
        state = row[idx["State"]]
        print(f"Found {name} in {city}, {state} at location [{geometry[0]}, {geometry[1]}]")
        # Select the feature (need to select it in lyr, not fc)
        querylyr = f"{oid_field} = {row[idx[oid_field]]}"  # Use OID for selection
        print(f"{querylyr=}")
        arcpy.management.SelectLayerByAttribute(lyr, "ADD_TO_SELECTION", querylyr)
        print(f"Selected feature for {name}.")

# Zoom to the selected feature(s)
aprx.activeView.zoomToAllLayers(True)
print(f"Zoomed to selected features.")