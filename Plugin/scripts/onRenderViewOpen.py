import maya.cmds as cmds
import pymel.core as pm

from extendRenderWindow import extendRenderWindow 

class WindowWatcher():

    def __init__(self):
        self.window_name = "renderViewWindow"
        self.window_opened = False       

    def check_for_window_open(self):        
        if not self.window_opened:
            if self.window_name in cmds.lsUI(windows=True):
                self.window_opened = True
                print("AI_TOOLKIT : Render Window Opened!")
                extendRenderWindow()
        else:
            if not self.window_name in cmds.lsUI(windows=True):
                self.window_opened = False
                #print("Render Window Closed!")


script_job_number = None
def listen_to_window_events():
    print("AI_TOOLKIT : Installing Window Watcher")
    render_window_watcher = WindowWatcher()
    global script_job_number
    script_job_number = cmds.scriptJob(event=["idle", pm.windows.Callback(render_window_watcher.check_for_window_open)])

def remove_listen_to_window_events():
    cmds.scriptJob(kill=script_job_number)

if __name__ == "__main__":
    listen_to_window_events()
