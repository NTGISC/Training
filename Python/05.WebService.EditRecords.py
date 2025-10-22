import arcpy
import os
import requests

def get_zipcode(lat, lon):
    """
    Returns the zipcode for given latitude and longitude using OpenStreetMap's Nominatim API.
    This service is free and does not require a login.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        str: Zipcode if found, else None
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "zipcode-fetcher-example"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Zipcode may be under 'postcode' in address
        return data.get("address", {}).get("postcode")
    except Exception as e:
        print(f"Error: {e}")
        return None

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
fc_orig = os.path.join(gdb, fc_name)

# copy feature class, if it doesn't exist
fc = os.path.join(gdb, f"{fc_name}_zipcodes")
if not arcpy.Exists(fc):
    arcpy.Copy_management(fc_orig, fc)
    print(f"Copied {fc_orig} to {fc}")

# Add field Zipcode if it doesn't exist
field_names = [f.name for f in arcpy.ListFields(fc)]
if "Zipcode" not in field_names:
    arcpy.AddField_management(fc, "Zipcode", "TEXT", field_length=10)
    print("Added field 'Zipcode'.")

# Open an UpdateCursor to edit zipcode and loop thru features
with arcpy.da.UpdateCursor(fc, ["SHAPE@", "Zipcode"]) as cursor:  # with takes care of cleanup for you
    for row in cursor:
        point_geom = row[0]  # SHAPE@ returns geometry object
        x = point_geom.centroid.X
        y = point_geom.centroid.Y
        print(f"Feature at X: {x}, Y: {y}")

        zipcode = get_zipcode(y, x)  # Note: Nominatim uses lat, lon order
        if zipcode:
            print(f"Found zipcode: {zipcode}")
            row[1] = zipcode
            cursor.updateRow(row)

print("Finished updating zipcodes.")