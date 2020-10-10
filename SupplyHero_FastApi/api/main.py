from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def create_uploaded_file(file: UploadFile = File(...)):
    supply_str = pytesseract.image_to_string(Image.open(file.file)).splitlines()
    supply_str = [elem for elem in supply_str if elem]
    print(supply_str)
    return {"filename": file.filename,
            "list": supply_str}

@app.get("/")
async def main():
    content = """
<body>
<form action="/upload" enctype="multipart/form-data" method="post">
<input name="file" type="file" required>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)