from fastapi.responses import HTMLResponse


def view(child: str) -> str:
    return f"""
    <html>
        <head>
            <title>Demo Polisher</title>
            <link
                rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
            />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
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


def response(child: str) -> HTMLResponse:
    return HTMLResponse(content=view(child))
