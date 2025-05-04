from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

app = FastAPI()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

@app.post("/predict/")
async def predict(file: UploadFile = File(...), rostro: str = Query(...)):
    try:
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        image_np = np.array(image)
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]

            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=30, minSize=(25,25))
            if len(smiles) > 0:
                return {"prediction": "sonrisa detectada"}

        return {"prediction": "no se detectó sonrisa"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))