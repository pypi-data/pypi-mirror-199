from typing import BinaryIO, Literal, get_args
from dataclasses import dataclass
import requests


# this will get more sophisticated as far as configuration goes, we'll want to abtract these into classes and leverage inheritance for various config options
tasks = {
    "style-transfer": {
        "fast-style-transfer": "https://fast-style-transfer-tfhmsoxnpq-uc.a.run.app",
        "cmd_styletransfer": "https://cmd-styletransfer-tfhmsoxnpq-uc.a.run.app",
        "tensorflow-fast-style-transfer": "https://tensorflow-fast-style-transfer-tfhmsoxnpq-uc.a.run.app"
    }
}


@dataclass
class Handler:
    url: str

    def inference(self, input_img: BinaryIO) -> bytes:
        files = {'image': input_img}
        response = requests.post(self.url, files=files)

        # reset seek index to start of file
        input_img.seek(0)

        if not response.ok:
            raise Exception(f'Request failed with {response.status_code}')

        return response.content

# TODO use enums to accomplish this


def pipeline(task,
             model) -> Handler:
    task = tasks.get(task)

    if not task:
        raise Exception(f"{task} is not supported by this package.")

    url = task.get(model)

    if not url:
        raise Exception(f"{model} is not supported by this package.")

    return Handler(url=url)
