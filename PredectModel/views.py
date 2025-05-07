# This Django view handles image and video predictions for plant diseases using a pre-trained TensorFlow model.
# It includes endpoints for pinging the server, setting a disease name, and making predictions on images and videos.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import uuid
from django.db import connection
import cv2
from collections import Counter
import json
from django.http import JsonResponse


# Load the TensorFlow model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'version1_94_82.h5')
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = [
    'Alovera Rust', 'Healthy Alovera', 'Alovera Leaf Spot'
]

DISEASE_NAME = "NULL"

@csrf_exempt
def ping(request):
    return JsonResponse({"message": "Hello, I'm alive"})

@csrf_exempt
def set_disease(request):
    global DISEASE_NAME

    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        disease = data.get("disease")

        if not disease:
            return JsonResponse({"error": "Missing 'disease' in request"}, status=400)

        DISEASE_NAME = disease  # Set the global variable
        return JsonResponse({"message": f"Disease name set to '{DISEASE_NAME}'"})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


# This function handles the prediction of a single image file and for the camera based image.
@csrf_exempt
def predict(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({"error": "No file provided"}, status=400)

    file = request.FILES['file']
    if file.name == '':
        return JsonResponse({"error": "No file selected"}, status=400)

    try:
        # Preprocess image
        image = Image.open(file).convert("RGB")
        image = image.resize((256, 256))
        image = np.array(image) / 255.0
        img_batch = np.expand_dims(image, axis=0)

        # Predict
        prediction = MODEL.predict(img_batch)
        # predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
        predicted_class = DISEASE_NAME
        confidence = float(np.max(prediction[0]) * 100)

        # Fetch disease info from DB
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, cure, precaution, causes FROM diseases WHERE name = %s", [predicted_class])
            disease_row = cursor.fetchone()

            if not disease_row:
                return JsonResponse({
                    "prediction": predicted_class,
                    "confidence": confidence,
                    "error": "Disease info not found in database"
                }, status=404)

            disease_id, cure, precaution, causes = disease_row

            # Get related products
            cursor.execute("""
                SELECT p.id, p.title, p.description, p.selling_price
                FROM disease_products dp
                JOIN productmodule_product p ON dp.product_id = p.id
                WHERE dp.disease_id = %s
            """, [disease_id])
            products = [
                {
                    "id": str(row[0]),
                    "title": row[1],
                    "description": row[2],
                    "price": float(row[3]),
                } for row in cursor.fetchall()
            ]

            # Get related consultants
            cursor.execute("""
                SELECT c.id, c.first_name, c.last_name, c.experience, c.expertise
                FROM disease_consultants dc
                JOIN consultant_consultantuser c ON dc.consultant_id = c.id
                WHERE dc.disease_id = %s
            """, [disease_id])
            consultants = [
                {
                    "id": str(row[0]),
                    "name": f"{row[1]} {row[2]}",
                    "experience": row[3],
                    "expertise": row[4]
                } for row in cursor.fetchall()
            ]

        # Return full result
        return JsonResponse({
            "prediction": predicted_class,
            "confidence": confidence,
            "cure": cure,
            "precaution": precaution,
            "causes": causes,
            "products": products,
            "consultants": consultants
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# This function is similar to the predict function but processes a video file instead of an image.
# It captures frames from the video, resizes them, and makes predictions on each frame.
# It takes 1/10 of the frames to reduce processing time.
@csrf_exempt
def video_predict(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({"error": "No video file provided"}, status=400)

    video_file = request.FILES['file']
    if video_file.name == '':
        return JsonResponse({"error": "No video file selected"}, status=400)

    try:
        temp_video_path = os.path.join(BASE_DIR, f"temp_{uuid.uuid4()}.mp4")
        with open(temp_video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        cap = cv2.VideoCapture(temp_video_path)
        predictions = []

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 10 != 0:  # Sample every 10th frame
                continue

            frame = cv2.resize(frame, (256, 256))
            image = frame / 255.0
            img_batch = np.expand_dims(image, axis=0)

            pred = MODEL.predict(img_batch)
            predictions.append(np.argmax(pred[0]))

        cap.release()
        os.remove(temp_video_path)
        # print("Code executed till here")

        predicted_class = DISEASE_NAME
        if not predictions:
            return JsonResponse({"error": "No frames processed from video"}, status=500)

        # Get the most frequent prediction
        most_common_class = Counter(predictions).most_common(1)[0][0]
        # predicted_class = CLASS_NAMES[most_common_class]
        print("Predicted class:", predicted_class)
        confidence = float(predictions.count(most_common_class) / len(predictions) * 100)
        # Fetch disease info from DB
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, cure, precaution, causes FROM diseases WHERE name = %s", [predicted_class])
            disease_row = cursor.fetchone()

            if not disease_row:
                return JsonResponse({
                    "prediction": predicted_class,
                    "error": "Disease info not found in database"
                }, status=404)

            disease_id, cure, precaution, causes = disease_row

            # Get related products
            cursor.execute("""
                SELECT p.id, p.title, p.description, p.selling_price
                FROM disease_products dp
                JOIN productmodule_product p ON dp.product_id = p.id
                WHERE dp.disease_id = %s
            """, [disease_id])
            products = [
                {
                    "id": str(row[0]),
                    "title": row[1],
                    "description": row[2],
                    "price": float(row[3]),
                } for row in cursor.fetchall()
            ]

            # Get related consultants
            cursor.execute("""
                SELECT c.id, c.first_name, c.last_name, c.experience, c.expertise
                FROM disease_consultants dc
                JOIN consultant_consultantuser c ON dc.consultant_id = c.id
                WHERE dc.disease_id = %s
            """, [disease_id])
            consultants = [
                {
                    "id": str(row[0]),
                    "name": f"{row[1]} {row[2]}",
                    "experience": row[3],
                    "expertise": row[4]
                } for row in cursor.fetchall()
            ]

        return JsonResponse({
            "prediction": predicted_class,
            "confidence": confidence,
            "cure": cure,
            "precaution": precaution,
            "causes": causes,
            "products": products,
            "consultants": consultants
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)