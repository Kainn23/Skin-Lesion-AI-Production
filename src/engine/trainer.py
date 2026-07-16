import copy
import time
import torch

from src.engine.train_one_epoch import train_one_epoch
from src.engine.validate import validate
from src.utils.metrics import compute_metrics


class Trainer:

    def __init__(
        self,
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        scheduler,
        device,
        epochs,
    ):

        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader

        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler

        self.device = device

        self.epochs = epochs

        self.best_model = copy.deepcopy(model.state_dict())

        self.best_macro_f1 = 0
        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": [],
            "macro_f1": [],
            "learning_rate": [],
        }

    def fit(self):

        patience = 5
        counter = 0

        for epoch in range(self.epochs):
            start = time.time()

            print("=" * 60)
            print(f"Epoch {epoch+1}/{self.epochs}")
            print("=" * 60)

            train_loss, train_preds, train_targets = train_one_epoch(
                self.model,
                self.train_loader,
                self.criterion,
                self.optimizer,
                self.device,
                desc=f"Training epoch {epoch+1}/{self.epochs}",
            )

            val_loss, val_preds, val_targets = validate(
                self.model,
                self.val_loader,
                self.criterion,
                self.device,
                desc=f"Validation epoch {epoch+1}/{self.epochs}",
            )

            train_metrics = compute_metrics(
                train_targets,
                train_preds,
            )

            val_metrics = compute_metrics(
                val_targets,
                val_preds,
            )

            self.history["train_loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["train_acc"].append(train_metrics["accuracy"])
            self.history["val_acc"].append(val_metrics["accuracy"])
            self.history["macro_f1"].append(val_metrics["macro_f1"])
            self.history["learning_rate"].append(
                self.optimizer.param_groups[0]["lr"]
            )

            if self.scheduler is not None:
                self.scheduler.step(val_loss)

            current_lr = self.optimizer.param_groups[0]["lr"]
            epoch_time = time.time() - start

            print(f"Train Loss : {train_loss:.4f}")
            print(f"Val Loss   : {val_loss:.4f}")
            print(f"Train Acc  : {train_metrics['accuracy']:.4f}")
            print(f"Val Acc    : {val_metrics['accuracy']:.4f}")
            print(f"Macro F1   : {val_metrics['macro_f1']:.4f}")
            print(f"Learning Rate : {current_lr:.6f}")
            print(f"Epoch Time : {epoch_time:.2f} sec")

            if val_metrics["macro_f1"] > self.best_macro_f1:
                self.best_macro_f1 = val_metrics["macro_f1"]
                self.best_model = copy.deepcopy(self.model.state_dict())

                checkpoint = {
                    "epoch": epoch,
                    "model_state_dict": self.model.state_dict(),
                    "optimizer_state_dict": self.optimizer.state_dict(),
                    "scheduler_state_dict": (
                        self.scheduler.state_dict() if self.scheduler else None
                    ),
                    "macro_f1": self.best_macro_f1,
                }

                torch.save(checkpoint, "weights/best_model.pth")
                counter = 0
                print("New Best Model Saved!")
            else:
                counter += 1
                if counter >= patience:
                    print("Early stopping triggered.")
                    break

        print("\nTraining Finished!")
        torch.save(self.model.state_dict(), "weights/last_model.pth")
        self.model.load_state_dict(self.best_model)

        return {
            "history": self.history,
            "best_macro_f1": self.best_macro_f1,
        }