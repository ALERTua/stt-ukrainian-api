import logging
import os
import tempfile
import time

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response

from dotenv import load_dotenv
from gradio_client import Client, handle_file

load_dotenv()


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("app")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
GRADIO_URL = os.getenv("GRADIO_URL", "http://gradio:7860")
UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))
UVICORN_HOST = os.getenv("UVICORN_HOST", "0.0.0.0")

gr_client = None
while gr_client is None:
    try:
        gr_client = Client(GRADIO_URL)
    except Exception:
        LOG.exception("Failed to connect to gradio. Retrying in 10 seconds")
        time.sleep(10)


@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    response_format: str = Form("json"),
):
    LOG.info(f"Transcribing file: {file.filename}, {response_format=}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        result = gr_client.predict(
            audio_path=handle_file(temp_path),
            api_name="/inference",
        )
        LOG.info(f"Transcription result: {result}")
        try:
            result = result.split('\n')[4].lstrip('> ')
            LOG.info(f"Clean transcription result: {result}")
        except:
            pass

        if response_format == "text":
            return Response(content=result, media_type="text/plain")
        return JSONResponse(content={"text": result})

    except Exception:
        LOG.exception("Error transcribing audio")
        return Response(content="Transcription failed", status_code=500)
    finally:
        os.remove(temp_path)


@app.get("/health")
def get_health():
    return {"status": "OK"}


@app.get("/")
def root():
    return RedirectResponse(url=GRADIO_URL)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT, log_level="debug")
