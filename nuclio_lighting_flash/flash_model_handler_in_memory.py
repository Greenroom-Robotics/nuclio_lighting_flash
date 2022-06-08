from typing import Union
import torch
from torchvision import transforms
from flash.image import ObjectDetector
from flash.core.data.io.output import Output
from flash.core.data.io.input import DataKeys
from flash.core.data.data_module import DataModule
from flash.core.data.io.input import DataKeys
from flash.core.data.io.output_transform import OutputTransform
from flash.core.trainer import Trainer
from flash.core.utilities.stages import RunningStage
from flash.core.integrations.icevision.adapter import to_icevision_record

# WORK IN PROGRESS

IMAGE_SIZE = 1024


class MockTrainer(Trainer):
    def __init__(self):
        super().__init__()
        self.state.stage = RunningStage.PREDICTING  # type: ignore


class FlashModelHandler:
    def __init__(self, model_path: str, output: Union[str, Output] = Output()):
        self.model = ObjectDetector(
            head="efficientdet", backbone="d0", num_classes=91, image_size=IMAGE_SIZE
        )
        self.output_transform_final = Output()
        self.trainer = MockTrainer()
        self.data_module = DataModule(batch_size=1)
        self.data_module.trainer = self.trainer  # type: ignore
        self.model.eval()

        self.output_transform = OutputTransform()

    def infer(self, image):
        image_input = {}
        image_input[DataKeys.INPUT] = image
        inputs = {
            DataKeys.INPUT: [
                [transforms.ToTensor()(image).unsqueeze_(0)],
                [to_icevision_record(image_input)],
            ],
            DataKeys.METADATA: {"size": [224, 224]},
        }

        with torch.no_grad():
            inputs = self.model.transfer_batch_to_device(inputs, self.model.device, 0)  # type: ignore
            inputs = self.data_module.on_after_batch_transfer(inputs, 0)
            preds = self.model.predict_step(inputs, 0)
            print("================")
            print(preds)
            # preds = self.output_transform(preds)
            # preds = preds[0][DataKeys.PREDS]
            # preds_output = self.output_transform_final(preds)

            # return {
            #     "confidence": 1,
            #     "label": preds_output,
            #     "points": [0, 0, 10, 10],
            #     "type": "rectangle",
            # }
