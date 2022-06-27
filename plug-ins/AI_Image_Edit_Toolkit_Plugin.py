import maya.api.OpenMaya as mui
import maya.cmds as cmds

from onRenderViewOpen_ScriptJob import listen_to_window_events

def maya_useNewAPI():
    pass
    
def initializePlugin(plugin):
    
    vendor = "Simon Weck"
    version = "1.0.0"
    
    mui.MFnPlugin(plugin, vendor, version)
    
    listen_to_window_events()
    
    print("AI_TOOLKIT : AI Image Edit Toolkit Plugin Loaded")
    
def uninitializePlugin(plugin):
    pass