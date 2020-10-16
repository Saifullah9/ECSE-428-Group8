from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
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


class User(models.BaseUser):
    password: str


@app.post("/login")
async def login(user: User):
    print(user.email)


@app.post("/upload")
async def create_uploaded_file(file: UploadFile = File(...)):
    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        supply_str = pytesseract.image_to_string(
            Image.open(file.file)).splitlines()
    elif file.content_type == 'application/pdf':  # Will need Poppler
        image_obj = convert_from_bytes(file.file.read())
        if len(image_obj) > 1:
            return {'error': 'PDF contains more than 1 page.'}
        supply_str = pytesseract.image_to_string(image_obj[0]).splitlines()
    else:
        return {'error': 'File is not an image.'}
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