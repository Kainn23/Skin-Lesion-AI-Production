import timm

def create_model(model_name: str, num_classes: int, pretrained: bool = False):
    """
    Factory function to create a PyTorch model.
    
    Args:
        model_name (str): Name of the model architecture (e.g., 'efficientnet_b0').
        num_classes (int): Number of output classes.
        pretrained (bool): Whether to load pretrained weights.
        
    Returns:
        torch.nn.Module: The created model.
    """
    return timm.create_model(
        model_name,
        pretrained=pretrained,
        num_classes=num_classes
    )
