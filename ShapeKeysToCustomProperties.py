### Create Custom Properties on an Armature that drive all Shape Keys on its Child Mesh ###

# Select the Mesh with the Shape Keys on it, then select the Armature that is to hold 
# the Custom Properties with which you are going to drive the ShapeKeys and run

import bpy

# Variable Definition
context = bpy.context
obj = bpy.context.object
active_obj = bpy.context.active_object
selected_obj = bpy.context.selected_objects
other_obj =  [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
active_bone = bpy.context.active_pose_bone
active_bone_name = active_bone.name
key_number = len(other_obj[0].data.shape_keys.key_blocks)

## Go through Selected Objects and assign the Mesh Object to a variable
#for s in selected_obj:
#    if selected_obj[s].type == 'MESH':
#        other_obj = selected_obj[s]
#        return other_obj
#        break

# Error in case Selection does not meet requirements
def error_selection(self, context):
    self.report({'INFO'}, 'Incorrect Object Selection: Please Select a Mesh Object followed by an Armature Object')
    return {'FINISHED'}

# Check for Object type: Active Object: Armature, Selected Object: Mesh
if len(selected_obj) == 2 and active_obj.type == 'ARMATURE' and other_obj[0].type == 'MESH':

    # If other objects are in selection: return Error
    for things in selected_obj:

        # Iterate over ShapeKey List, Store Names, Add Properties to Active Object, 
        for i in range(key_number):
            # Access RNA_UI Dictionary, create if it does not exist
            if "_RNA_UI" not in other_obj[0].keys():
                other_obj[0]['_RNA_UI'] = {}
            obj_rna_ui = other_obj[0].get('_RNA_UI')
            
            # Store ShapeKey Name
            name_shapekey = other_obj[0].data.shape_keys.key_blocks[i].name
            # Add Property with ShapeKey's name to Active PoseBone and set Value to 0
            active_bone[name_shapekey] = 0.0
            # Add Custom Properties to RNA_UI dictionary, fill values
            obj_rna_ui[name_shapekey] = {
                        "default": 0.0,
                        "min":0.0,
                        "max":1.0, 
                        "soft_min":0,
                        "soft_max":1,
                        "description":"Shape Key Influence"
                        }

            # Add the Drivers to the ShapeKeys Value Field, so ttheir influence can be controlled via Custom Properties                  
            driver = other_obj[0].data.shape_keys.key_blocks[i].driver_add("value").driver
            # Create new input Variable for driver
            driver_var = driver.variables.new()
            # Set number of Variables in the driver stack, since there is only one, that is 0
            target = driver_var.targets[0]
            # Set the Target object for the Driver's Variable Input, i.e. the Armature Object, where the input sliders are
            target.id = active_obj
            # Set the drivers Data Path, i.e. the RNA Path to the Property it uses as input
            target.data_path = "pose.bones"+"["+"\""+active_bone.name+"\""+"]"+"[" +"\""+ name_shapekey + "\"" +"]"
            # Set the Expression Field of the Driver, in this case with only the variable name
            driver.expression = driver_var.name

    # Set ShapeKey Startup Value
    other_obj[0][name_shapekey] = 0.0

    # property attributes.for UI
    # redraw Properties panel
    for window in bpy.context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()
                break

else:
    print("Incorrect Object Selection: Please Select a Mesh Object followed by an Armature Object")
#     error_selection(self, context)
