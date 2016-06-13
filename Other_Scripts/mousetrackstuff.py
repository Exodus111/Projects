from bge import logic
from random import randint

def main():
    scene = logic.getCurrentScene()
    cont = logic.getCurrentController()
    own = cont.owner
    
    mouse_over = cont.sensors["mouse_over"]
    mouse_click = cont.sensors["mouse_click"]
    add_object = cont.actuators["add_object"]
    
    greencube = scene.objectsInactive["GreenCube"]
    redcube = scene.objectsInactive["RedCube"]
    bluecube = scene.objectsInactive["BlueCube"]
    
    if mouse_over.positive:
        tracker = scene.objects["tracker"]
        tracker.worldPosition = mouse_over.hitPosition
        tracker.worldPosition.z += 1
        
        if mouse_click.positive:
            num = randint(1, 3)
            if num == 1:
                add_object.object = greencube
                add_object.instantAddObject()
            elif num  == 2:
                add_object.object = redcube
                add_object.instantAddObject()
            elif num  == 3:
                add_object.object = bluecube
                add_object.instantAddObject()
            
            
            
        
