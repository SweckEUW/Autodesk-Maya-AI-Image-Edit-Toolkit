import maya.cmds as cmds

from unload_packages import unload_packages

if __name__ == "__main__":
   unload_packages() 
   
   plugin_name = "AI_Image_Edit_Toolkit_Plugin.py"
   cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
   cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))