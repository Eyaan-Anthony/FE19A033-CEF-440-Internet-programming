from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import torch
import numpy as np
from typing import List
import io

# Initialize models once at the top-level (better than inside the function)
mtcnn = MTCNN(image_size=160, margin=14)
resnet = InceptionResnetV1(pretrained='vggface2').eval()



def generate_embeddings(images: List[Image.Image]) -> List[float]:
    """
    Takes a list of 4 PIL images and returns a robust embedding (as a list of floats).
    Aggregates embeddings across all valid face detections.
    """

    embeddings = []

    for img in images:
        try:
            # Detect and crop the face
            img_cropped = mtcnn(img)

            if img_cropped is None:
                print("Warning: Face not detected in one of the images.")
                continue

            # Add batch dimension, send to model, detach from graph
            with torch.no_grad():
                embedding = resnet(img_cropped.unsqueeze(0)).squeeze()  # [512]
                embeddings.append(embedding)

        except Exception as e:
            print(f"Error processing image: {e}")
            continue

    if not embeddings:
        raise ValueError("No valid face embeddings could be extracted.")

    # Average the embeddings into a single vector
    stacked = torch.stack(embeddings)
    mean_embedding = torch.mean(stacked, dim=0)

    return mean_embedding.tolist()  # returns List[float]

async def verify_face(image_file, stored_embedding: list, threshold=0.85):
    contents = await image_file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    face = mtcnn(image)
    if face is None:
        raise ValueError("No face detected")

    img_embedding = resnet(face.unsqueeze(0))
    stored_tensor = torch.tensor(stored_embedding).unsqueeze(0)

    similarity = torch.nn.functional.cosine_similarity(img_embedding, stored_tensor).item()
    return similarity > threshold
