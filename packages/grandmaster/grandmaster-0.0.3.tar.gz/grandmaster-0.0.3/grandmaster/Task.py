import inspect
from grandmaster import models
from typing import Optional, List, Literal

from pydantic import BaseModel, create_model
from grandmaster.helper import read_image

from grandmaster.tasks import all_tasks


class Task:
    def get_model(self, input) -> models.Model:
        self.task_name = input.task_name
        self.model_name = input.model_name

        for model in models.all_models:
            if model.task.name == self.task_name:
                return model()
        raise ValueError(f"Task {self.task_name} not found")

    def __call__(self, *args, **kwargs) -> models.Model:
        return self.get_model(*args, **kwargs)


from pydantic import BaseModel


# TODO generate this dynamically
class Input(BaseModel):
    task_name: str
    model_name: str


def predict_int(input: Input):
    task = Task()
    model = task.get_model(input)
    return model.prediction(input)


def xxx():
    import requests


from typing import List
from pydantic import BaseModel
from fastapi import UploadFile
import json


class Input(BaseModel):
    image: UploadFile
    candidate_labels: List[str]


import requests


import requests
from typing import List
from pydantic import BaseModel
from fastapi import UploadFile


class Input(BaseModel):
    image: UploadFile
    candidate_labels: List[str]


def fastapi_pydantic_to_request(
    pydantic_object: BaseModel, url: str
) -> requests.Response:
    files = {}

    for field, value in pydantic_object.dict().items():
        if isinstance(value, UploadFile):
            files[field] = (value.filename, value.file)
        elif isinstance(value, List):
            files[field] = (None, str(",".join(value)))
        else:
            files[field] = (None, str(value))

    response = requests.post(url, files=files)

    return response


def predict(*args, **kwargs):
    task_name = kwargs["task_name"]

    task = None
    for t in all_tasks:
        if t.name == task_name:
            task = t
            break

    if not task:
        return

    if kwargs.get("api"):
        print("Use api")

        response = fastapi_pydantic_to_request(
            task.Inputs(**kwargs), "http://localhost:8080/image-classification"
        )

        x = response.json()
        print(x)
        return x

    # TODO
    if "image" in kwargs:
        kwargs["image"] = read_image(kwargs["image"])

    models = task.get_models()

    model = None
    for m in models:
        if m.model_name == t.default_model_name:
            model = m
            break

    mm = model()
    mm.load_model()
    x = mm.predict(task.Inputs(**kwargs))
    return x.dict()
