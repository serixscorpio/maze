# flake8: noqa
import tempfile
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "Red Dot": "<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='/>",
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/pic")
def read_pic():
    from maze import example_gen_png

    fp = tempfile.NamedTemporaryFile(suffix=".png")
    example_gen_png(fp)
    return FileResponse(fp.name, media_type="image/png")