import maya.cmds as cmds
import pymel.core as pm

class WindowWatcher():

    def __init__(self):
        self.window_name = "renderViewWindow"
        self.window_opened = False       

    def check_for_window_open(self):        
        if not self.window_opened:
            if self.window_name in cmds.lsUI(windows=True):
                self.window_opened = True
                print("Render Window opened!")
        else:
            if not self.window_name in cmds.lsUI(windows=True):
                self.window_opened = False
                print("Render Window Closed!")


if __name__ == "__main__":
    render_window_watcher = WindowWatcher()
    cmds.scriptJob(event=["idle", pm.windows.Callback(render_window_watcher.check_for_window_open)])