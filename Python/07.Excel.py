import arcpy
import datetime
import os
import pandas as pd

def fc_to_xlsx(fc_path, xlsx_path):
    """
    Export a feature class to an XLSX file.
    Geometry is exported as WKT.
    """
    # List fields
    fields = [f.name for f in arcpy.ListFields(fc_path) if f.type not in ("Geometry", "OID")]
    # Add geometry as WKT
    fields_with_geom = fields + ["SHAPE@WKT"]
    
    # Read features
    rows = []
    with arcpy.da.SearchCursor(fc_path, fields_with_geom) as cursor:
        for row in cursor:
            row_dict = {field: value for field, value in zip(fields, row[:-1])}
            row_dict["geometry"] = row[-1]  # WKT
            rows.append(row_dict)
    
    # Write to Excel
    df = pd.DataFrame(rows)
    df.to_excel(xlsx_path, index=False)
    print(f"Saved {fc_path} to {xlsx_path}")

# Example usage
# fc_to_xlsx(r"C:\path\to\your.gdb\PeopleLocations", r"C:\output\PeopleLocations.xlsx")

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

# Get feature class
gdb = aprx.defaultGeodatabase
fc_name = "PeopleLocations"
fc = os.path.join(gdb, fc_name)

# Export to XLSX
stringdate = datetime.datetime.now().strftime('%Y_%m_%d_%H.%M.%S%f')
# Create c:\temp if it doesn't exist
if not os.path.exists(r"C:\temp"):
    os.makedirs(r"C:\temp")
fc_to_xlsx(fc, f"C:/temp/PeopleLocations_{stringdate}.xlsx")