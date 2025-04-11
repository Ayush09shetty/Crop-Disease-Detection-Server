# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from PIL import Image
# import numpy as np
# import tensorflow as tf
# import os

# # Load model once globally
# MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/version1_94_82.h5')
# MODEL = tf.keras.models.load_model(MODEL_PATH)
# CLASS_NAMES = [
#     'Potato Early Blight', 'Potato Healthy', 'Potato Late Blight',
#     'Tomato Bacterial Spot', 'Tomato Early Blight', 'Tomato Healthy',
#     'Tomato Late Blight', 'Tomato Septoria Spot'
# ]

# @api_view(["GET"])
# def ping(request):
#     return Response("Hello, I'm alive", status=status.HTTP_200_OK)

# @api_view(["POST"])
# def predict(request):
#     if 'file' not in request.FILES:
#         return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

#     file = request.FILES['file']

#     try:
#         image = Image.open(file).convert("RGB")
#         image = image.resize((256, 256))
#         image = np.array(image) / 255.0
#         img_batch = np.expand_dims(image, axis=0)

#         prediction = MODEL.predict(img_batch)
#         predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
#         confidence = float(np.max(prediction[0]) * 100)

#         return Response({
#             "prediction": predicted_class,
#             "confidence": confidence
#         })

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import tensorflow as tf
import os

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'version1_94_82.h5')
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ['Potato Early Blight', 'Potato Healthy', 'Potato Late Blight', 'Tomato Bacterial Spot', 'Tomato Early Blight', 'Tomato Healthy', 'Tomato Late Blight', 'Tomato Septoria Spot']

@csrf_exempt
def ping(request):
    return JsonResponse({"message": "Hello, I'm alive"})

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
        predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
        confidence = float(np.max(prediction[0]) * 100)

        return JsonResponse({"prediction": predicted_class, "confidence": confidence})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
