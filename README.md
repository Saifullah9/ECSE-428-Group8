# ECSE-428-Group8
This is a repository for group 8 from the course ECSE 428 which will hold their project of SupplyHero 

# How to Install Backend (SupplyHero_FastApi)
Make sure you have installed Tesseract OCR (**Don't forget to add to PATH variable!**)
https://tesseract-ocr.github.io/tessdoc/Downloads

Here's a link to Windows installers if you have Windows: https://github.com/UB-Mannheim/tesseract/wiki
If you have MacOS -> Download Tesseract OCR using Homebrew: https://brew.sh/

Next cd into SupplyHero_FastApi:
``` pip install -r requirements.txt ```

Run the server from inside SupplyHero_FastApi
``` uvicorn api.main:app --reload ```

And you're done for backend installation

# How to Install Frontend (SupplyHero_React)

Make sure you have Node.js https://nodejs.org/en/download/

From the root SupplyHero_React folder, cd into frontend-app and enter the following:

``` npm install ```

You can run the frontend on your local development using the following:

``` npm start ```



