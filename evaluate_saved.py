"""Load saved weights and evaluate the trained model on the test set.

Usage:
    python evaluate_saved.py

This script mirrors the train splits in `train.py`, loads `weights/best_model.pth`,
and runs `src.evaluation.evaluator.evaluate_model`.
"""
from __future__ import annotations

import os
import sys
from typing import Dict

import torch
from sklearn.model_selection import train_test_split

from src.datasets.ham10000 import HAM10000DatasetInfo
from src.datasets.dataloader import create_dataloaders
from src.models.factory import create_model
from src.evaluation.evaluator import evaluate_model


def load_checkpoint_into_model(model, weights_path, device):
    """Load a checkpoint into a model from either a raw state_dict or a trainer payload."""
    state = torch.load(weights_path, map_location=device)

    if isinstance(state, dict):
        if "model_state_dict" in state and isinstance(state["model_state_dict"], dict):
            state = state["model_state_dict"]
        elif "state_dict" in state and isinstance(state["state_dict"], dict):
            state = state["state_dict"]

    if not isinstance(state, dict):
        raise TypeError("Loaded object is not a state dict. Inspect the file manually.")

    stripped = {k.replace("module.", ""): v for k, v in state.items()}

    try:
        model.load_state_dict(stripped)
    except RuntimeError:
        model_keys = set(model.state_dict().keys())
        state_keys = set(stripped.keys())

        missing = model_keys - state_keys
        unexpected = state_keys - model_keys

        if missing or unexpected:
            print("Warning: key mismatch when loading state_dict.")
            if missing:
                print(f"Missing keys in checkpoint: {len(missing)} (showing up to 10): {list(missing)[:10]}")
            if unexpected:
                print(f"Unexpected keys in checkpoint: {len(unexpected)} (showing up to 10): {list(unexpected)[:10]}")

        model.load_state_dict(stripped, strict=False)

    return model


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = HAM10000DatasetInfo()
    df = dataset.load()

    # reproduce same splits as training
    train_df, temp_df = train_test_split(
        df, test_size=0.2, stratify=df["label"], random_state=42
    )

    val_df, test_df = train_test_split(
        temp_df, test_size=0.5, stratify=temp_df["label"], random_state=42
    )

    _, _, test_loader = create_dataloaders(
        train_df, val_df, test_df, batch_size=32, num_workers=0
    )

    model = create_model(
        model_name="efficientnet_b3",
        num_classes=len(dataset.get_classes()),
        pretrained=True,
    )

    weights_path = os.path.join("weights", "best_model.pth")
    if not os.path.exists(weights_path):
        sys.exit(f"Weights not found: {weights_path}")

    try:
        model = load_checkpoint_into_model(model, weights_path, device)
    except (TypeError, RuntimeError) as exc:
        sys.exit(str(exc))

    model.to(device)
    model.eval()

    result: Dict = evaluate_model(model, test_loader, device, class_names=dataset.get_classes())

    print("Evaluation metrics:")
    for k, v in result["metrics"].items():
        print(f"  {k}: {v:.4f}")

    print("Confusion matrix shape:", result["confusion_matrix"].shape)


if __name__ == "__main__":
    main()
