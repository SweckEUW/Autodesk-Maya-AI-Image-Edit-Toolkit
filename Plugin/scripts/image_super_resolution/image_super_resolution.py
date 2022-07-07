from image_super_resolution.model.srgan import generator
from image_super_resolution.model import resolve_single
from image_super_resolution.model.edsr import edsr
from image_super_resolution.model.wdsr import wdsr_b
from PIL import Image
import numpy as np
import maya.cmds as mc
import os
import maya.app.general.createImageFormats as createImageFormats

from optionWindow_utils import getOptions


# Source: https://github.com/krasserm/super-resolution

def get_absolute_path(path):
    return os.path.join(os.path.split(mc.file(q=True, loc=True))[0], path)

def load_image(path):
    return np.array(Image.open(path))
    
def main(path):
    options = getOptions()["image_super_resolution"]
    
    # EDSR
    if options["model"] == "EDSR":
        model = edsr(scale=4, num_res_blocks=16)
        model.load_weights(get_absolute_path('Plugin/scripts/image_super_resolution/weights/edsr-16-x4/weights.h5'))

    # WDSR
    if options["model"] == "WDSR":
        model = wdsr_b(scale=4, num_res_blocks=32)
        model.load_weights(get_absolute_path('Plugin/scripts/image_super_resolution/weights/wdsr-b-32-x4/weights.h5'))

    # SRGAN
    if options["model"] == "SRGAN":
        model = generator()
        model.load_weights(get_absolute_path("Plugin/scripts/image_super_resolution/weights/srgan/gan_generator.h5"))

    lr = load_image(path)
    sr = resolve_single(model, lr)

    img = Image.fromarray(np.array(sr), 'RGB')
    return img

if __name__ == "__main__":
    formatManager = createImageFormats.ImageFormats()
    formatManager.pushRenderGlobalsForDesc("JPEG")

    path = os.path.join(os.path.split(mc.file(q=True, loc=True))[0], "Plugin/media/tmp/rendering.jpg")
    mc.renderWindowEditor("renderView", e=True, writeImage=path)
    main(path)