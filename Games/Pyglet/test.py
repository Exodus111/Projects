#!BPY

"""
Name: 'InnerWorld'
Blender: 247
Group: 'Add'
Tooltip: 'A wizard for creating terrains.'
"""

__author__ = 'Nostalghia'
__version__ = '0.0.7' # 
__url__ = ["Innerworld homepage, http://innerworld.sourceforge.net", "Support forum, http://sourceforge.net/tracker/?atid=725228&group_id=132755&func=browse", "blender", "elysiun"]
__bpydoc__ = """\
Inner World is a landscape generator running inside Blender.

Terrains are generated from Blenders internal noise functions and external height fields. Using a graph editor different noise sources and operators can be used to define a production line for the mesh creation.<br>

Usage:<br>
        Please read tutorial at http://innerworld.sourceforge.net/firstSteps.html<br>

        InnerWorld has a graph base approach for generating terrains. You produce the mesh by building an acyclic graph to evaluate the hight of every mesh point. There are different types of nodes: data sources, operators, and data sinks. A graph needs exactly one sink connected to one ore more sources to produce an mesh.

Known issues:<br>
        This is an alfa release of InnerWorld.<br>
        Parts of the required functionality are not implemented yet.
"""

#------------------------------------------------------------------------
# Landscape generator for blender 2.36 and above
#
# Homepage: http://innerworld.sourceforge.net"
#
# Author: Thomas Jourdan
#------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2005 - 2009: Thomas Jourdan
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****

# pylint: disable-msg=C0103
# pylint: disable-msg=C0111
# pylint: disable-msg=C0301
# pylint: disable-msg=W0613
# pylint: disable-msg=W0312

