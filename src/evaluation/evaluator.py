from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from tqdm import tqdm


def evaluate_model(
    model: torch.nn.Module,
    loader: torch.utils.data.DataLoader,
    device: torch.device,
    class_names: Optional[List[str]] = None,
) -> Dict[str, object]:
    """Run model on `loader` and compute common evaluation metrics.

    Returns a dictionary containing:
    - "metrics": dict of accuracy/precision/recall/weighted_f1/macro_f1
    - "confusion_matrix": np.ndarray (n_classes x n_classes)
    - "y_true": np.ndarray
    - "y_pred": np.ndarray
    - "y_score": np.ndarray of shape (n_samples, n_classes) with softmax 
    scores

    This is intentionally minimal: plotting and advanced visualizations
    are left to separate helper functions.
    """

    model.eval()

    device = torch.device(device)
    model.to(device)

    y_true: List[int] = []
    y_pred: List[int] = []
    y_score: List[np.ndarray] = []

    with torch.no_grad():
        for images, labels in tqdm(
            loader,
            desc="Evaluating",
            unit="batch",
            leave=False,
        ):
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            if isinstance(outputs, tuple):
                outputs = outputs[0]

            probs = F.softmax(outputs, dim=1).cpu().numpy()
            preds = probs.argmax(axis=1)

            y_true.extend(labels.cpu().numpy().tolist())
            y_pred.extend(preds.tolist())
            y_score.extend(probs.tolist())

    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    y_score_arr = np.array(y_score)

    n_classes = y_score_arr.shape[1]

    metrics = {
        "accuracy": accuracy_score(y_true_arr, y_pred_arr),
        "precision": precision_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0),
        "recall": recall_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0),
        "weighted_f1": f1_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0),
        "macro_f1": f1_score(y_true_arr, y_pred_arr, average="macro", zero_division=0),
    }

    cm = confusion_matrix(y_true_arr, y_pred_arr)

    # Compute ROC AUC if possible (multiclass with one-vs-rest)
    roc_auc: Optional[float] = None
    try:
        if n_classes == 2:
            roc_auc = roc_auc_score(y_true_arr, y_score_arr[:, 1])
        else:
            # one-vs-rest macro
            roc_auc = roc_auc_score(y_true_arr, y_score_arr, multi_class="ovr")
    except Exception:
        roc_auc = None

    if roc_auc is not None:
        metrics["roc_auc"] = float(roc_auc)

    result: Dict[str, object] = {
        "metrics": metrics,
        "confusion_matrix": cm,
        "y_true": y_true_arr,
        "y_pred": y_pred_arr,
        "y_score": y_score_arr,
    }

    if class_names is not None:
        result["class_names"] = class_names

    return result
