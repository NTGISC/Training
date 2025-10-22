import arcpy
import pandas as pd

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

map = aprx.listMaps()[0]  # Get the first map in the project
gdb = aprx.defaultGeodatabase  # Path to the default geodatabase

# Specify the table name
table_name = "PeopleLocations_zipcodes"  # Replace with your table name
table_path = f"{gdb}\\{table_name}"

# Convert the table to a NumPy array and then to a Pandas DataFrame
# List fields except geometry, geometry is object not numeric or string so it causes issues
fields = [f.name for f in arcpy.ListFields(table_path) if f.type != 'Geometry']

data = []

# Add geometry tokens directly
data = arcpy.da.FeatureClassToNumPyArray(
    table_path,
    field_names = fields + ["SHAPE@X", "SHAPE@Y"],
    skip_nulls = False,          # Keep rows with NULLs
    null_value = None            # Use None for NULLs (avoids masked arrays)
)
"""
# Add geometry as SHAPE@XY to cursor fields
cursor_fields = fields + ["SHAPE@XY"]

# Extract rows
with arcpy.da.SearchCursor(table_path, cursor_fields) as cursor:
    for row in cursor:
        row_dict = dict(zip(fields, row[:-1]))  # All non-geometry fields
        row_dict['X'], row_dict['Y'] = row[-1]  # Unpack XY
        data.append(row_dict)
"""
# Display the DataFrame
df = pd.DataFrame(data)
print(df)