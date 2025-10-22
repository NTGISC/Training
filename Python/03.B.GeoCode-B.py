# Place code in new notebook cell
# Add Name label
# When using a new cell if previous cell was ran you don't have to redefine variables
# Redefining required variables here in case original cell was not ran
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps()[0]
fc_name = "PeopleLocations"
layer = None
for lyr in m.listLayers():
    if lyr.name == fc_name:
        layer = lyr
        break

if layer:
    # Get CIM definition
    cim_layer = layer.getDefinition('V3')  # Use 'V2' for Pro 2.x
    
    # Enable labeling
    cim_layer.labelsVisible = True
    
    if hasattr(cim_layer, 'labelClasses') and cim_layer.labelClasses:
        for label_class in cim_layer.labelClasses:
            label_class.expression = "$feature.Name"
            label_class.visibility = True
            print("for label_class in cim_layer.labelClasses")
            # Optional: set expression engine
            label_class.expressionEngine = "Arcade"
    
    # Apply changes back to the layer
    layer.setDefinition(cim_layer)
    
    print("Labels updated using CIM access")
else:
    print("Layer not found!")

# Force refresh the active map view
activeMap = aprx.activeView
if activeMap:
    activeMap.camera = activeMap.camera  # This forces a refresh

# Save the project
aprx.save()