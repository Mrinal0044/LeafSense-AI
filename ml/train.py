import os
import argparse
import json
import logging
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ml_train")

def parse_args():
    parser = argparse.ArgumentParser(description="LeafSense AI - Plant Health Model Training")
    parser.add_argument("--dataset-dir", type=str, default="ml/dataset", help="Path to dataset directory")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--img-size", type=int, default=224, help="Input size of images (height and width)")
    parser.add_argument("--learning-rate", type=float, default=0.001, help="Initial learning rate")
    parser.add_argument("--quick-train", action="store_true", help="Enable quick 1-epoch dry-run training on subset")
    parser.add_argument("--output-dir", type=str, default="ml/saved_model", help="Directory to save output model and metadata")
    return parser.parse_args()

def build_model(num_classes, img_shape=(224, 224, 3)):
    """
    Build transfer learning model using EfficientNetB0 as the feature extractor.
    Returns (model, base_model).
    """
    logger.info("Initializing EfficientNetB0 base model...")
    try:
        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False,
            weights="imagenet",
            input_shape=img_shape
        )
        logger.info("Successfully loaded pre-trained ImageNet weights.")
    except Exception as e:
        logger.warning(
            f"Failed to download pre-trained weights ({e}). "
            "Falling back to initializing EfficientNetB0 with random weights (weights=None) for offline development compatibility."
        )
        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False,
            weights=None,
            input_shape=img_shape
        )
    
    # Freeze the base model to prevent weights update during initial training phase
    base_model.trainable = False
    
    # Data Augmentation Layers
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical", name="aug_flip"),
        tf.keras.layers.RandomRotation(0.2, name="aug_rotate"),
        tf.keras.layers.RandomZoom(0.1, name="aug_zoom"),
        tf.keras.layers.RandomTranslation(0.1, 0.1, name="aug_translate"),
    ], name="data_augmentation")

    # Build the full architecture
    inputs = tf.keras.Input(shape=img_shape, name="input_image")
    x = data_augmentation(inputs)
    # Ensure base_model runs in inference mode (crucial for BatchNormalization behavior)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="global_pooling")(x)
    x = tf.keras.layers.BatchNormalization(name="batch_norm")(x)
    x = tf.keras.layers.Dense(256, activation="relu", name="dense_fc")(x)
    x = tf.keras.layers.Dropout(0.4, name="dropout")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="output_classifier")(x)
    
    model = tf.keras.Model(inputs, outputs, name="LeafSense_EfficientNetB0")
    return model, base_model

def plot_and_save_curves(history_list, output_dir):
    """
    Generate and save training accuracy and loss curves from a list of histories.
    """
    loss = []
    val_loss = []
    acc = []
    val_acc = []
    
    for hist in history_list:
        if hist and hasattr(hist, 'history'):
            loss.extend(hist.history.get('loss', []))
            val_loss.extend(hist.history.get('val_loss', []))
            acc.extend(hist.history.get('accuracy', []))
            val_acc.extend(hist.history.get('val_accuracy', []))
            
    epochs_range = range(len(loss))
    if len(loss) == 0:
        return
        
    plt.figure(figsize=(12, 5))
    
    # Loss Curve
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    
    # Accuracy Curve
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "loss_accuracy_curves.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    logger.info(f"Training curves saved to: {plot_path}")

def generate_evaluation_reports(model, val_ds, class_names, output_dir):
    """
    Run prediction on evaluation data, produce classification report and confusion matrix.
    """
    logger.info("Evaluating model on validation dataset...")
    
    y_true = []
    y_pred = []
    
    # Iterate through validation dataset to collect true classes and predictions
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # 1. Save Classification Report
    labels_list = list(range(len(class_names)))
    report = classification_report(y_true, y_pred, labels=labels_list, target_names=class_names, zero_division=0)
    report_path = os.path.join(output_dir, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    logger.info(f"Classification report saved to: {report_path}")
    
    # 2. Save Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels_list)
    plt.figure(figsize=(15, 15))
    
    # Simple manual styling of Confusion Matrix heatmap to avoid dependency issues with seaborn
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=90, fontsize=8)
    plt.yticks(tick_marks, class_names, fontsize=8)
    
    # Annotate counts inside the matrix (if class counts are reasonably small for visibility)
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black",
                     fontsize=6)
                     
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    plt.close()
    logger.info(f"Confusion matrix saved to: {cm_path}")