print("***** BEGIN GPL LICENSE BLOCK for plugin InnerWorld *****")
print("InnerWorld " + __version__ + " http://innerworld.sourceforge.net")
print("Copyright (C) 2005 - 2009: Thomas Jourdan")
print("")
print("This program is free software; you can redistribute it and/or")
print("modify it under the terms of the GNU General Public License")
print("as published by the Free Software Foundation; either version 2")
print("of the License, or (at your option) any later version.")
print("")
print(" This program is distributed in the hope that it will be useful,")
print(" but WITHOUT ANY WARRANTY; without even the implied warranty of")
print(" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
print(" GNU General Public License for more details.")
print("")
print(" You should have received a copy of the GNU General Public License")
print(" along with this program; if not, write to the Free Software Foundation,")
print(" Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.")
print("***** END GPL LICENSE BLOCK for plugin InnerWorld *****")

try:
    import Blender
    import Blender.Draw
    import Blender.BGL
    import Blender.Mathutils
    import bpy
    import Blender.Object
    import Blender.Registry
except ImportError:
    print("missing import Blender")

import math
try:
    import webbrowser
except ImportError:
    print("missing import webbrowser")
import sys, traceback
import time
sys.path.append(".")
import IwNodeView
import IwEvaluator
import IwProcessingNode
import IwPick
import IwPlacement

# ----- constant -----
iwPrefix = "iw"

# ----- global variables -----
mouseX = mouseY = moveX = moveY = leftMouseX = leftMouseY = 0
isShiftPressed = isDraged = 0
pnode1 = None
activeButton = []
lastFilename = None
quickScale = 2
quotaButton = None

# ----- mesh generation -----
def newMesh():
    global quickScale
    editmode = Blender.Window.EditMode()    # are we in edit mode?  If so ...
    if editmode:
        Blender.Window.EditMode(0)     # leave edit mode before getting the mesh
    #print "Mesh.Get()", Blender.Mesh.Get()
    scene = bpy.data.scenes.active
    mx = 1
    for pnode in IwProcessingNode.getSinkList():
#        if running and pnode.isInvalid():
        if pnode.isInvalid():
            print("new mesh from node " + str(pnode.id) + " " + pnode.evaluator.info["headline"])
            mxx = IwProcessingNode.str1(mx)
            objName = iwPrefix + 'Terrain' + mxx
            meshName = iwPrefix + 'Mesh' + mxx
            vertices, faces = pnode.newMeshData(quickScale)
            obj = ifExists(scene.objects, objName)
            if not obj:
                # create a new mesh
                mesh = bpy.data.meshes.new(meshName)
                obj = scene.objects.new(mesh, objName)
                obj.link(mesh)
            else:
                # patch existing mesh
                mesh = obj.getData(mesh=True)
                oldMaterials = mesh.materials
                #print "coloring: ", pnode.evaluator.coloring
                #print "mesh.materials 1: ", oldMaterials
                mesh.verts = None
                if pnode.evaluator.coloring == 0:
                    #preserve materials
                    for material in oldMaterials:
                        mesh.materials += [material]
                #print "mesh.materials 2: ", mesh.materials
            mesh.verts.extend(vertices)   # add vertices to mesh
            mesh.faces.extend(faces)      # add faces to the mesh (also adds edges)
    
            mesh.sel = True
            if (pnode.evaluator.look % 2) == 1:
                mesh.quadToTriangle()
            if pnode.evaluator.look <= 1:
                for face in mesh.faces:
                    face.smooth = True
            mesh.calcNormals()
    
            if pnode.evaluator.coloring == 1:
                #add solid color
                material = linkDataObject(bpy.data.materials, iwPrefix + 'SolidColor', mx)
                material.rgbCol = pnode.evaluator.SolidColor
                material.specCol = pnode.evaluator.SpecularColor
                material.mirCol = [0.0, 0.0, 0.0]
                mesh.materials += [material]
                
            if pnode.evaluator.coloring == 2:
                #add colorband
                texture = linkDataObject(bpy.data.textures, iwPrefix + 'GradientTexture', mx)
                texture.setType('Blend')
                texture.flags = Blender.Texture.Flags.COLORBAND
                texture.colorband = pnode.evaluator.colorband()
    
                material = linkDataObject(bpy.data.materials, iwPrefix + 'GradientColor', mx)
                material.specCol = pnode.evaluator.SpecularColor
                material.mirCol = [0.0, 0.0, 0.0]
                material.setTexture(0, texture, Blender.Texture.TexCo.ORCO, Blender.Texture.MapTo.COL)
                mtex = material.getTextures()[0]
                mtex.xproj = Blender.Texture.Proj.Z
                mtex.yproj = Blender.Texture.Proj.NONE
                mtex.zproj = Blender.Texture.Proj.NONE
                mesh.materials += [material]
    
            if pnode.evaluator.coloring == 3:
                #add vertex color layer for baked face colors.
                mesh.vertexColors = True
                mesh.faceUV = True
                for face in mesh.faces:
                    for vx, v in enumerate(face):
                        no = v.no
                        col = face.col[vx]
                        col.r = int((no.x+1)*128)
                        col.g = int((no.y+1)*64)
                        col.b = int((no.z+1)*32)
                material = linkDataObject(bpy.data.materials, iwPrefix + 'VertexColor', mx)
                material.setMode('VColPaint') 
                mesh.materials += [material]
            
            mesh.update()
            obj.makeDisplayList()
            
#            scene.objects.selected = []
#            obj.sel = 1
#            for xTile in xrange(-2, 2+1):
#                if not xTile == 0:
#                    tileName = objName + 'x' + str(xTile)
#                    for dupliObject in filter(lambda o: o.name.startswith(tileName), scene.objects):
#                        print "unlink", dupliObject.name, dupliObject.getData(name_only=True, mesh=False)
#                        scene.objects.unlink(dupliObject)
#                    Blender.Object.Duplicate()
#                    activeObject = scene.objects.active
#                    activeObject.name = objName + 'x' + str(xTile)
#                    activeObject.LocX = ((xTile + 1) / 2) * 2.0
#                    activeObject.SizeX = 1.0 - (2 * (xTile % 2))

        mx += 1
    if editmode:
        Blender.Window.EditMode(editmode)  # optional, just being nice
#    Blender.Window.RedrawAll()

def linkDataObject(container, nameSchema, mx):
    name = nameSchema + IwProcessingNode.str1(mx)
    dataObject = ifExists(container, name)
    if not dataObject:
        dataObject = container.new(name)
    return dataObject

def ifExists(container, name):
    for element in container:
        if element.name == name:
            return element
    return None

def ifExistsPrefix(container, prefix):
    for element in container:
        #print element.name
        if element.name == prefix or element.name.startswith(prefix + "."):
            return element
    return None


def duplicateMasterObjects():
    scene = bpy.data.scenes.active
    originalActiveObject = scene.objects.active

    # remove orphaned duplicated objects formerly created by now deleted nodes
    for pnode in [n for n in IwProcessingNode.cleanupList if n.evaluator.info["type"] == IwEvaluator.typeSink and n.evaluator.info["subtype"] == IwEvaluator.subtypeObjDupli]:
        iwDupliPrefix = iwPrefix + "{" + str(pnode.id) + "}"
        for dupliObject in [o for o in scene.objects if o.name.startswith(iwDupliPrefix)]:
            print("unlink", dupliObject.name, dupliObject.getData(name_only=True, mesh=False))
            scene.objects.unlink(dupliObject)

    # duplicate objects
    for pnode in IwProcessingNode.getSinkList(IwEvaluator.subtypeObjDupli):
        if pnode.isInvalid():
            print("new placement from node " + str(pnode.id) + " " + pnode.evaluator.info["headline"])
            iwDupliPrefix = iwPrefix + "{" + str(pnode.id) + "}"
            # remove duplicated objects created formerly by InnerWorld
            for dupliObject in [o for o in scene.objects if o.name.startswith(iwDupliPrefix)]:
                # print "unlink", dupliObject.name, dupliObject.getData(name_only=True, mesh=False)
                scene.objects.unlink(dupliObject)
    
            # search master object
            masterObject = None
            #print "masterObjectName=", pnode.evaluator.masterObjectName, "originalActiveObject=", originalActiveObject
            if pnode.evaluator.masterObjectName == "":
                if originalActiveObject:
                    # the active object of this scene is used as master for Duplicate()
                    pnode.evaluator.masterObjectName = originalActiveObject.name
                    masterObject = originalActiveObject
            else:
                # the object selected by the evaluator is used as master for Duplicate()
                for object in [o for o in scene.objects if not o.name.startswith(iwPrefix)]:
                    if object.name == pnode.evaluator.masterObjectName:
                        scene.objects.active = object
                        masterObject = object
                        break
    
            if masterObject:
                # duplicate master object
                dupliName = iwDupliPrefix + masterObject.name
                #print "master",  pnode.evaluator.masterObjectName, "active object", scene.objects.active.name
                positions, sizes, rotations = pnode.newDupliData(masterObject.getSize("worldspace"))
                scene.objects.selected = []
                masterObject.sel = 1
                for ox, objPosition in enumerate(positions):
                    Blender.Object.Duplicate()
                    activeObject = scene.objects.active
                    activeObject.name = dupliName + IwProcessingNode.str3(ox)
                    activeObject.setLocation(objPosition[0], objPosition[1], objPosition[2])
                    objSize = sizes[ox]
                    activeObject.setSize(objSize[0], objSize[1], objSize[2])
                    objRotate = rotations[ox]
                    activeObject.RotX = objRotate[0]
                    activeObject.RotY = objRotate[1]
                    activeObject.RotZ = objRotate[2]
                    if IwNodeView.check_contract:
                        if math.fabs(activeObject.LocX) > 1000  or math.fabs(activeObject.LocY) > 1000  or math.fabs(activeObject.LocZ) > 1000: raise AssertionError
                        if math.fabs(activeObject.RotX) > 1000  or math.fabs(activeObject.RotY) > 1000  or math.fabs(activeObject.RotZ) > 1000: raise AssertionError
                        if math.fabs(activeObject.SizeX) > 1000 or math.fabs(activeObject.SizeY) > 1000 or math.fabs(activeObject.SizeZ) > 1000: raise AssertionError
    
                # restore scene and set master object for evaluator
                scene.objects.selected = []
                try:
                    if originalActiveObject:
                        originalActiveObject.sel = 1
                        scene.objects.active = originalActiveObject
                except:
                    print("Can not select object: ", originalActiveObject.name)
                    pass

def updatePreview():
    for pnode in [item for item in IwProcessingNode.pnList if item.isInvalid()]:
        updatePreviewImage(pnode)        

def updatePreviewImage(pnode):
    pnode.preview = Blender.BGL.Buffer(Blender.BGL.GL_FLOAT, [pnode.u, pnode.v, 1])
    pnode.updateNodePreview()

# ----- 
def localizeMouse():
    size = Blender.BGL.Buffer(Blender.BGL.GL_FLOAT, 4)
    Blender.BGL.glGetFloatv(Blender.BGL.GL_SCISSOR_BOX, size)
    size = size.list
    return mouseX-int(size[0]), mouseY-int(size[1])

def activateNode(pnode):
    global activeButton
    activeButton = []
    for param in pnode.evaluator.info["param"]:
        if param["ui"] == IwEvaluator.uiColorWeight or param["ui"] == IwEvaluator.uiColor:
            activeButton.append(Blender.Draw.Create("0.5, 0.5, 0.0"))
        elif param["ui"] == IwEvaluator.uiObjectSelect:
            activeButton.append(Blender.Draw.Create(indexOfObject(getattr(pnode.evaluator, param["name"]))))
        else:
            activeButton.append(Blender.Draw.Create(getattr(pnode.evaluator, param["name"])))

# ----- draw gui -----
def drawNode(pnode):
    # draw preview
    Blender.BGL.glRasterPos2i(pnode.x, pnode.y)
    if "preview" in pnode.__dict__ and pnode.preview is not None:
        Blender.BGL.glDrawPixels(pnode.u, pnode.v, Blender.BGL.GL_LUMINANCE, Blender.BGL.GL_FLOAT, pnode.preview)
    
    controlLines = (len(pnode.evaluator.controls)+3)/4
    # draw control connection areas
    Blender.BGL.glColor3f(0.73, 0.73, 0.73)
    Blender.BGL.glRecti(pnode.x, pnode.y-1, pnode.x+pnode.u, pnode.y-controlLines*IwNodeView.nodeControlAreaHight)
    mix = mpx = mpy = 0
    for evcp in pnode.evaluator.controls:
        if (mix % 4) == 0:
            if not mix == 0:
                Blender.BGL.glColor3f(0.53, 0.53, 0.53)
                Blender.BGL.glBegin(Blender.BGL.GL_LINE_STRIP)
                Blender.BGL.glVertex2i(pnode.x-1,         pnode.y-mpy-1)
                Blender.BGL.glVertex2i(pnode.x+pnode.u+1, pnode.y-mpy-1)
                Blender.BGL.glEnd()
            mpx = 0
            mpy += IwNodeView.nodeControlAreaHight
        else:
            mpx += IwNodeView.nodeControlIncrement
        if not ((mix % 4) == 0):
            Blender.BGL.glColor3f(0.53, 0.53, 0.53)
            Blender.BGL.glBegin(Blender.BGL.GL_LINE_STRIP)
            Blender.BGL.glVertex2i(pnode.x+mpx, pnode.y-mpy+IwNodeView.nodeControlAreaHight)
            Blender.BGL.glVertex2i(pnode.x+mpx, pnode.y-mpy)
            Blender.BGL.glEnd()
        if pnode.evaluator.connectedControls[mix]:
            Blender.BGL.glColor3f(0.0, 0.53, 0.73)
        else:
            Blender.BGL.glColor3f(0.0, 0.0, 0.0)
        Blender.BGL.glRasterPos2i(pnode.x+mpx+2, pnode.y-mpy+1)
        if "abbreviation" in pnode.evaluator.info["param"][evcp]:
            abbreviation = pnode.evaluator.info["param"][evcp]["abbreviation"]
        else:
            abbreviation = pnode.evaluator.info["param"][evcp]["name"][0:2]
        Blender.Draw.Text(abbreviation)
        mix += 1

    # draw headline
    Blender.BGL.glColor3f(0.73, 0.73, 0.73)
    Blender.BGL.glRecti(pnode.x, pnode.y+pnode.v+1, pnode.x+pnode.u, pnode.y+pnode.v+IwNodeView.nodeControlAreaHight)
    Blender.BGL.glColor3f(0.0, 0.0, 0.0)
    Blender.BGL.glRasterPos2i(pnode.x+1, pnode.y+pnode.v+2)
    Blender.Draw.Text(pnode.evaluator.info["headline"])

    # draw border
    Blender.BGL.glBegin(Blender.BGL.GL_LINE_LOOP)
    if pnode.active:
        Blender.BGL.glColor3f(1.0, 1.0, 0.0)
    elif pnode.selected:
        Blender.BGL.glColor3f(1.0, 0.53, 0.0)
    else:
        Blender.BGL.glColor3f(0.53, 0.53, 0.53)
    Blender.BGL.glVertex2i(pnode.x-1,         pnode.y-mpy-2)
    Blender.BGL.glVertex2i(pnode.x+pnode.u+1, pnode.y-mpy-2)
    Blender.BGL.glVertex2i(pnode.x+pnode.u+1, pnode.y+pnode.v+IwNodeView.nodeControlAreaHight+1)
    Blender.BGL.glVertex2i(pnode.x-1,         pnode.y+pnode.v+IwNodeView.nodeControlAreaHight+1)
    Blender.BGL.glEnd()

def drawArrow(x1, y1, x2, y2, cr, cg, cb):
    alfa = math.atan2(y2-y1, x2-x1)
    tailLen = 12
    op = 0.45
    x2 = (x2+x1) / 2 
    y2 = (y2+y1) / 2
    Blender.BGL.glBegin(Blender.BGL.GL_POLYGON)
    Blender.BGL.glColor3f(cr, cg, cb)
    Blender.BGL.glVertex2i(x2, y2)
    Blender.BGL.glVertex2f(x2-int(tailLen*math.cos(alfa+op)), y2-int(tailLen*math.sin(alfa+op)))
    Blender.BGL.glVertex2f(x2-int(tailLen*math.cos(alfa-op)), y2-int(tailLen*math.sin(alfa-op)))
    Blender.BGL.glEnd()

def drawGraphGui():
    Blender.BGL.glClearColor(0.66, 0.66, 0.66, 1)
    Blender.BGL.glClear(Blender.BGL.GL_COLOR_BUFFER_BIT)

    # draw input connections between nodes
    for pnode in IwProcessingNode.pnList:
        for pnode2 in pnode.inputs:
            Blender.BGL.glBegin(Blender.BGL.GL_LINES)
            if pnode.selectedInput == pnode2:
                Blender.BGL.glColor3f(1.0, 1.0, 0.0)
            else:
                Blender.BGL.glColor3f(0.73, 0.53, 0.0)
            x1, y1 = pnode2.x+pnode.u, pnode2.y+pnode.v/2
            x2, y2 = pnode.x, pnode.y+pnode.v/2
            Blender.BGL.glVertex2i(x1, y1)
            Blender.BGL.glVertex2i(x2, y2)
            Blender.BGL.glEnd()
            if pnode.selectedInput == pnode2:
                drawArrow(x1, y1, x2, y2, 1.0, 1.0, 0.0)
            else:
                drawArrow(x1, y1, x2, y2, 0.73, 0.53, 0.0)

    # draw control connections between nodes
    Blender.BGL.glEnable (Blender.BGL.GL_LINE_STIPPLE)
    Blender.BGL.glLineStipple (2, 0x5555) # dots
    for pnode in IwProcessingNode.pnList:
        controlIndex = 0
        for pnode2 in pnode.evaluator.connectedControls:
            if not pnode2 == None:
                Blender.BGL.glBegin(Blender.BGL.GL_LINES)
                if controlIndex == pnode.evaluator.selectedControl:
                    Blender.BGL.glColor3f(0.0, 1.0, 1.0)
                else:
                    Blender.BGL.glColor3f(0.0, 0.53, 0.73)
                x1, y1 = pnode2.x+pnode2.u, pnode2.y+pnode2.v/2
                if controlIndex < 4:
                    x2, y2 = pnode.x+controlIndex*IwNodeView.nodeControlIncrement+IwNodeView.nodeControlIncrement/2, pnode.y-IwNodeView.nodeControlAreaHight/2
                else:
                    x2, y2 = pnode.x+(controlIndex-4)*IwNodeView.nodeControlIncrement+IwNodeView.nodeControlIncrement/2, pnode.y-IwNodeView.nodeControlAreaHight-IwNodeView.nodeControlAreaHight/2
                Blender.BGL.glVertex2i(x1, y1)
                Blender.BGL.glVertex2i(x2, y2)
                Blender.BGL.glEnd()
                if controlIndex == pnode.evaluator.selectedControl:
                    drawArrow(x1, y1, x2, y2, 0.0, 1.0, 1.0)
                else:
                    drawArrow(x1, y1, x2, y2, 0.0, 0.53, 0.73)
            controlIndex += 1
    Blender.BGL.glDisable (Blender.BGL.GL_LINE_STIPPLE)

    # draw nodes
    for pnode in IwProcessingNode.pnList:
        drawNode(pnode)

    # draw rubber band
    if pnode1 and (leftMouseX-mouseX) * (leftMouseX-mouseX) + (leftMouseY-mouseY) * (leftMouseY-mouseY) > 16:
        localMouseX, localMouseY = localizeMouse()
        Blender.BGL.glBegin(Blender.BGL.GL_LINES)
        Blender.BGL.glColor3f(1.0, 1.0, 1.0)
        Blender.BGL.glVertex2i(pnode1.x+pnode1.u, pnode1.y+pnode1.v/2)
        Blender.BGL.glVertex2i(localMouseX, localMouseY)
        Blender.BGL.glEnd()

def drawNodeGui():
    global activeButton
    buttonWidth = IwNodeView.nodeGuiAreaWidth-4
    buttonHight = 19
    rowHeight = 21
    xp1, yp1 = IwNodeView.nodeGuiAreaX+2, IwNodeView.nodeGuiAreaY+IwNodeView.nodeGuiAreaHight-10
    xp2, yp2 = IwNodeView.nodeGuiAreaX+IwNodeView.nodeGuiAreaWidth+2, IwNodeView.nodeGuiAreaY+IwNodeView.nodeGuiAreaHight-10
    ix = 0
    Blender.BGL.glColor3f(0.73, 0.73, 0.73)
    Blender.BGL.glRecti(IwNodeView.nodeGuiAreaX, IwNodeView.nodeGuiAreaY, IwNodeView.nodeGuiAreaX+IwNodeView.nodeGuiAreaWidth, IwNodeView.nodeGuiAreaY+IwNodeView.nodeGuiAreaHight)
    for pnode in [node for node in IwProcessingNode.pnList if node.active]:
        Blender.BGL.glColor3f(1.0, 1.0, 1.0)
        Blender.BGL.glRasterPos2d(xp1, yp1)
        Blender.Draw.Text(pnode.evaluator.info["name"] + " node: " + str(pnode.id))
        if len(activeButton):
            paramList = pnode.evaluator.info["param"]
            for param in paramList:
#                print "drawNodeGui", param["name"], pnode.evaluator.isVisible(param["name"]), param["ui"]
                if pnode.evaluator.isVisible(param["name"]):
                    col2 = "column" in param and param["column"] == 2
                    if col2:
                        yp2 -= rowHeight
                        xp, yp = xp2, yp2
                    else:
                        yp1 -= rowHeight
                        xp, yp = xp1, yp1
                    if param["ui"] == IwEvaluator.uiSlider:
                        activeButton[ix] = Blender.Draw.Slider(param["name"] + "  ", 100+ix, \
                                                                xp, yp, \
                                                                buttonWidth, buttonHight, \
                                                                activeButton[ix].val, \
                                                                param["min"], param["max"], 0, \
                                                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiRadio:
                        uiSelect = param["name"] + "%t|"
                        cx = 0
                        for choice in param["enum"]:
                            uiSelect += choice + "%x" + str(cx) + "|"
                            cx += 1
                        activeButton[ix] = Blender.Draw.Menu(uiSelect, 100+ix, \
                                                                xp, yp, \
                                                                buttonWidth, buttonHight, \
                                                                activeButton[ix].val, \
                                                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiString:
                        activeButton[ix] = Blender.Draw.String(param["name"] + "  ", 100+ix, \
                                                                xp, yp, \
                                                                buttonWidth, buttonHight, \
                                                                activeButton[ix].val, \
                                                                399, \
                                                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiImage:
                        activeButton[ix] = IwNodeView.ImageChooserButton(param["name"] + ": ", 100+ix, \
                                xp, yp, \
                                buttonWidth, buttonHight, \
                                activeButton[ix].val, \
                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiColorWeight:
                        activeButton[ix] = IwNodeView.ColorWeightButton(param["name"] + ": ", 100+ix, \
                                xp, yp, \
                                buttonWidth, buttonHight, \
                                getattr(pnode.evaluator, param["name"]), \
                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiColor:
                        activeButton[ix] = IwNodeView.ColorButton(param["name"] + ": ", 100+ix, \
                                xp, yp, \
                                buttonWidth, buttonHight, \
                                getattr(pnode.evaluator, param["name"]), \
                                param["tooltip"])
                    elif param["ui"] == IwEvaluator.uiObjectSelect:
                        uiSelect = param["name"] + "%t|"
                        uiSelect += "<use active object>" + "%x" + str(0) + "|"
                        scene= bpy.data.scenes.active
                        cx = 1
                        for object in [o for o in scene.objects if not o.name.startswith(iwPrefix)]:
                            uiSelect += object.name + "%x" + str(cx) + "|"
                            cx += 1
                        activeButton[ix] = Blender.Draw.Menu(uiSelect, 100+ix, \
                                                                xp, yp, \
                                                                buttonWidth, buttonHight, \
                                                                indexOfObject(getattr(pnode.evaluator, param["name"])), \
                                                                param["tooltip"])
                ix += 1

tooltipExit = "Exit InnerWorld"
tooltipHelp = "Open help in browser: http://innerworld.sourceforge.net/firstSteps.html"
tooltipLoad = "Import processing graph from file"
tooltipSave = "Save processing graph to file"
tooltipSaveAs = "Export processing graph to another file"
tooltipGrid1 = "Set grid to defined number of grid points."
tooltipGrid4 = "Set grid size to 1/4 of defined number of grid points."
tooltipGrid16 = "Set grid size to 1/16 of defined number of grid points."
tooltipGrid64 = "Set grid size to 1/64 of defined number of grid points."
tooltipQuota = "This is a fuse limiting the number of generated objects."
tooltipRefresh = "Recalculate all meshes and object positions."
quotaMsg = "Quota %t|Disable duplicating objects %x0|1 object %x1|100 duplicated objects %x100|250 objects %x250|1000 duplicated objects %x1000|unlimited %x1000000"

def drawButtons():
    global quotaButton
    buttonWidth = IwNodeView.buttonAreaWidth-4
    buttonHight = 19
    buttonCol = IwNodeView.buttonAreaX+2
    buttonRow = IwNodeView.buttonAreaY+2
    Blender.BGL.glColor3f(0.73, 0.73, 0.73)
    Blender.BGL.glRecti(IwNodeView.buttonAreaX, IwNodeView.buttonAreaY, IwNodeView.buttonAreaX+IwNodeView.buttonAreaWidth, IwNodeView.buttonAreaY+IwNodeView.buttonAreaHight)
    Blender.Draw.PushButton("Exit",   5, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipExit)
    buttonRow += buttonHight + 6
    Blender.Draw.PushButton("Help",   4, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipHelp)
    buttonRow += buttonHight + 6
    Blender.Draw.PushButton("Load",   3, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipLoad)
    buttonRow += buttonHight
    tts = tooltipSave
    Blender.Draw.PushButton("Save",   2, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipSave)
    buttonRow += buttonHight
    Blender.Draw.PushButton("Save As",1, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipSaveAs)
    buttonRow += buttonHight + 6
    colOffset = 0
    Blender.Draw.Toggle(":64",  13, buttonCol+colOffset, buttonRow, buttonWidth/3, buttonHight, quickScale == 8, tooltipGrid64)
    colOffset += buttonWidth/3
    Blender.Draw.Toggle(":16",  12, buttonCol+colOffset, buttonRow, buttonWidth/3, buttonHight, quickScale == 4, tooltipGrid16)
    colOffset += buttonWidth/3
    Blender.Draw.Toggle(":4",   11, buttonCol+colOffset, buttonRow, buttonWidth/3, buttonHight, quickScale == 2, tooltipGrid4)
    buttonRow += buttonHight
    Blender.Draw.Toggle("1:1",  10, buttonCol,           buttonRow, buttonWidth,   buttonHight, quickScale == 1, tooltipGrid1)
    buttonCol = IwNodeView.buttonAreaX+2
    buttonRow += buttonHight+ 6
    quotaButton = Blender.Draw.Menu(quotaMsg, 14, buttonCol, buttonRow, buttonWidth, buttonHight, IwPlacement.quota, tooltipQuota)
    buttonRow += buttonHight + 6
    Blender.Draw.PushButton("Refresh",   9, buttonCol, buttonRow, buttonWidth, buttonHight, tooltipRefresh)


def drawGui():
    global lastFilename
    try:
        Blender.BGL.glEnable(Blender.BGL.GL_LINE_SMOOTH)
        drawGraphGui()
        drawNodeGui()
        drawButtons()
        Blender.BGL.glColor3f(0.73, 0.73, 0.73)
        Blender.BGL.glRecti(IwNodeView.statusAreaX, IwNodeView.statusAreaY, IwNodeView.statusAreaX+IwNodeView.statusAreaWidth, IwNodeView.statusAreaY+IwNodeView.statusAreaHight)
        Blender.BGL.glColor3f(1.0, 1.0, 1.0)
        Blender.BGL.glRasterPos2d(IwNodeView.statusAreaX+2, IwNodeView.statusAreaY+5)
        if lastFilename:
            Blender.Draw.Text(lastFilename)
        else:
            Blender.Draw.Text("InnerWorld " + __version__ + " http://innerworld.sourceforge.net")
    except:
        Blender.Draw.PupMenu( "Unexpected Error: %s, %s, %s" % tuple(sys.exc_info()[0:3]) )
        traceback.print_exc()


# ----- action handling -----
def actionNewNode():
    try:
        resultType = Blender.Draw.PupMenu(IwEvaluator.getTypeSelector())
        if resultType > 0:
            resultNode = Blender.Draw.PupMenu(IwEvaluator.getNodeSelector(resultType-1))
            if resultNode > 0:
                processingNode = IwProcessingNode.ProcessingNode()
                localMouseX, localMouseY = localizeMouse()
                py = localMouseY
                if py < IwNodeView.buttonAreaY+IwNodeView.buttonAreaHight:
                    py = IwNodeView.buttonAreaY+IwNodeView.buttonAreaHight+5
                processingNode.setPosition(localMouseX, py)
                processingNode.evaluator = IwEvaluator.createEvaluator(resultType-1, resultNode-1)
                IwProcessingNode.pnList.append(processingNode)
                # select and activate new node
                list(map(lambda n: n.clearMarkers(), IwProcessingNode.pnList))
                processingNode.active = processingNode.selected = True
                activateNode(processingNode)
                updateAll()
    except:
        Blender.Draw.PupMenu( "Unexpected Error: %s, %s, %s" % tuple(sys.exc_info()[0:3]) )
        traceback.print_exc()

    Blender.Draw.Redraw()

def actionNewConnection():
    global pnode1
    if pnode1 and (leftMouseX-mouseX) * (leftMouseX-mouseX) + (leftMouseY-mouseY) * (leftMouseY-mouseY) > 16:
        localX, localY = localizeMouse()
        msg = IwPick.connectNode(IwProcessingNode.pnList, pnode1, localX, localY)
        pnode1 = None
        if msg:
            Blender.Draw.PupMenu("Error!%t|" + msg)
        else:
            updateAll()
        Blender.Draw.Redraw()
                    
def actionDel():
    selectedNodeList = [node for node in IwProcessingNode.pnList if node.selected]
    if len(selectedNodeList) > 0:
        result = Blender.Draw.PupMenu("OK?%t|Delete Nodes")
        if result == 1:
            IwProcessingNode.removeselectedNodes()
    for pnode in IwProcessingNode.pnList:
        if pnode.selectedInput != None:
            result = Blender.Draw.PupMenu("OK?%t|Delete Input")
            if result == 1:
                pnode.removeInput(pnode.selectedInput)
    for pnode in IwProcessingNode.pnList:
        if pnode.evaluator.selectedControl >= 0:
            result = Blender.Draw.PupMenu("OK?%t|Delete Control")
            if result == 1:
                pnode.removeControl(pnode.evaluator.selectedControl)
    updateAll()
    Blender.Draw.Redraw()

def actionSave(filename):
    global lastFilename
    if filename:
        if not filename.endswith('.iw'):
            filename += '.iw'
        lastFilename = filename
        if not IwProcessingNode.save(filename):
            Blender.Draw.PupMenu("error storing file '" + filename + "'.")
        updateDict()

def actionLoad(filename):
    global lastFilename
    if filename and filename.endswith('.iw'):
        if IwProcessingNode.load(filename):
            lastFilename = filename
        else:
            Blender.Draw.PupMenu("error loading file '" + filename + "'.")
        for pnode in [node for node in IwProcessingNode.pnList if node.active]:
            activateNode(pnode)
        IwProcessingNode.invalidateSinkList()
        IwProcessingNode.invalidateSinkList(subtype=IwEvaluator.subtypeObjDupli)
    else:
        Blender.Draw.PupMenu("error loading file: extension '.iw' expected.")
    updateAll()

# ----- event handling -----
def handleEvent(evt, val):
    global mouseX, mouseY, moveX, moveY, leftMouseX, leftMouseY, isDraged, pnode1, isShiftPressed
    try:
        if evt == Blender.Draw.MOUSEX:
            mouseX = val
            if isDraged:
                moveX = IwPick.moverX(IwProcessingNode.pnList, mouseX, moveX)
                Blender.Draw.Redraw()
            if pnode1:
                Blender.Draw.Redraw()
    
        elif evt == Blender.Draw.MOUSEY:
            mouseY = val
            if isDraged:
                moveY = IwPick.moverY(IwProcessingNode.pnList, mouseY, moveY)
                Blender.Draw.Redraw()
            if pnode1:
                Blender.Draw.Redraw()
    
        elif evt == Blender.Draw.RIGHTMOUSE and not val:
            #print "RIGHTMOUSE up        x", mouseX, " y", mouseY, " ", val
            localX, localY = localizeMouse()
            pnode = IwPick.select(IwProcessingNode.pnList, localX, localY, isShiftPressed)
            if pnode:
                activateNode(pnode)
            isDraged = 0
            Blender.Draw.Redraw()
    
        elif evt == Blender.Draw.LEFTMOUSE and val:
            #print "LEFTMOUSE down x", mouseX, " y", mouseY, " ", val
            if not isDraged:
                localX, localY = localizeMouse()
                leftMouseX, leftMouseY = mouseX, mouseY
                pnode1 = IwPick.pickNode(IwProcessingNode.pnList, localX, localY)
            isDraged = 0
            Blender.Draw.Redraw()
    
        elif evt == Blender.Draw.LEFTMOUSE and not val:
            #print "LEFTMOUSE up      x", mouseX, " y", mouseY, " ", val
            actionNewConnection()
                        
        elif evt == Blender.Draw.SPACEKEY and val:
            actionNewNode()
                
        elif evt == Blender.Draw.XKEY and val:
            actionDel()
                
        elif evt == Blender.Draw.GKEY and not val:
            moveX = mouseX
            moveY = mouseY
            isDraged = 1
    
        elif evt == Blender.Draw.AKEY and not val:
            isShiftPressed = 0
            pnode = IwPick.selectAll(IwProcessingNode.pnList)
            if pnode:
                activateNode(pnode)
            Blender.Draw.Redraw()
    
        elif evt == Blender.Draw.ESCKEY and not val:
            isDraged = 0
            pnode1 = None
    
        elif evt == Blender.Draw.LEFTSHIFTKEY or evt == Blender.Draw.RIGHTSHIFTKEY:
            isShiftPressed = val
#            print "isShiftPressed", isShiftPressed
    except:
        Blender.Draw.PupMenu( "Unexpected Error: %s, %s, %s" % tuple(sys.exc_info()[0:3]) )
        traceback.print_exc()

def handleButtonEvent(bevt):
    global lastFilename, quickScale, quotaButton
    try:
        needsUpdate = False
        if bevt == 2 and lastFilename == None:
            bevt = 1
        if bevt == 1:
            Blender.Window.FileSelector(actionSave, "Save File As: ", "*.iw")
        elif bevt == 2:
            actionSave(lastFilename)
        elif bevt == 3:
            Blender.Window.FileSelector(actionLoad, "Load File: ", "*.iw")
#            Blender.Window.Redraw(-1)
        elif bevt == 4:
            webbrowser.open("http://innerworld.sourceforge.net/firstSteps.html")
        elif bevt == 5:
            updateDict()
            Blender.Draw.Exit()
        elif bevt == 6:
            Blender.Window.FileSelector(actionLoadImageCallback, "Load Image", IwNodeView.ImageChooserButton.active.val)
        elif bevt == 9:
            IwProcessingNode.invalidateSinkList(subtype=IwEvaluator.subtypeObjDupli)
            needsUpdate = True
        elif bevt == 10:
            quickScale = 1
            IwProcessingNode.invalidateSinkList()
            needsUpdate = True
        elif bevt == 11:
            quickScale = 2
            IwProcessingNode.invalidateSinkList()
            needsUpdate = True
        elif bevt == 12:
            quickScale = 4
            IwProcessingNode.invalidateSinkList()
            needsUpdate = True
        elif bevt == 13:
            quickScale = 8
            IwProcessingNode.invalidateSinkList()
            needsUpdate = True
        elif bevt == 14:
            if not IwPlacement.quota == quotaButton.val:
                IwPlacement.quota = quotaButton.val
                IwProcessingNode.invalidateSinkList(subtype=IwEvaluator.subtypeObjDupli)
                needsUpdate = True
        elif bevt >= 100 and bevt < 150:
            ix = bevt-100
            newValue = activeButton[ix].val
#            print "bevt", bevt, newValue
            for pnode in [node for node in IwProcessingNode.pnList if node.active]:
                px = 0
                for param in pnode.evaluator.info["param"]:
                    if px == ix:
                        paramName = pnode.evaluator.info["param"][ix]["name"]
                        oldValue = getattr(pnode.evaluator, paramName)
                        if paramName == "masterObjectName":
                            #print "paramName=", paramName, newValue
                            #needsUpdate = True
                            if newValue == 0:
                                originalActiveObject = bpy.data.scenes.active.objects.active
                                if originalActiveObject:
                                    cx = 0
                                    for object in [o for o in bpy.data.scenes.active.objects if not o.name.startswith(iwPrefix)]:
                                        cx += 1
                                        if object.name == originalActiveObject.name:
                                            setattr(pnode.evaluator, paramName, originalActiveObject.name)
                                            pnode.invalidate()
                                            needsUpdate = True
                                            activeButton[ix].val = cx
                                            break
                            else:
                                cx = 0
                                for object in [o for o in bpy.data.scenes.active.objects if not o.name.startswith(iwPrefix)]:
                                    cx += 1
                                    if newValue == cx:
                                        setattr(pnode.evaluator, paramName, object.name)
                                        pnode.invalidate()
                                        needsUpdate = True
                                        break
                        elif newValue != oldValue:
                            setattr(pnode.evaluator, paramName, newValue)
                            pnode.invalidate()
                            needsUpdate = True
                            #needsMeshUpdate = needsMeshUpdate or pnode.evaluator.needsMeshRecalculation(paramName)
                    px += 1
        if needsUpdate:
            updateAll()
#            Blender.Window.Redraw(-1)
    except:
        Blender.Draw.PupMenu( "Unexpected Error: %s, %s, %s" % tuple(sys.exc_info()[0:3]) )
        traceback.print_exc()

def indexOfObject(masterObjectName):
    #print "indexOfObject masterObjectName=", masterObjectName
    cx = 0
    if not masterObjectName == "":
        for object in [o for o in bpy.data.scenes.active.objects if not o.name.startswith(iwPrefix)]:
            cx += 1
            if object.name == masterObjectName:
                break
    return cx

def actionLoadImageCallback(filename):
    IwNodeView.ImageChooserButton.actionLoadImage(filename)
    for pnode in [node for node in IwProcessingNode.pnList if node.active]:
        px = 0
        ix = 0
        for param in pnode.evaluator.info["param"]:
            if px == ix:
                setattr(pnode.evaluator, pnode.evaluator.info["param"][ix]["name"], activeButton[ix].val)
                pnode.invalidate()
            px += 1
    updateAll()
#    Blender.Window.Redraw(-1)

def updateAll():
    Blender.Window.WaitCursor(1)
    t0 = time.time()
    c0 = time.clock()
    print("------- updateAll")
    newMesh()
    duplicateMasterObjects()
    updatePreview()
    IwProcessingNode.cleanupList = []
    updateDict()
    IwProcessingNode.setAllInvalid(False)
    print("----------------- ", time.clock()-c0, time.time()-t0)
    Blender.Window.Redraw(-1)
    Blender.Window.WaitCursor(0)


def updateDict():
    iwDict = {'version' : __version__, 'pnList' : IwProcessingNode.serialize()}
    Blender.Registry.SetKey('InnerWorld', iwDict)

def reloadNodeList():
    iwDict = Blender.Registry.GetKey('InnerWorld')
    if iwDict: # if found, get the values saved in Blender registry
        IwProcessingNode.deserialize(iwDict['pnList'])
    for pnode in [node for node in IwProcessingNode.pnList if node.active]:
        activateNode(pnode)
    updateAll()


# ----- start up -----
try:
    reloadNodeList()
except:
    traceback.print_exc()
Blender.Draw.Register(drawGui, handleEvent, handleButtonEvent)