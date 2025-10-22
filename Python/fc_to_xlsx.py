import arcpy
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