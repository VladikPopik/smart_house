import os
import cv2
import face_recognition
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_known_faces(known_faces_dir):
    """Load known faces and their encodings from the given directory."""
    known_faces = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_faces.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])

    return known_faces, known_names

def process_image(image, known_faces, known_names, detected_dir):
    """Process the input image, detect faces, and save the results."""
    # Convert image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        color = (0, 0, 255)  # Default color for unknown faces

        # If a match is found, use the name from the known faces
        if matches:
            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                color = (0, 255, 0)  # Green for recognized faces

        # Draw a rectangle around the face and label it
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Save the processed image to the detected directory
    if not os.path.exists(detected_dir):
        os.makedirs(detected_dir)

    output_path = os.path.join(detected_dir, "processed_image.jpg")
    cv2.imwrite(output_path, image)

    return output_path

@app.route('/process-image', methods=['GET', 'POST'])
def upload_image():
    """Endpoint to receive and process an uploaded image."""
    try:
        if request.method == 'POST':
            if 'image' not in request.files:
                return jsonify({"error": "No image file provided."}), 400

            file = request.files['image']

            if file.filename == '':
                return jsonify({"error": "No selected file."}), 400

            # Read the image file
            np_img = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        else:  # Handle GET request
            # Load an image from the unknown_faces folder
            unknown_faces_dir = './unknown_faces'
            unknown_files = [f for f in os.listdir(unknown_faces_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            if not unknown_files:
                return jsonify({"error": "No images found in the unknown_faces directory."}), 404

            # Use the first image from the unknown_faces directory
            image_path = os.path.join(unknown_faces_dir, unknown_files[0])
            image = cv2.imread(image_path)

        # Load known faces and names
        known_faces_dir = "./known_faces"
        detected_dir = "./detected"
        known_faces, known_names = load_known_faces(known_faces_dir)

        # Process the image
        output_path = process_image(image, known_faces, known_names, detected_dir)

        return jsonify({"message": "Image processed successfully.", "output_path": output_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)