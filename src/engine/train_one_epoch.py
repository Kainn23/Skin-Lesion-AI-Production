import torch

from tqdm import tqdm


def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    device,
    desc="Training",
):

    model.train()

    running_loss = 0

    predictions = []

    targets = []

    for images, labels in tqdm(
        loader,
        desc=desc,
        unit="batch",
        leave=False,
    ):

        images = images.to(device)

        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item() * images.size(0)

        preds = outputs.argmax(dim=1)

        predictions.extend(preds.cpu().numpy())

        targets.extend(labels.cpu().numpy())

    epoch_loss = running_loss / len(loader.dataset)

    return epoch_loss, predictions, targets