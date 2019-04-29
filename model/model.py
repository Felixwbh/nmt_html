import time


class MyModel(object):
    def __init__(self):
        time.sleep(1)
        print("Model loaded")

    def translate(self, input):
        time.sleep(1)
        return "TRANSLATED " + input


def load_model() -> MyModel:
    print("Loading model...")
    return MyModel()


def translate(model: MyModel, input: str) -> str:
    return model.translate(input)
