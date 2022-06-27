import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from PIL import Image 
import os
import maya.app.general.createImageFormats as createImageFormats

media_path = "C:/Users/Simon/Desktop/Projektarbeit/Autodesk-Maya-AI-Toolkit/media/"
style_img_path = [media_path+"style7.jpg"]

def transfer_image(args):    
    
    def load_image(img_path):
        img = tf.io.read_file(img_path)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = img[tf.newaxis, :]
        return img
    
    #Save current rendering to disk
    editor = 'renderView'
    cmds.renderWindowEditor(editor, e=True, writeImage=media_path+"rendering.jpg")
    
    #load neural net
    model = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")
    
    if os.path.exists(media_path+"output.jpg"):
        content_img = load_image(media_path+"output.jpg")
    else:
        content_img = load_image(media_path+"rendering.jpg")
        
    style_img = load_image(style_img_path[0])
    
    transfered_img = model(tf.constant(content_img), tf.constant(style_img))[0]
    
    im1 = Image.fromarray(np.uint8(np.squeeze(transfered_img)*255)).convert('RGB')
    im1 = im1.save(media_path+"output.jpg")

    cmds.image("test123",image=media_path+"output.jpg", edit=True)

def upscale_image(args):
    
    def load_image(image_path):
        hr_image = tf.image.decode_image(tf.io.read_file(image_path))
        if hr_image.shape[-1] == 4:
          hr_image = hr_image[...,:-1]
        hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
        hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
        hr_image = tf.cast(hr_image, tf.float32)
        return tf.expand_dims(hr_image, 0)
    
    #Save current rendering to disk
    editor = 'renderView'
    cmds.renderWindowEditor(editor, e=True, writeImage=media_path+"rendering.jpg")
    
    #load neural net
    model = hub.load("https://tfhub.dev/captain-pool/esrgan-tf2/1")
    
    if os.path.exists(media_path+"output.jpg"):
        low_resolution_image = load_image(media_path+"output.jpg")
    else:
        low_resolution_image = load_image(media_path+"rendering.jpg")

    super_resolution_image = model(low_resolution_image)

    image = tf.squeeze(tf.cast(tf.clip_by_value(super_resolution_image, 0, 255), tf.uint8))
    image = Image.fromarray(image.numpy())
    image.save(media_path+"output.jpg")    

    cmds.image("test123",image=media_path+"output.jpg", edit=True)
    
def createUI():
    
    #delete old output
    if os.path.exists(media_path+"output.jpg"):
        os.remove(media_path+"output.jpg")
    
    #delte old rendering
    if os.path.exists(media_path+"rendering.jpg"):
        os.remove(media_path+"rendering.jpg")
        
    windowID = "myWindowID"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID, title="AI Tools", sizeable=True, resizeToFitChildren=True)
    
    #cmds.columnLayout(numberOfColumns=2)
    cmds.columnLayout( columnAttach=('both', 5), rowSpacing=5, adjustableColumn=True, columnAlign='center')

    #Save current rendering to disk
    editor = 'renderView'
    formatManager = createImageFormats.ImageFormats()
    formatManager.pushRenderGlobalsForDesc("JPEG")
    cmds.renderWindowEditor(editor, e=True, writeImage=media_path+"rendering.jpg")
    
    cmds.image("test123",image=media_path+"rendering.jpg")
    
    def searchForFiles(args):  
        global style_img_path  
        style_img_path = cmds.fileDialog2(fileFilter="All Files (*.*)",dialogStyle=2,fileMode=1,cap='Open Image')
        
    cmds.button(label="select style image", command=searchForFiles)
    cmds.button(label="style transfer", command=transfer_image)
    
    cmds.separator(h=10)
    
    cmds.button(label="upscale", command=upscale_image)
    
    cmds.showWindow()
    

createUI()