from __future__ import annotations
import json
import base64
from PIL import Image
import io
import yaml

from flash.image import ObjectDetector
from flash_model_handler import FlashModelHandler


def init_context(context):
    context.logger.info("Init context...  0%")

    # Read labels
    with open("/opt/nuclio/function.yaml", "rb") as function_file:
        functionconfig = yaml.safe_load(function_file)
    annotations = labels_spec = functionconfig["metadata"]["annotations"]

    labels_spec = annotations["spec"]
    labels = {item["id"]: item["name"] for item in json.loads(labels_spec)}

    # Read the DL model
    # Either "checkpoint_path" or "head" and "backbone" should be specified
    model = (
        ObjectDetector.load_from_checkpoint(annotations["checkpoint_path"])
        if "checkpoint_path" in annotations
        else ObjectDetector(
            head=annotations["head"],
            backbone=annotations["backbone"],
            num_classes=len(labels),
            image_size=1024,
        )
    )
    model_handler = FlashModelHandler(model=model, image_size=1024, labels=labels)
    context.user_data.model = model_handler

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run Lighting Flash model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    threshold = float(data.get("threshold", 0.5))
    image = Image.open(buf)

    results = context.user_data.model.infer(image, threshold)

    return context.Response(
        body=json.dumps(results),
        headers={},
        content_type="application/json",
        status_code=200,
    )
