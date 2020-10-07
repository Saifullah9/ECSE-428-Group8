import React, { useState, useRef, useCallback, useEffect } from 'react';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/lib/ReactCrop.scss';
import Button from '@material-ui/core/Button';

const pixelRatio = window.devicePixelRatio || 1;


function getResizedCanvas(canvas, newWidth, newHeight) {
    const tmpCanvas = document.createElement("canvas");
    tmpCanvas.width = newWidth;
    tmpCanvas.height = newHeight;

    const ctx = tmpCanvas.getContext("2d");
    ctx.drawImage(
        canvas,
        0,
        0,
        canvas.width,
        canvas.height,
        0,
        0,
        newWidth,
        newHeight
    );

    return tmpCanvas;
}

function generateUpload(previewCanvas, crop) {
    if (!crop || !previewCanvas) {
        return;
    }

    const canvas = getResizedCanvas(previewCanvas, crop.width, crop.height);

    return new Promise((resolve, reject) => {
        canvas.toBlob(blob => {
            blob.name = 'test.jpg';
            resolve(blob);
        }, 'image/jpeg', 1);
    });
}

function ImageUpload() {

    const [upImg, setUpImg] = useState();
    const imgRef = useRef(null);
    const [crop, setCrop] = useState({ unit: "%", width: 30 });
    const previewCanvasRef = useRef(null);
    const [completedCrop, setCompletedCrop] = useState(null);

    const onLoad = useCallback((img) => {
        imgRef.current = img;
    }, []);

    useEffect(() => {
        if (!completedCrop || !previewCanvasRef.current || !imgRef.current) {
            return;
        }

        const image = imgRef.current;
        const canvas = previewCanvasRef.current;
        const crop = completedCrop;

        const scaleX = image.naturalWidth / image.width;
        const scaleY = image.naturalHeight / image.height;
        const ctx = canvas.getContext("2d");

        canvas.width = crop.width * pixelRatio;
        canvas.height = crop.height * pixelRatio;

        ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        ctx.imageSmoothingQuality = "high";

        ctx.drawImage(
            image,
            crop.x * scaleX,
            crop.y * scaleY,
            crop.width * scaleX,
            crop.height * scaleY,
            0,
            0,
            crop.width,
            crop.height
        );
    }, [completedCrop]);

    return (
        <div>
            <FilePond
                instantUpload={false}
                onaddfile={
                    async (error, file) => {
                        const reader = new FileReader();
                        reader.addEventListener("load", () => {
                            setUpImg(reader.result)
                            console.log(reader.result)

                        });
                        reader.readAsDataURL(file.file);
                    }
                }
                onremovefile={
                    (error, file) => {
                        setUpImg(null);
                        setCompletedCrop(null);
                        const context = previewCanvasRef.current.getContext('2d');
                        context.clearRect(0, 0, previewCanvasRef.current.width, previewCanvasRef.current.height);
                    }
                }
                name="file"
            />
            <ReactCrop
                src={upImg}
                onImageLoaded={onLoad}
                crop={crop}
                onChange={(c) => setCrop(c)}
                onComplete={(c) => setCompletedCrop(c)}
            />
            <div>
                <canvas
                    ref={previewCanvasRef}
                    // Rounding is important so the canvas width and height matches/is a multiple for sharpness.
                    style={{
                        width: Math.round(completedCrop?.width ?? 0),
                        height: Math.round(completedCrop?.height ?? 0)
                    }}
                />
            </div>
            <Button
                type="button"
                variant="contained"
                color="primary"
                disabled={!completedCrop?.width || !completedCrop?.height}
                onClick={() => {
                    generateUpload(previewCanvasRef.current, completedCrop).then((value) => {
                        var formData = new FormData();
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "http://localhost:8000/upload")
                        formData.append("file", value);
                        xhr.send(formData);
                    });
                }
                }
            >
                Upload cropped image
      </Button>
        </div>
    );
}

export default ImageUpload;