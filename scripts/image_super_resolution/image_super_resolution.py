from image_super_resolution.model.srgan import generator
from image_super_resolution.model import resolve_single
from image_super_resolution.model.edsr import edsr
#from image_super_resolution.model.wdsr import wdsr_b
from PIL import Image
import numpy as np

from optionWindow_utils import getOptions


# Source: https://github.com/krasserm/super-resolution


def load_image(path):
    return np.array(Image.open(path))
    
def main():
    options = getOptions()["image_super_resolution"]

    # EDSR
    if options["model"] == "EDSR":
        model = edsr(scale=4, num_res_blocks=16)
        model.load_weights('C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/scripts/image_super_resolution/weights/edsr-16-x4/weights.h5')

    # WDSR
    # if options["model"] == "WDSR":
    #     model = wdsr_b(scale=4, num_res_blocks=32)
    #     model.load_weights('C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/scripts/image_super_resolution/weights/wdsr-b-32-x4/weights.h5')

    # SRGAN
    if options["model"] == "SRGAN":
        model = generator()
        model.load_weights('C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/scripts/image_super_resolution/weights/srgan/gan_generator.h5')

    lr = load_image('C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/scripts/image_super_resolution/demo/0869x4-crop.png')
    sr = resolve_single(model, lr)

    img = Image.fromarray(np.array(sr), 'RGB')
    img.save('C:/Users/Simon/Desktop/test.jpg')

if __name__ == "__main__":
    main()