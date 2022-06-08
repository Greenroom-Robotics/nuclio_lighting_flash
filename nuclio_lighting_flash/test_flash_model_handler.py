from PIL import Image
from flash.image import ObjectDetector
import os

from flash_model_handler import FlashModelHandler

model = ObjectDetector(
    head="efficientdet",
    backbone="d0",
    num_classes=91,
    image_size=1024
)
model_handler = FlashModelHandler(
    model=model,
    image_size=1024,
    labels={
        25: "giraffe"
    }
)
image = Image.open(os.path.join(os.getcwd(), "./fixtures/giraffe.jpg"))

result = model_handler.infer(image, 0)
print(result)
