import json
from multiprocessing import freeze_support

import torch
from sklearn.model_selection import train_test_split

from src.datasets.ham10000 import HAM10000DatasetInfo
from src.datasets.dataloader import create_dataloaders
from src.models.factory import create_model
from src.losses.focal_losses import FocalLoss
from src.utils.optimizer import get_optimizer
from src.utils.scheduler import get_scheduler
from src.engine.trainer import Trainer


def main():

    # =====================================
    # Device
    # =====================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print(f"\nUsing Device: {device}\n")

    # =====================================
    # Load Dataset
    # =====================================

    dataset = HAM10000DatasetInfo()

    df = dataset.load()

    print(f"Total Images: {len(df)}")
    print(f"Classes: {dataset.get_classes()}\n")

    # =====================================
    # Train / Validation / Test Split
    # =====================================

    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df["label"],
        random_state=42,
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df["label"],
        random_state=42,
    )

    print(f"Train      : {len(train_df)}")
    print(f"Validation : {len(val_df)}")
    print(f"Test       : {len(test_df)}\n")

    # =====================================
    # DataLoaders
    # =====================================

    train_loader, val_loader, test_loader = create_dataloaders(
        train_df,
        val_df,
        test_df,
        batch_size=32,
        num_workers=0,      # Change to 4 later if desired
    )

    images, labels = next(iter(train_loader))

    print(f"Batch Images : {images.shape}")
    print(f"Batch Labels : {labels.shape}\n")

    # =====================================
    # Model
    # =====================================

    model = create_model(
        model_name="efficientnet_b3",
        num_classes=len(dataset.get_classes()),
        pretrained=True,
    )

    model = model.to(device)

    print("Model Loaded Successfully!\n")

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(
        p.numel() for p in model.parameters()
        if p.requires_grad
    )

    print(f"Total Parameters     : {total_params:,}")
    print(f"Trainable Parameters : {trainable_params:,}")

    # =====================================
    # Loss, Optimizer, Scheduler, Trainer
    # =====================================

    criterion = FocalLoss(
        gamma=2.0,
    )

    optimizer = get_optimizer(
        model,
        lr=3e-4,
        weight_decay=1e-4,
    )

    scheduler = get_scheduler(optimizer)

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        epochs=25,
    )

    print("\nStarting training...\n")
    results = trainer.fit()
    print(f"Best Macro F1 : {results['best_macro_f1']:.4f}")

    # Save training history
    with open("logs/training_history.json", "w") as f:
        json.dump(results["history"], f, indent=2)


if __name__ == "__main__":
    freeze_support()
    main()