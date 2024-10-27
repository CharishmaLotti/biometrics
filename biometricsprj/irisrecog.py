import cv2
import numpy as np
import mysql.connector

# Establish connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="yourpassword",  # Replace with your MySQL password
    database="smart_home"
)

cursor = db.cursor()

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Placeholder for authenticated user's ID
authenticated_user_id = None

# Function to check if the iris data matches
def check_iris_in_database(iris_data):
    query = "SELECT id, name, authorized FROM users WHERE iris_data = %s"
    cursor.execute(query, (iris_data,))
    result = cursor.fetchone()
    if result:
        return result  # (id, name, authorized)
    return None

# Function to show personalization options
def show_personalizations(user_id):
    query = "SELECT lighting_level, music_type, fan_level, tv_mode FROM personalizations WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    
    if result:
        print(f"Personalization for User ID {user_id}:")
        print(f"Lighting Level: {result[0]}")
        print(f"Music Type: {result[1]}")
        print(f"Fan Level: {result[2]}")
        print(f"TV Mode: {result[3]}")
    else:
        print("No personalizations found for this user.")

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes in the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            eye_region = roi_gray[ey:ey+eh, ex:ex+ew]

            # Simulate iris data as a simple string (in practice, use actual iris recognition)
            iris_data = str(eye_region.sum())

            # Check if this iris data matches any user in the database
            user = check_iris_in_database(iris_data)

            if user:
                user_id, name, authorized = user
                if authorized:
                    print(f"User {name} authenticated. ID: {user_id}")
                    authenticated_user_id = user_id
                    # Ask for personalization
                    apply_pers = input("Apply personalizations? (yes/no): ").strip().lower()
                    if apply_pers == "yes":
                        show_personalizations(user_id)
                else:
                    print("User not authorized")
            else:
                print("User not found or unauthorized")

    # Display the video with face/eye rectangles
    cv2.imshow('Iris Recognition', frame)

    # Break the loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Close the database connection
db.close()
