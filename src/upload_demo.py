import logging
from fastapi import File, UploadFile, APIRouter, Request
import requests
from starlette.datastructures import URL
from fastapi.responses import RedirectResponse
from src.kv.factory import KvFactory
from src.audio_source_separator.factory import AudioSourceSeparatorFactory
from src.object_storage.factory import ObjectStorageFactory
import src.document as document

router = APIRouter(prefix="/upload-demo")


@router.get("/")
async def get() -> str:
    return document.response(
        """
        <main class="container">
            <form method="post" enctype="multipart/form-data">
                <fieldset>
                    <label>
                        Audio Demo File
                        <input
                            name="audio_demo_file"
                            type="file"
                            placeholder="Audio Demo File"
                            autocomplete="audio_demo_file"
                            required
                        />
                    </label>
                </fieldset>
                <input
                    type="submit"
                    value="Submit"
                />
            </form>
        </main>
    """
    )


BASE_DIR = "files"


@router.post("/")
async def post(request: Request, audio_demo_file: UploadFile = File(...)):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing upload for file: {audio_demo_file.filename}")
    base_url = str(URL(scope=request.scope).replace(path="", query=""))
    logger.info(f"Base URL from request: {base_url}")

    storage = ObjectStorageFactory.create(
        impl="local",
        base_dir=f"{BASE_DIR}/demos",
        base_url=f"{base_url}",
        router=router,
        logger=logger,
    )
    logger.info(f"Created local storage with base directory: {BASE_DIR}/demos")

    kv = KvFactory.create(impl="dict")

    # upload_record_db = UploadRecordDbFactory.create()

    audio_source_separator = AudioSourceSeparatorFactory.create(
        impl="demucs", logger=logger
    )
    logger.info("Created Demucs audio source separator")

    file_content = await audio_demo_file.read()
    filename = audio_demo_file.filename
    object_name = f"demos/{filename}"
    logger.info(f"Read file content, filename: {filename}, object_name: {object_name}")

    storage.upload(object_name, file_content)
    logger.info(f"Uploaded file to storage: {object_name}")

    logger.info(f"Starting audio source separation for: {filename}")
    file_url = storage.get_url(object_name)

    logger.info(f"Downloading file from storage: {file_url}")

    # input_file = f"{BASE_DIR}/demos/{filename}"
    # download_file(file_url, input_file)

    # audio_source_separator.separate(
    #     input_file=input_file,
    #     output_dir=f"{BASE_DIR}/demos/separated",
    # )

    logger.info(f"Completed audio source separation for: {filename}")

    logger.info(f"Redirecting to result page")
    return RedirectResponse(url=f"{router.prefix}/result", status_code=303)


def download_file(file_url: str, filename: str):
    response = requests.get(file_url)
    with open(filename, "wb") as f:
        f.write(response.content)


@router.get("/result")
async def get_result():
    return document.response(
        """
        <main class="container">
            <h1>Result</h1>
        </main>
        """
    )
