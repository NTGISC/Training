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

# Query the fc
# Ask user to enter a name to query
user_entered_name = input("Enter the name (or part of it) to query: ")
# Ensure the name is properly formatted for the query
user_entered_name = user_entered_name.strip().replace("'", "''")  # Escape single quotes
query = f"UPPER(Name) LIKE '%{user_entered_name.upper()}%'"  # LIKE % for partial match
print(f"{query=}")
# ["SHAPE@", "Name", "City", "State"] are the fields to retrieve
with arcpy.da.SearchCursor(fc, ["SHAPE@", "Name", "City", "State"], where_clause=query) as cursor:
    for row in cursor:
        geometry = row[0]
        name = row[1]
        city = row[2]
        state = row[3]
        print(f"Found {name} in {city}, {state} at location [{geometry.centroid.X}, {geometry.centroid.Y}]")