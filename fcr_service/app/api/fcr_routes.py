from fastapi import APIRouter, Body, Form, HTTPException, File, UploadFile
from PIL import Image
from typing import List
from ..service.fcr_service import generate_embeddings, verify_face
import io

router = APIRouter()

@router.post("/generate-embeddings")
async def generate_face_embeddings(images: List[UploadFile] = File(...)):
    print(f"Received {len(images)} images.")
    if len(images) != 4:
        raise HTTPException(status_code=400, detail="Exactly 4 images are required.")

    pil_images = []
    for file in images:
        try:
            contents = await file.read()
            img = Image.open(io.BytesIO(contents)).convert("RGB")
            pil_images.append(img)
        except Exception as e:
            print(f"Image conversion error: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid image: {file.filename}")

    try:
        mean_embedding = generate_embeddings(pil_images)
        print("Embedding successfully generated.")
        return {"embedding": mean_embedding}
    except Exception as e:
        import traceback
        print("Exception during embedding generation:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/verify-face")
async def verify_face_endpoint(
    image: UploadFile = File(...),
    stored_embedding: List[float] = Form(...)
):
    
    try:
        result = await verify_face(image, stored_embedding)
        return {"match": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

  
