from fastapi import File, UploadFile, APIRouter
from fastapi.responses import RedirectResponse
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

    storage = ObjectStorageFactory.create("local", base_dir=f"{BASE_DIR}/demos")

    file_content = await audio_demo_file.read()
    filename = audio_demo_file.filename
    object_name = f"demos/{filename}"

    storage.upload(object_name, file_content)

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
