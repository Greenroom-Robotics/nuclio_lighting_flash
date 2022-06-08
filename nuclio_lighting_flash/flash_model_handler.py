from flash.image import ObjectDetector, ObjectDetectionData
from flash.core.trainer import Trainer
from flash.core.utilities.stages import RunningStage
from PIL.Image import Image

from nuclio_detection_labels_output import NuclioDetectionLabelsOutput


class MockTrainer(Trainer):
    def __init__(self):
        super().__init__()
        self.state.stage = RunningStage.PREDICTING  # type: ignore


class FlashModelHandler:
    def __init__(
        self,
        model: ObjectDetector,
        image_size = 1024,
        labels = {}
    ):
        self.image_size = image_size
        self.labels = labels
        self.model = model
        self.trainer = MockTrainer()
        self.model.eval()

    def infer(self, image: Image, threshold: float = 0.0):
        path = "/tmp/image.jpg"
        image.save(path)

        datamodule = ObjectDetectionData.from_files(
            predict_files=[path],
            transform_kwargs={"image_size": self.image_size},
            batch_size=1,
        )
        predictions = self.trainer.predict(
            self.model,
            datamodule=datamodule,
            output=NuclioDetectionLabelsOutput(threshold=threshold, labels=self.labels),
        )
        return predictions