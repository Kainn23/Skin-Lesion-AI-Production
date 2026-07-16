import timm
model = timm.create_model("efficientnet_b0", pretrained=False)
for name, module in model.named_modules():
    if "conv" in name.lower() or "layer" in name.lower() or "blocks" in name.lower():
        print(name)
