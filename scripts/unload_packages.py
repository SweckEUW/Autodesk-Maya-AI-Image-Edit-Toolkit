import sys

# if you have some packages that you often reload, you can put them here
# and they will get reloaded if "packages" attribute is not explicitly stated
DEFAULT_RELOAD_PACKAGES = ["AI_Image_Edit_Toolkit_Plugin_Test.py","collapsible_widget.py","extendRenderWindow.py","onRenderViewOpen_EventFiltering.py","onRenderViewOpen_ScriptJob.py","options.json","optionWindow_utils.py","optionWindow.py","neural_style.py"] 

def unload_packages(silent=False, packages=None):
            
    if packages is None:
        packages = DEFAULT_RELOAD_PACKAGES

    # construct reload list
    reloadList = []
    for i in sys.modules.keys():
        for package in packages:
            if i.startswith(package):
                reloadList.append(i)
    
    # unload everything
    for i in reloadList:
        try:
            if sys.modules[i] is not None:
                del(sys.modules[i])
                if not silent:
                    print("Unloaded: %s" % i)
        except:
            print("Failed to unload: %s" % i)

if __name__ == "__main__":
    unload_packages()