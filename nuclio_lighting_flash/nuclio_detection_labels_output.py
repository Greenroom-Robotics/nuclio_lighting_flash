from typing import Any, Dict, List, Optional, Union

from flash.core.data.io.input import DataKeys
from flash.core.data.io.output import Output
from flash.core.model import Task
from flash.core.registry import FlashRegistry
from flash.core.utilities.imports import _FIFTYONE_AVAILABLE, lazy_import, requires
from flash.core.utilities.providers import _FIFTYONE

from flash.core.classification import FiftyOneLabelsOutput


class NuclioDetectionLabelsOutput(Output):
    """A :class:`.Output` which converts model outputs to Nuclio detection format.

    Args:
        image_width: The size the image (before resizing)
        image_height: The size the image (before resizing)
        labels: A list of labels, assumed to map the class index to the label for that class.
        threshold: a score threshold to apply to candidate detections.
    """

    def __init__(
        self,
        image_width: int,
        image_height: int,
        labels: Optional[List[str]] = None,
        threshold: Optional[float] = None,
    ):
        super().__init__()
        self._labels = labels
        self.image_width = image_width
        self.image_height = image_height
        self.threshold = threshold

    @classmethod
    def from_task(cls, task: Task, **kwargs) -> Output:
        return cls(labels=getattr(task, "labels", None))

    def transform(self, sample: Dict[str, Any]) -> List[Dict[str, Any]]:
        if DataKeys.METADATA not in sample:
            raise ValueError(
                "sample requires DataKeys.METADATA to use a FiftyOneDetectionLabelsOutput output."
            )

        # This is the size the image was resized to, i.e. 1024x1024
        height, width = sample[DataKeys.METADATA]["size"]

        detections = []

        preds = sample[DataKeys.PREDS]

        for bbox, label, score in zip(preds["bboxes"], preds["labels"], preds["scores"]):
            confidence = score.tolist()

            if self.threshold is not None and confidence < self.threshold:
                continue

            # The image is resized to "width" x "height" and we want the box relative to
            # the actual image size, "self.image_width", " self.image_height".
            # This is why we "/ width * self.image_width" etc
            box = [
                bbox["xmin"] / width * self.image_width,
                bbox["ymin"] / height * self.image_height,
                (bbox["xmin"] + bbox["width"]) / width * self.image_width,
                (bbox["ymin"] + bbox["height"]) / height * self.image_height,
            ]

            label = label.item()
            if self._labels is not None:
                label = self._labels[label]
            else:
                label = str(int(label))

            detections.append(
                {
                    "confidence": confidence,
                    "label": label,
                    "points": box,
                    "type": "rectangle",
                }
            )
        return detections
