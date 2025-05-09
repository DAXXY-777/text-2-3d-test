Assignment
Title: Prototype: Convert Photo or Text to a Simple 3D Model
Description: Implement a Python prototype that:

Input: accepts either a photo (.jpg/.png) of a single object or a short text prompt (e.g., “A small toy car”)

Processing: uses open-source AI/ML libraries to generate a basic 3D mesh

Output: produces a downloadable .obj (or .stl) and a simple visualization 
GitHub
GitHub

Prerequisites
Python 3.8+

CUDA-enabled GPU (12 GB VRAM recommended) to accelerate inference 
Hugging Face

virtualenv for isolated environments 
Virtualenv

Setup
Clone & enter project

bash
Copy
Edit
git clone https://github.com/Tencent/Hunyuan3D-2.git
cd Hunyuan3D-2
Create & activate virtualenv

bash
Copy
Edit
python3 -m venv venv        # venv module :contentReference[oaicite:4]{index=4}
source venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
pip install torch torchvision diffusers transformers trimesh
Install HunyuanDiT & Hunyuan3D-mini

bash
Copy
Edit
pip install huggingface_hub      # for model downloads :contentReference[oaicite:5]{index=5}
pip install git+https://github.com/Tencent/HunyuanDiT.git  
# Alternatively, diffusers format:
pip install diffusers
Usage
1. Photo Input Workflow
bash
Copy
Edit
python main.py --input_image path/to/photo.jpg --mode photo
Preprocessing: (optional) background removal with hy3dgen.rembg

3D Generation: directly send the RGB image into Hunyuan3D-mini 
Hugging Face

Output: output.obj mesh saved in project root

2. Text Prompt Workflow
bash
Copy
Edit
python main.py --prompt "A small toy car" --mode text
Text→Image: HunyuanDiT produces a 512×512 PIL image of the prompt 
GitHub

Image→Mesh: flow-matching on the generated image

Output: output.obj ready for 3D viewing

Example Code Snippet
python
Copy
Edit
from hy3dgen.text2image import HunyuanDiTPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

# Text→2D
t2i = HunyuanDiTPipeline('Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers-Distilled', device='cuda')
img = t2i("A shiny red apple on white")

# 2D→3D
i2m = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2mini', subfolder='hunyuan3d-dit-v2-mini-turbo', device='cuda'
)
mesh = i2m(img, num_inference_steps=5)[0]

# Export
import trimesh
mesh.export("apple.obj")  # MeshLib :contentReference[oaicite:8]{index=8}
Dependencies
HunyuanDiT: multi-resolution diffusion transformer for text-to-image 
GitHub

Diffusers & Transformers: Hugging Face libraries for model loading 
Hugging Face

Hunyuan3D-2mini: 0.6 B parameter shape generator, flow-matching on images 
Hugging Face

trimesh: Python library for mesh handling and export 
trimesh.org

virtualenv / venv: environment isolation 
Python documentation

Thought Process
Choice of Models: HunyuanDiT offers high-quality prompt→image (English+Chinese) with readily available weights; Hunyuan3D-mini provides fast image→mesh conversion without complex C++ extensions 
GitHub
.

Simplicity: Pipeline requires only two function calls—t2i(prompt) and i2m(image)—enabling rapid prototyping.

Flexibility: Supports photo or text input by treating both as images for the 3D flow model.

Extendability: Future work could add rembg for cleaner silhouettes or integrate Shap-E for pure text-to-3D 
GitHub
.

Run the prototype and load apple.obj in any 3D viewer (e.g., MeshLab, Blender) or slicer for 3D printing.
