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
# Add geometry tokens for X and Y
fields = fields + ["SHAPE@X", "SHAPE@Y"]
np_array = arcpy.da.TableToNumPyArray(table_path, fields)
df = pd.DataFrame(np_array)

# Clean up field names
df = df.rename(columns={"SHAPE@X": "X", "SHAPE@Y": "Y"})
print(df)

import matplotlib.pyplot as plt

def mini_map(df, x_col="X", y_col="Y", size=(3,3), point_size=6, alpha=0.7,
             frame=False, dpi=120, out_file=None):
    plt.figure(figsize=size, dpi=dpi)
    plt.scatter(df[x_col], df[y_col], s=point_size, c="#1f78b4", alpha=alpha, edgecolors="none")
    if not frame:
        plt.axis('off')
    else:
        plt.xlabel("X")
        plt.ylabel("Y")
    # Pad the extent a bit
    xmin, xmax = df[x_col].min(), df[x_col].max()
    ymin, ymax = df[y_col].min(), df[y_col].max()
    dx = (xmax - xmin) * 0.05 if xmax > xmin else 1
    dy = (ymax - ymin) * 0.05 if ymax > ymin else 1
    plt.xlim(xmin - dx, xmax + dx)
    plt.ylim(ymin - dy, ymax + dy)
    if out_file:
        plt.savefig(out_file, bbox_inches="tight", pad_inches=0)
    plt.show()

mini_map(df)                # show inline (notebook)
# mini_map(df, out_file="mini_map.png")   # save for outside notebook