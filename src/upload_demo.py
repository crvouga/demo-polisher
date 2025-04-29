import logging
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import RedirectResponse
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
async def post(audio_demo_file: UploadFile = File(...)):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing upload for file: {audio_demo_file.filename}")

    storage = ObjectStorageFactory.create(type="local", base_dir=f"{BASE_DIR}/demos")
    logger.info(f"Created local storage with base directory: {BASE_DIR}/demos")

    audio_source_separator = AudioSourceSeparatorFactory.create(
        type="demucs", logger=logger
    )
    logger.info("Created Demucs audio source separator")

    file_content = await audio_demo_file.read()
    filename = audio_demo_file.filename
    object_name = f"demos/{filename}"
    logger.info(f"Read file content, filename: {filename}, object_name: {object_name}")

    storage.upload(object_name, file_content)
    logger.info(f"Uploaded file to storage: {object_name}")

    logger.info(f"Starting audio source separation for: {filename}")
    audio_source_separator.separate(
        input_file=storage.get_url(object_name),
        output_dir=f"{BASE_DIR}/demos/separated",
    )
    logger.info(f"Completed audio source separation for: {filename}")

    logger.info(f"Redirecting to result page")
    return RedirectResponse(url=f"{router.prefix}/result", status_code=303)


@router.get("/result")
async def get_result():
    return document.response(
        """
        <main class="container">
            <h1>Result</h1>
        </main>
        """
    )
