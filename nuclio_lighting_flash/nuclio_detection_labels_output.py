from typing import Any, Dict, List, Optional, Union

from flash.core.data.io.input import DataKeys
from flash.core.data.io.output import Output
from flash.core.model import Task
from icevision.tfms import A
from icevision.core import BBox
from icevision.models.inference import postprocess_bbox
from PIL.Image import Image


class NuclioDetectionLabelsOutput(Output):
    """A :class:`.Output` which converts model outputs to Nuclio detection format.

    Args:
        image: The image (before resizing)
        labels: A list of labels, assumed to map the class index to the label for that class.
        threshold: a score threshold to apply to candidate detections.
    """

    def __init__(
        self,
        image: Image,
        labels: Optional[List[str]] = None,
        threshold: Optional[float] = None,
    ):
        super().__init__()
        self._labels = labels
        self.image = image
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

            # The bboxes are for the width/height after the image has been transformed
            # we need to undo this transform so thos bboxes are relative to the initial
            # image dimensions.
            # We can leverage some icevision logic to do this...
            size = width if width == height else (width, height)
            transform = A.Adapter(A.resize_and_pad(size))
            ice_bbox = BBox(
                bbox["xmin"],
                bbox["ymin"],
                bbox["xmin"] + bbox["width"],
                bbox["ymin"] + bbox["height"],
            )
            points = postprocess_bbox(self.image, ice_bbox, transform.tfms_list, height, width)

            label = label.item()
            if self._labels is not None:
                label = self._labels[label]
            else:
                label = str(int(label))

            detections.append(
                {
                    "confidence": round(confidence, 2),
                    "label": label,
                    "points": points,
                    "type": "rectangle",
                }
            )
        return detections
