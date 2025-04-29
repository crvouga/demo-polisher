from fastapi import File, UploadFile, APIRouter
import src.document as document

router = APIRouter(prefix="/upload-demo")


def html() -> str:
    return """
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


@router.get("/")
async def get() -> str:
    return document.response(html())


@router.post("/")
async def post(audio_demo_file: UploadFile = File(...)):
    return {"filename": audio_demo_file.filename}
