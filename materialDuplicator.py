# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Material Duplicator",
    "author": "DESIGN3D",
    "version": (0, 2),
    "blender": (2, 80, 4),
    "location": "Node Editor > Properties > Duplicator",
    "description": "Material duplication tools",
    "category": "Node"
}

import bpy
from bpy.types import Operator, Panel

class MD_PT_DuplicatorPanel(Panel):
    bl_label = "Material Duplicator"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Duplicate"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column
        row.operator('duplicate.button')

class MD_OT_DuplicatorButton(Operator):

    '''Duplicate current Material'''
    bl_idname = 'duplicate.button'
    bl_label = 'Duplicate Material'
    
    def execute(self, context):
        
        material = bpy.context.material
        newMaterial = material.copy()
        for node in newMaterial.node_tree.nodes:
            if hasattr(node, "node_tree"):
                nodeGroup = node.node_tree.copy()
                node.node_tree = nodeGroup
                drivers = node.node_tree.animation_data.drivers
                for driv in drivers:
                    vars = driv.driver.variables
                    for var in vars:
                        targets = var.targets
                        for target in targets:
                            print(target.id.name)
                            if(target.id == material):
                                target.id = newMaterial
                                print("changed to " + target.id.name)

        return {'FINISHED'}

classes = [
    MD_PT_DuplicatorPanel,
    MD_OT_DuplicatorButton,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()