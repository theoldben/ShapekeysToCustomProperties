### Create Custom Properties on an Armature that drive all Shape Keys on its Child Mesh ###

# Select the Mesh with the Shape Keys on it, then select the Armature that is to hold 
# the Custom Properties with which you are going to drive the ShapeKeys and run

import bpy

# Variable Definition
context = bpy.context
obj = bpy.context.object
active_obj = bpy.context.active_object
selected_obj = bpy.context.selected_objects
other_obj = ""
key_number = len(bpy.context.object.data.shape_keys.key_blocks)

# Go through Selected Objects and assign the Mesh Object to a variable
for s in selected_obj:
    if selected_obj[s].type == 'MESH':
        other_obj = selected_obj[s]
        return other_obj
        break

# Error in case Selection does not meet requirements
def error_selection(self, context):
    self.report({'INFO'}, 'Incorrect Object Selection: Please Select a Mesh Object followed by an Armature Object')
    return {'FINISHED'}

# Check for Object type: Active Object: Armature, Selected Object: Mesh
if len(selected_obj) == 2 and active_obj.type == 'ARMATURE' and other_obj.type == 'MESH':

    # If other objects are in selection: return Error
    for things in selected_obj:

        # Iterate over ShapeKey List, Store Names, Add Properties to Active Object, 
        for i in key_number:
            obj_rna_ui = obj.get('_RNA_UI')
            # Store ShapeKey Name
            varI = bpy.context.object.data.shape_keys['Key'].key_blocks[i].name
            # Add Property with ShapeKey's name to Active Object and set Value to 0
            obj[varI] = 0.0
            # Add Custom Properties, fill values
            obj_rna_ui[varI] = {
                        "default": 0.0,
                        "min":0.0,
                        "max":1.0, 
                        "soft_min":0,
                        "soft_max":1,
                        "description":"Shape Key Influence"
                        }

            # Add the Drivers to the ShapeKeys so they can be controlled via Custom Properties                  
            driver = bpy.context.object.data.shape_keys['Key'].key_blocks[i].driver_add("value").driver
            # Create new input Variable for driver
            driver_var = driver.variables.new()
            # Set number of Variables in the driver stack, since there is only one, that is 0
            target = driver_var.targets[0]
            # Set the Target object for the Driver's Variable Input, i.e. the Mesh Object
            target.id = other_obj
            # Set the drivers Data Path, i.e. the RNA Path to the Property it uses as input
            target.data_path = "[" +"\""+ varI + "\"" +"]"
            # Set the Expression Field of the Driver, in this case with only the variable name
            driver.expression = driver_var.name

    # Set ShapeKey Startup Value
    obj[varI] = 0.0

    # property attributes.for UI
    # redraw Properties panel
    for window in bpy.context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()
                break

else error_selection()
