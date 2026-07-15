import os
import argparse
import json
import cv2
import numpy as np
import tensorflow as tf

def parse_args():
    parser = argparse.ArgumentParser(description="LeafSense AI - Plant Health Model Inference")
    parser.add_argument("--image", type=str, required=True, help="Path to input leaf image")
    parser.add_argument("--model", type=str, default="ml/saved_model/plant_disease_model.keras", help="Path to trained Keras model")
    parser.add_argument("--class-indices", type=str, default="ml/saved_model/class_indices.json", help="Path to class indices JSON file")
    parser.add_argument("--disease-info", type=str, default="ml/saved_model/disease_info.json", help="Path to disease details database JSON file")
    return parser.parse_args()

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Read an image using OpenCV, convert from BGR to RGB, and resize to target_size.
    EfficientNetB0 handles its own normalization, so we feed raw pixel values.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")
        
    # Read image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image file (possibly corrupted or unsupported format): {image_path}")
        
    # Convert BGR (OpenCV default) to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to target size (224x224 for EfficientNetB0)
    img = cv2.resize(img, target_size)
    
    # Add batch dimension: (1, 224, 224, 3)
    img_batch = np.expand_dims(img, axis=0).astype(np.float32)
    return img_batch

def predict(image_path, model_path, class_indices_path, disease_info_path):
    """
    Load resources, run inference, and compile prediction results with crop disease details.
    """
    # 1. Load class indices mapping
    if not os.path.exists(class_indices_path):
        raise FileNotFoundError(f"Class indices mapping file not found at: {class_indices_path}")
    with open(class_indices_path, "r") as f:
        class_indices = json.load(f)
        
    # 2. Load disease detailed information
    if not os.path.exists(disease_info_path):
        raise FileNotFoundError(f"Disease information file not found at: {disease_info_path}")
    with open(disease_info_path, "r") as f:
        disease_database = json.load(f)

    # 3. Load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at: {model_path}. Please run train.py first.")
    
    # Suppress tf warnings for clean output
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    model = tf.keras.models.load_model(model_path)
    
    # 4. Preprocess input image
    processed_img = preprocess_image(image_path)
    
    # 5. Run inference
    predictions = model.predict(processed_img, verbose=0)[0]
    predicted_idx = str(np.argmax(predictions))
    confidence = float(predictions[int(predicted_idx)])
    
    # Map index to directory class name
    class_folder = class_indices.get(predicted_idx)
    if not class_folder:
        raise ValueError(f"Predicted index {predicted_idx} not found in class indices mappings.")

    # 6. Retrieve disease details
    details = disease_database.get(class_folder, {
        "name": class_folder.replace("___", " ").replace("_", " "),
        "scientific_name": "Unknown",
        "description": "No detailed description available in database.",
        "symptoms": "N/A",
        "causes": "N/A",
        "treatment": "N/A",
        "prevention": "N/A"
    })

    # Compile report structure
    report = {
        "class_id": class_folder,
        "disease_name": details.get("name"),
        "scientific_name": details.get("scientific_name"),
        "confidence": confidence,
        "is_healthy": "healthy" in class_folder.lower(),
        "details": {
            "description": details.get("description"),
            "symptoms": details.get("symptoms"),
            "causes": details.get("causes"),
            "treatment": details.get("treatment"),
            "prevention": details.get("prevention")
        }
    }
    return report

def main():
    args = parse_args()
    try:
        result = predict(
            image_path=args.image,
            model_path=args.model,
            class_indices_path=args.class_indices,
            disease_info_path=args.disease_info
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }, indent=2))
        exit(1)

if __name__ == "__main__":
    main()
