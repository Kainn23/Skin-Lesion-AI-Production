import numpy as np
import torch
from torch.utils.data import WeightedRandomSampler


def create_weighted_sampler(train_df):
    """
    Creates a WeightedRandomSampler using inverse sqrt class frequency.

    Args:
        train_df (pd.DataFrame): Training dataframe containing 'label'

    Returns:
        WeightedRandomSampler
    """

    labels = train_df["label"].to_numpy()
    class_counts = np.bincount(labels)

    print("\nClass Counts:")
    print(class_counts)

    class_weights = 1.0 / np.sqrt(class_counts)

    print("\nClass Weights:")
    print(class_weights)

    sample_weights = class_weights[labels]
    sample_weights = torch.as_tensor(sample_weights, dtype=torch.double)

    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True,
    )

    return sampler
