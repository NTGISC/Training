# Recommend running in ArcGIS Pro Python Notebook
# Clear previous notebook if opening with previous cell code, by closing notebook and reopening
import arcpy

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

fc_name = "PeopleLocations"

# Get the layer by name
layer = None
for lyr in m.listLayers():
    if lyr.name == fc_name:
        layer = lyr
        break

if not layer:
    print(f"Layer '{fc_name}' not found in the map.")
    exit()

# Query the layer
arcpy.management.SelectLayerByAttribute(layer, "CLEAR_SELECTION")  # to ensure query iterates all records
# Ask user to enter a name to query
user_entered_name = input("Enter the name to query: ")
# Ensure the name is properly formatted for the query
user_entered_name = user_entered_name.strip().replace("'", "''")  # Escape single quotes
query = f"UPPER(Name) = '{user_entered_name.upper()}'"  # Using upper() to ensure case-insensitivity
print(f"{query=}")
# ["SHAPE@", "Name", "City", "State"] are the fields to retrieve
with arcpy.da.SearchCursor(layer, ["SHAPE@", "Name", "City", "State"], where_clause=query) as cursor:
    for row in cursor:
        geometry = row[0]
        name = row[1]
        city = row[2]
        state = row[3]
        print(f"Found {name} in {city}, {state} at location [{geometry.centroid.X}, {geometry.centroid.Y}]")
        # Select the feature in the layer
        arcpy.management.SelectLayerByAttribute(layer, "NEW_SELECTION", query)
        print(f"Selected feature for {name}.")
        # Zoom to the selected feature
        aprx.activeView.zoomToAllLayers(True)
        print(f"Zoomed to {name}'s location.")
        break  # Exit after finding the first match