import maya.api.OpenMaya as mui
import maya.cmds as cmds

from onRenderViewOpen import listen_to_window_events, remove_listen_to_window_events

def maya_useNewAPI():
    pass
    
def initializePlugin(plugin):
    print("AI_TOOLKIT : Loading Plugin")
        
    vendor = "Simon Weck"
    version = "1.0.0"
    
    mui.MFnPlugin(plugin, vendor, version)
    
    listen_to_window_events()
    
    
def uninitializePlugin(plugin):
    remove_listen_to_window_events()