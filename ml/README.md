# LeafSense AI – Machine Learning Pipeline

This folder contains the Machine Learning code, dataset structures, trained weights, and inference scripts for the plant disease detection model.

We utilize **Transfer Learning** using the pre-trained **EfficientNetB0** architecture, which achieves high accuracy with excellent computational efficiency.

---

## 📂 Folder Structure

```text
ml/
├── dataset/                  # PlantVillage dataset split
│   ├── train/                # 38 Crop & disease training classes (~38k images)
│   ├── valid/                # Validation subset (~10k images)
│   └── test/                 # Holdout test set (~5.4k images)
├── models/                   # Folder for intermediate weights / checkpoints
├── saved_model/              # Production output directory
│   ├── plant_disease_model.keras  # Best saved Keras model weights
│   ├── class_indices.json    # Category index mapper
│   ├── disease_info.json     # Detailed plant pathology knowledge base
│   ├── loss_accuracy_curves.png   # Training plot output
│   ├── confusion_matrix.png  # Confusion matrix plot
│   └── classification_report.txt  # Precision, recall, and F1 metrics
├── train.py                  # Orchestration script to run model training
├── predict.py                # Single-image prediction pipeline
└── requirements.txt          # ML dependencies (TensorFlow, OpenCV, NumPy, etc.)
```

---

## ⚡ Training Pipeline (`train.py`)

The training script loads raw images, resizes them, runs custom on-the-fly data augmentations, initializes the CNN model with pre-trained ImageNet weights, and trains the dense classification head.

### CLI Parameters
- `--dataset-dir`: Path to database root folder containing `train` and `valid` (default: `ml/dataset`)
- `--epochs`: Number of training epochs (default: `15`)
- `--batch-size`: Batch size (default: `32`)
- `--img-size`: Input dimensions for the network (default: `224`)
- `--learning-rate`: Base rate for Adam optimizer (default: `0.001`)
- `--quick-train`: Restricts training to a tiny sub-sample (10 batches, 1 epoch) to instantly generate model artifacts for verification.
- `--output-dir`: Path to write the output model and charts (default: `ml/saved_model`)

### Run Training

#### Option A: Quick Verification Run (Recommended for Dev Setup)
Runs a 1-epoch dry run on a small dataset batch to quickly verify everything compiles and produces mock model weights.
```bash
python ml/train.py --quick-train
```

#### Option B: Full Pipeline Training
Trains the full model on the complete dataset (~38,000 images).
```bash
python ml/train.py --epochs 15 --batch-size 32
```

---

## 🔍 Model Inference (`predict.py`)

Use the prediction utility to perform inference on individual leaf images. It returns the predicted crop disease class, confidence percentage, and complete pathology information from our clinical database.

### Usage
Run the following script, passing the path to the leaf image:
```bash
python ml/predict.py --image path/to/leaf_image.jpg
```

### JSON Output Format
```json
{
  "class_id": "Tomato___Early_blight",
  "disease_name": "Tomato Early Blight",
  "scientific_name": "Alternaria solani",
  "confidence": 0.9412,
  "is_healthy": false,
  "details": {
    "description": "A common fungal disease causing circular spots with concentric rings on older tomato leaves.",
    "symptoms": "Dark spots with concentric target-like rings on lower leaves; leaves turn yellow and drop off.",
    "causes": "Fungal pathogen overwintering in crop residues...",
    "treatment": "Apply copper or chlorothalonil fungicides...",
    "prevention": "Prune lower leaves to prevent contact with soil; apply thick organic mulch..."
  }
}
```
