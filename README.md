# 🌴 Mango Tree Detection & Counter

A Streamlit web app that uses **YOLOv8** to detect and count mango trees
in aerial or field photographs.

---

## 📁 Project Structure

```
mango-tree-counter/
├── app.py               ← Main Streamlit app (beautiful dark-green UI)
├── train.py             ← Script to train YOLO on your dataset
├── requirements.txt     ← Python dependencies
├── best.pt              ← Your trained model weights (YOU add this)
└── dataset/             ← Your Roboflow dataset (YOU add this)
    ├── data.yaml
    ├── train/
    │   ├── images/
    │   └── labels/
    ├── valid/
    │   ├── images/
    │   └── labels/
    └── test/
        ├── images/
        └── labels/
```

---

## 🚀 Step-by-Step Guide

### STEP 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ On Streamlit Cloud use the `requirements.txt` directly (no pip command needed).

---

### STEP 2 — Download your Roboflow dataset

1. Go to your Roboflow project:  
   https://universe.roboflow.com/sibbalas-workspace/mango-tree-count/dataset/2

2. Click **Download Dataset**

3. Choose format: **YOLOv8**

4. Download and extract into a folder called `dataset/` inside this project.

5. Open `dataset/data.yaml` and update the paths:

```yaml
train: dataset/train/images
val:   dataset/valid/images
test:  dataset/test/images

nc: 1
names: ['Trees']
```

---

### STEP 3 — Train the model

```bash
python train.py
```

This will:
- Download `yolov8n.pt` base weights automatically
- Train for 50 epochs on your mango dataset
- Save the best weights to `runs/mango/train_v1/weights/best.pt`

Training takes ~10–30 minutes on CPU, ~3–5 minutes with a GPU.

---

### STEP 4 — Copy best weights to app folder

```bash
cp runs/mango/train_v1/weights/best.pt best.pt
```

Your folder should now look like:
```
mango-tree-counter/
├── app.py
├── best.pt     ✅  ← this is the key file
├── train.py
└── requirements.txt
```

---

### STEP 5 — Run the app locally

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser. 🎉

---

### STEP 6 — Deploy to Streamlit Cloud

1. Push your project to a **GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "mango tree counter"
   git remote add origin https://github.com/YOUR_USERNAME/mango-tree-counter.git
   git push -u origin main
   ```

2. Go to https://share.streamlit.io

3. Click **New app** → select your repo → set main file to `app.py`

4. Click **Deploy** ✅

> ⚠️ **Important for Streamlit Cloud**: `best.pt` must be committed to GitHub
> (it's a binary file ~6 MB for yolov8n). If it's too large, use Git LFS:
> ```bash
> git lfs install
> git lfs track "*.pt"
> git add .gitattributes best.pt
> git commit -m "add model weights with LFS"
> ```

---

## 🎨 App Features

| Feature | Description |
|---------|-------------|
| 🌿 Dark green UI | Beautiful mango-orchard themed interface |
| 📊 Live stats | Trees detected, images analysed, avg per image |
| 🤖 YOLOv8 detection | Bounding boxes drawn on every tree |
| 🖼️ Side-by-side view | Original vs AI-annotated image |
| 🌴 Total banner | Grand total count across all uploaded images |
| 🗑️ Clear button | Reset session and start fresh |

---

## ⚙️ Customise Training

Edit `train.py` to change:

| Parameter | Default | Options |
|-----------|---------|---------|
| `MODEL`   | `yolov8n.pt` | `yolov8s.pt`, `yolov8m.pt` (more accurate, slower) |
| `EPOCHS`  | `50` | Increase to 100 for better accuracy |
| `BATCH`   | `16` | Lower to 8 if you get memory errors |
| `device`  | `"cpu"` | `0` for GPU (much faster) |

---

## 🛠️ Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: ultralytics` | Run `pip install ultralytics` or check `requirements.txt` |
| `best.pt not found` | Run `train.py` first, then copy the weights file |
| `opencv` error on Streamlit Cloud | Make sure `opencv-python-headless` is in requirements (not `opencv-python`) |
| Out of memory during training | Lower `BATCH` size in `train.py` |
| App runs but 0 trees detected | Check `data.yaml` paths are correct; retrain with more epochs |

---

## 📜 Dataset Info

- **Source**: Roboflow — Mango Tree Count v2
- **Images**: 150 aerial/field images
- **Format**: YOLOv8
- **License**: CC BY 4.0
- **Classes**: 1 (`Trees`)
