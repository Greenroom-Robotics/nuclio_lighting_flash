import json
import os

from main import init_context, handler
from fixtures.fixtures_nuclio import Context, Event


def test_main():
    """
    Runs main nuclio function with a fake nuclio context
    """
    context = Context()
    init_context(context)

    event = Event(image_path=os.path.join(os.getcwd(), "./fixtures/giraffe.jpg"), threshold=0.5)
    response = handler(context, event)
    assert response.body == json.dumps(
        [
            {
                "confidence": 0.92,
                "label": "giraffe",
                "points": [372.63, 114.84, 601.54, 315.84],
                "type": "rectangle",
            },
            {
                "confidence": 0.87,
                "label": "giraffe",
                "points": [52.77, 305.4, 185.64, 349.67],
                "type": "rectangle",
            },
        ]
    )
