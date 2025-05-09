# Prototype: Convert Photo or Text to a Simple 3D Model

A lightweight Python prototype that transforms a single-object photo or a short text prompt into a basic 3D mesh (.obj/.stl), complete with a quick visualization.

---

## 🚀 Features

- **Dual-Mode Input**: Accepts either a **photo** (`.jpg`/`.png`) of an object or a **text prompt** (e.g., “A small toy car”).
- **Open-Source Pipelines**: Leverages [HunyuanDiT](https://github.com/Tencent/HunyuanDiT) for text-to-image and [Hunyuan3D-2mini](https://huggingface.co/tencent/Hunyuan3D-2mini) for image-to-mesh.
- **Fast Prototyping**: Two simple function calls—`t2i(prompt)` and `i2m(image)`—to generate your 3D model.
- **Export Formats**: Outputs a `.obj` (or `.stl`) file compatible with tools like MeshLab, Blender, or 3D slicers.
- **Extendable**: Easy to integrate background removal (`rembg`), alternative shape generators (e.g., Shap-E), or custom post-processing.

---

## 📋 Prerequisites

- **Python** 3.8 or higher
- **CUDA-enabled GPU** (12 GB VRAM recommended)
- **virtualenv** for environment isolation
- **Hugging Face account** (for model downloads)

---

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Tencent/Hunyuan3D-2.git
   cd Hunyuan3D-2
   ```

2. **Set up a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install torch torchvision diffusers transformers trimesh
   ```

4. **Install HunyuanDiT & Hunyuan3D-mini**

   ```bash
   pip install huggingface_hub
   pip install git+https://github.com/Tencent/HunyuanDiT.git
   # Or, if you prefer the Diffusers format:
   pip install diffusers
   ```

---

## 🎬 Usage

### 1. Photo Input Workflow

```bash
python main.py --input_image path/to/photo.jpg --mode photo
```

- **Preprocessing** (optional): Background removal using `hy3dgen.rembg` for cleaner silhouettes.
- **3D Generation**: Feeds the RGB image into the `Hunyuan3DDiTFlowMatchingPipeline`.
- **Output**: `output.obj` mesh saved to the project root.

### 2. Text Prompt Workflow

```bash
python main.py --prompt "A small toy car" --mode text
```

1. **Text → Image**: `HunyuanDiTPipeline` generates a 512×512 PIL image of your prompt.
2. **Image → Mesh**: Flow-matching model creates the 3D mesh.
3. **Output**: `output.obj` ready for viewing or 3D printing.

---

## 📝 Example Code Snippet

```python
from hy3dgen.text2image import HunyuanDiTPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
import trimesh

# Text → 2D
t2i = HunyuanDiTPipeline(
    'Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers-Distilled',
    device='cuda'
)
img = t2i("A shiny red apple on white")

# 2D → 3D
i2m = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2mini',
    subfolder='hunyuan3d-dit-v2-mini-turbo',
    device='cuda'
)
mesh = i2m(img, num_inference_steps=5)[0]

# Export mesh
mesh.export("apple.obj")
```

---

## 📦 Dependencies

- **HunyuanDiT**: Multi-resolution diffusion transformer for text-to-image [GitHub]
- **Hunyuan3D-2mini**: 0.6B parameter shape generator using flow matching [Hugging Face]
- **diffusers & transformers**: Model loading and inference [Hugging Face]
- **trimesh**: Mesh handling and export
- **rembg** (optional): Background removal for photos

---

## 💭 Thought Process & Future Work

- **Model Selection**: Chose HunyuanDiT for high-quality 2D generation and Hunyuan3D-mini for fast, Python-native mesh synthesis.
- **Simplicity**: Designed two-step pipelines (`t2i` & `i2m`) for minimal boilerplate.
- **Extendability**:
  - Integrate `rembg` to refine object silhouettes.
  - Explore combining with [Shap-E](https://github.com/openai/shap-e) for direct text-to-3D.
  - Add surface smoothing, UV mapping, and texture baking.

---
![apple_color](https://github.com/user-attachments/assets/a40b9810-f6c2-43c6-9596-95dac350533c)

![apple](https://github.com/user-attachments/assets/9b61a729-baac-4bab-8116-8a0a95b066a5)


