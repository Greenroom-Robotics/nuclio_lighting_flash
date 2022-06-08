from typing import Any, Dict, List, Optional, Union

from flash.core.data.io.input import DataKeys
from flash.core.data.io.output import Output
from flash.core.model import Task
from flash.core.registry import FlashRegistry
from flash.core.utilities.imports import _FIFTYONE_AVAILABLE, lazy_import, requires
from flash.core.utilities.providers import _FIFTYONE


class NuclioDetectionLabelsOutput(Output):
    """A :class:`.Output` which converts model outputs to Nuclio detection format.

    Args:
        labels: A list of labels, assumed to map the class index to the label for that class.
        threshold: a score threshold to apply to candidate detections.
    """

    def __init__(
        self,
        labels: Optional[List[str]] = None,
        threshold: Optional[float] = None,
    ):
        super().__init__()
        self._labels = labels
        self.threshold = threshold

    @classmethod
    def from_task(cls, task: Task, **kwargs) -> Output:
        return cls(labels=getattr(task, "labels", None))

    def transform(self, sample: Dict[str, Any]) -> List[Dict[str, Any]]:
        detections = []

        preds = sample[DataKeys.PREDS]

        for bbox, label, score in zip(
            preds["bboxes"], preds["labels"], preds["scores"]
        ):
            confidence = score.tolist()

            if self.threshold is not None and confidence < self.threshold:
                continue

            box = [
                bbox["xmin"],
                bbox["ymin"],
                bbox["xmin"] + bbox["width"],
                bbox["ymin"] + bbox["height"],
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
