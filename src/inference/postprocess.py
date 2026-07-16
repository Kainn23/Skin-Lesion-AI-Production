from typing import List, Dict, Any
import numpy as np
import torch


def postprocess_logits(logits: Any, class_names: List[str]) -> Dict[str, Any]:
    """Convert logits into a JSON-serializable prediction payload."""
    if isinstance(logits, torch.Tensor):
        probs = torch.softmax(logits, dim=-1).squeeze(0).detach().cpu().numpy()
    else:
        probs = np.asarray(logits).squeeze(0)
        probs = probs / probs.sum(axis=-1, keepdims=True)

    top_indices = np.argsort(probs)[::-1][:3]

    top3 = [
        {
            "class": class_names[int(idx)],
            "confidence": float(probs[int(idx)]),
        }
        for idx in top_indices
    ]

    best_idx = int(top_indices[0])
    return {
        "prediction": class_names[best_idx],
        "confidence": float(probs[best_idx]),
        "top3": top3,
    }
