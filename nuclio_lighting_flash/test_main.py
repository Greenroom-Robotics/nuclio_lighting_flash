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
                "points": [596.2103271484375, 276.046875, 962.4700927734375, 759.198974609375],
                "type": "rectangle",
            },
            {
                "confidence": 0.8744097352027893,
                "label": "giraffe",
                "points": [
                    84.43610382080078,
                    734.1155395507812,
                    297.03192138671875,
                    840.5248413085938,
                ],
                "type": "rectangle",
            },
        ]
    )
