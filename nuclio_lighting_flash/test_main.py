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
                "confidence": 0.9171872138977051,
                "label": "giraffe",
                "points": [
                    372.63145446777344,
                    114.83981323242188,
                    601.5438079833984,
                    315.83863592147827,
                ],
                "type": "rectangle",
            },
            {
                "confidence": 0.8744097352027893,
                "label": "giraffe",
                "points": [
                    52.77256488800049,
                    305.4035350084305,
                    185.64495086669922,
                    349.67146718502045,
                ],
                "type": "rectangle",
            },
        ]
    )
