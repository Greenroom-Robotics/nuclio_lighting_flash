from PIL import Image
from flash.image import ObjectDetector
import os

from flash_model_handler import FlashModelHandler


def test_flash_model_handler():
    """
    Runs the flash model handler (bypassing nuclio)
    Should detect giraffes in the COCO image
    """
    model = ObjectDetector(head="efficientdet", backbone="d0", num_classes=91, image_size=1024)
    model_handler = FlashModelHandler(model=model, image_size=1024, labels={25: "giraffe"})
    image = Image.open(os.path.join(os.getcwd(), "./fixtures/giraffe.jpg"))

    result = model_handler.infer(image, 0.0)

    assert len(result) == 2
    assert result[0]["label"] == "giraffe"
    assert result[1]["label"] == "giraffe"
