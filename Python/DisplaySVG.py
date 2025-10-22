import arcpy
from IPython.display import SVG, display
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

gdb = aprx.defaultGeodatabase  # Path to the default geodatabase

# Specify the table name
table_name = "PeopleLocations_zipcodes"  # Replace with your table name
fc = f"{gdb}\\{table_name}"

# Convert the table to a NumPy array and then to a Pandas DataFrame
# List fields except geometry, geometry is object not numeric or string so it causes issues
fields = [f.name for f in arcpy.ListFields(fc) if f.type != 'Geometry']
# Add geometry tokens for X and Y
fields = fields + ["SHAPE@X", "SHAPE@Y"]
np_array = arcpy.da.TableToNumPyArray(fc, fields)
df = pd.DataFrame(np_array)

# Clean up field names
df = df.rename(columns={"SHAPE@X": "X", "SHAPE@Y": "Y"})
print(df)
print()

def tiny_svg_map(df, x="X", y="Y", size=120, margin=4, color="#1f78b4"):
    xmin, xmax = df[x].min(), df[x].max()
    ymin, ymax = df[y].min(), df[y].max()
    dx = xmax - xmin or 1
    dy = ymax - ymin or 1
    scale = (size - 2*margin)
    pts = []
    for Xv, Yv in zip(df[x], df[y]):
        sx = margin + (Xv - xmin)/dx * scale
        sy = margin + (ymax - Yv)/dy * scale  # invert y for display
        pts.append(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="2" fill="{color}" />')
    svg = f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">' + "".join(pts) + "</svg>"
    display(SVG(svg))

tiny_svg_map(df)