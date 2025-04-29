from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


def view_root(child: str):
    return f"""
    <html>
        <head>
            <title>Demo Polisher</title>
            <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
            />
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <header class="container">
                <nav>

                    <ul>
                        <li><a href="/">Demo Polisher</a></li>
                    </ul>
                </nav>
            </header>
            {child}
        </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
async def root():
    return view_root(
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


@app.post("/")
async def root_post(audio_demo_file: UploadFile = File(...)):
    return {"filename": audio_demo_file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
