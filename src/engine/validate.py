import torch
from tqdm import tqdm


def validate(
    model,
    loader,
    criterion,
    device,
    desc="Validation",
):
    model.eval()

    running_loss = 0.0
    predictions = []
    targets = []

    with torch.no_grad():

        for images, labels in tqdm(
            loader,
            desc=desc,
            unit="batch",
            leave=False,
        ):

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)

            preds = outputs.argmax(dim=1)

            predictions.extend(preds.cpu().numpy())
            targets.extend(labels.cpu().numpy())

    epoch_loss = running_loss / len(loader.dataset)

    return epoch_loss, predictions, targets