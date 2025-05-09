from hy3dgen.text2image import HunyuanDiTPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

# 1) Text → 2D color image
t2i = HunyuanDiTPipeline(
    "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled",
    device="cuda"
)
color_img = t2i("A shiny red apple on a white background")
color_img.save("apple_color.png")

# 2) Initialize the mini shape model
i2m = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    "tencent/Hunyuan3D-2mini",
    subfolder="hunyuan3d-dit-v2-mini-turbo",
    device="cuda"
)

# 3) Generate mesh from the RGB mask (few steps for speed)
meshes = i2m(color_img, num_inference_steps=5)
mesh    = meshes[0]

# 4) Export to OBJ for 3D printing
mesh.export("apple_silhouette.obj")
print("Saved apple_silhouette.obj")
