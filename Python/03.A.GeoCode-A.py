# Recommend running in ArcGIS Pro Python Notebook
import arcpy
from arcgis.geocoding import geocode

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

# List of people with name, city, state, feel free to add more
people = [
    {"name": "YourName", "city": "St Louis", "state": "MO"},
    {"name": "YourNeighborName", "city": "Kansas City", "state": "MO"}
]

# Print greetings
print("Hello")
for person in people:
    print(f"{person['name']} from {person['city']}, {person['state']}")

# Geocode each city/state and collect results
features = []
for person in people:
    query = f"{person['city']}, {person['state']}"
    results = geocode(address=query, max_locations=1, as_featureset=True)
    if len(results.features) > 0:
        pt = results.features[0]
        pt.attributes['Name'] = person['name']
        pt.attributes['City'] = person['city']
        pt.attributes['State'] = person['state']
        features.append(pt)
    else:
        print(f"Could not geocode {query}")

# Create a new point feature class in a file geodatabase
gdb = aprx.defaultGeodatabase
print(f"{gdb=}")
fc_name = "PeopleLocations"
fc = arcpy.management.CreateFeatureclass(gdb, fc_name, "POINT", spatial_reference=4326)[0]

# Add fields for name, city, state
arcpy.management.AddField(fc, "Name", "TEXT", field_length=50)
arcpy.management.AddField(fc, "City", "TEXT", field_length=50)
arcpy.management.AddField(fc, "State", "TEXT", field_length=50)

# Insert the points
with arcpy.da.InsertCursor(fc, ["SHAPE@XY", "Name", "City", "State"]) as cursor:
    for feat in features:
        x, y = feat.geometry['x'], feat.geometry['y']
        name = feat.attributes['Name']
        city = feat.attributes['City']
        state = feat.attributes['State']
        cursor.insertRow([(x, y), name, city, state])

print("Points added to feature class:", fc)

# Add the feature class to the map
m.addDataFromPath(fc)
print("Feature class added to map.")

# Save project changes
aprx.save()
print("Project updated and saved.")