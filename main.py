from PIL import Image, ImageEnhance, ImageFilter
import os
import gradio as gr
import numpy as np
direc = "./editedImgs"


if not os.path.exists(direc):
    os.makedirs(direc) 

def warm_image(image, factor):
    if image is None:
        return None 

    image = image.convert("RGB")

    enhancer = ImageEnhance.Color(image)
    colored_image = enhancer.enhance(1 + factor/2)
    enhancer = ImageEnhance.Sharpness(colored_image)
    sharp_image = enhancer.enhance(1 - factor/4)
    enhancer = ImageEnhance.Contrast(sharp_image)
    contrast_image = enhancer.enhance(1 + factor/10)
    enhancer = ImageEnhance.Brightness(contrast_image)
    final_image = enhancer.enhance(1 + factor/10)

    return final_image


def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    print(input_img.shape, sepia_img.shape)
    return sepia_img

def function(image):
    pathOut = "./editedImgs"
    edit = image.filter(ImageFilter.SHARPEN).convert("L")
    edit.save(f"{pathOut}/test.png")
    return f"{pathOut}/test.png"

with gr.Blocks() as demo:
    gr.Markdown("## PIL filter | make an image grey")
    demo1 = gr.Interface(function, gr.Image(height=200, width=200, type='pil'), "image", title="Filters | By: Daniel")

    gr.Markdown("## Sepia Filter | make an image warmish-grey")
    demo2 = gr.Interface(sepia, gr.Image(height=200, width=200), "image")
    gr.Markdown("## PIL Filter | make an image brighter")
    demo3 = gr.Interface(
    fn=warm_image,
    inputs=[
        gr.Image(type="pil"), 
        gr.Slider(minimum=-8, maximum=8, step=0.1, label="Warmth Factor")
    ],
    outputs=gr.Image(type="pil"), 
    description="Adjust the brightness of an image. Use the slider to control the brightness factor.",
)

demo.launch(server_name="0.0.0.0", share=False)