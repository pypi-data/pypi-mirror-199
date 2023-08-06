from typing import List
from grandmaster.inputs import Image, Label
from grandmaster.outputs import LabelWithScore
from grandmaster.tasks import ImageClassification
from grandmaster.Model import Model

from transformers import pipeline


"""
class CLIP(Model):
    # image classification
    def __init__(self):
        from transformers import CLIPProcessor, CLIPModel

        self.xmodel = lambda: CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
        self.xprocessor = lambda: CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch16"
        )

        self.model_name = "openai/clip-vit-base-patch16"

        self.inputs: List[InputsTypedDict] = [
            {"dataType": "IMAGE"},
            {"dataType": "TEXT"},
        ]
        self.outputs: List[OutputsTypedDict] = [{"dataType": "LABEL"}]

    def load(self):
        self.xmodel()
        self.xprocessor()

    def tasks(self):
        return [
            create_task(
                self.model_name,
                self.inputs,
                self.outputs,
                self.apply,
                self.preprocess,
                self.postprocess,
            )
        ]

    def apply(self, query: ImageZeroShotQueryTypedDict) -> Any:
        image = load_image_from_data(query["image"])
        processed = self.xprocessor()(
            text=query["candidate_labels"].split(","),
            images=image,
            return_tensors="pt",
            padding=True,
        )
        x = self.xmodel()(**processed)  # type: ignore
        results = list(x.logits_per_image.softmax(dim=1).detach().numpy()[0])
        out: List[ResultLabelDC] = []
        for i, r in zip(query["candidate_labels"].split(","), results):
            out.append(ResultLabelDC(label=i, score=r.item()))
        return out

    def postprocess(self, x: Any) -> List[ResultLabelDC]:
        return x

    def preprocess(self, query: ImageZeroShotQueryTypedDict) -> Any:
        return query
"""

from pydantic import BaseModel

from PIL import Image as PILImage
from fastapi import UploadFile
from io import BytesIO


def uploadfile_to_pil(uploadfile: UploadFile) -> PILImage.Image:
    # Read the contents of the file
    contents = uploadfile.file.read()

    # Create a file-like object from the bytes
    file_like = BytesIO(contents)

    # Create a PIL.Image object from the file-like object
    image = PILImage.open(file_like)

    return image


class CLIP(ImageClassification):
    model_name = "openai/clip-vit-large-patch14-336"

    def load_model(self):
        model_name = "openai/clip-vit-large-patch14-336"
        self.classifier = pipeline("zero-shot-image-classification", model=model_name)

    def predict(
        self,
        input: ImageClassification.Inputs,
    ) -> ImageClassification.Outputs:
        image_pil = uploadfile_to_pil(input.image)
        candidate_labels = (
            input.candidate_labels
        )  # [x.strip() for x in input.candidate_labels.split(",")]

        labels: List[LabelWithScore] = self.classifier(
            image_pil, candidate_labels=candidate_labels
        )

        return ImageClassification.Outputs(labels=labels)


class CLIP2(ImageClassification):
    model_name = "B"

    def load_model(self):
        model_name = "openai/clip-vit-large-patch14-336"
        self.classifier = pipeline("zero-shot-image-classification", model=model_name)

    def predict(
        self, image: Image, candidate_labels: List[Label], size: int
    ) -> List[LabelWithScore]:
        out = self.classifier(image, candidate_labels=candidate_labels)
        return []
