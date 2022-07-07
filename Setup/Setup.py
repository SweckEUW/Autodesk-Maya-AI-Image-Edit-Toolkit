import subprocess
import sys

def install(package):
    subprocess.check_call(["mayapy", "-m", "pip", "install", package])

subprocess.check_call(["mayapy", "-m", "get-pip"])
subprocess.check_call(["mayapy", "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/cu116"])
install("numpy")
install("pillow")
install("tensorflow")
install("tensorflow_addons")
install("typeguard")