def main():
    args = parse_args()
    
    # Establish directories
    train_dir = os.path.join(args.dataset_dir, "train")
    valid_dir = os.path.join(args.dataset_dir, "valid")
    
    if not os.path.exists(train_dir) or not os.path.exists(valid_dir):
        raise FileNotFoundError(
            f"Dataset directories not found. Make sure {train_dir} and {valid_dir} exist."
        )
        
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load dataset
    logger.info("Loading training and validation datasets...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        label_mode="categorical"
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        valid_dir,
        image_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        label_mode="categorical",
        shuffle=False
    )
    
    class_names = train_ds.class_names
    num_classes = len(class_names)
    logger.info(f"Loaded dataset with {num_classes} classes.")
    
    # Save class indices metadata mapping
    class_indices = {i: name for i, name in enumerate(class_names)}
    metadata_path = os.path.join(args.output_dir, "class_indices.json")
    with open(metadata_path, "w") as f:
        json.dump(class_indices, f, indent=2)
    logger.info(f"Class indices saved to: {metadata_path}")
    
    # Optimize datasets for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    
    # If quick-train is specified, sub-sample datasets for instant execution
    epochs = args.epochs
    if args.quick_train:
        logger.warning("Quick-train mode is active. Training on a small subset (10 batches) for 1 epoch only.")
        train_ds = train_ds.take(10)
        val_ds = val_ds.take(5)
        epochs = 1
        
    # Build Model
    model, base_model = build_model(num_classes=num_classes, img_shape=(args.img_size, args.img_size, 3))
    
    # Determine epochs for each stage
    if args.quick_train:
        stage1_epochs = 1
        stage2_epochs = 0
    else:
        stage1_epochs = 3
        stage2_epochs = max(1, args.epochs - 3)

    histories = []
    model_save_path = os.path.join(args.output_dir, "plant_disease_model.keras")

    # ==============================================================================
    # STAGE 1: HEAD WARM-UP (Base Model Frozen)
    # ==============================================================================
    logger.info(f"--- STAGE 1: Head Warm-up Training for {stage1_epochs} epoch(s) ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=args.learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    model.summary(print_fn=logger.info)
    
    history_stage1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=stage1_epochs
    )
    histories.append(history_stage1)

    # ==============================================================================
    # STAGE 2: FINE-TUNING (Unfreeze Top 20 Layers of Base Model)
    # ==============================================================================
    if stage2_epochs > 0:
        logger.info(f"--- STAGE 2: Fine-tuning - Unfreezing top 20 layers of EfficientNetB0 base ---")
        base_model.trainable = True
        
        # Freeze all layers except the last 20 layers to maintain low-level filters
        for layer in base_model.layers[:-20]:
            layer.trainable = False
            
        # Recompile with a significantly lower learning rate (10x reduction) to prevent weight distortion
        fine_tune_lr = args.learning_rate * 0.1
        logger.info(f"Recompilation learning rate: {fine_tune_lr}")
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=fine_tune_lr),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        
        model.summary(print_fn=logger.info)
        
        # Setup callbacks for fine-tuning
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                filepath=model_save_path,
                monitor="val_loss",
                save_best_only=True,
                verbose=1
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.2,
                patience=3,
                min_lr=1e-6,
                verbose=1
            )
        ]
        
        history_stage2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=stage2_epochs,
            callbacks=callbacks
        )
        histories.append(history_stage2)

    # Save final model if not saved by checkpoints or if in quick-train mode
    if not os.path.exists(model_save_path) or args.quick_train:
        model.save(model_save_path)
        logger.info(f"Saved fallback model weights to: {model_save_path}")
        
    # Plot training Curves combining both stages
    plot_and_save_curves(histories, args.output_dir)
    
    # Generate Evaluation Charts & Reports
    generate_evaluation_reports(model, val_ds, class_names, args.output_dir)
    
    logger.info("LeafSense AI ML Pipeline Training Phase completed successfully.")

if __name__ == "__main__":
    main()
