import cv2
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwerty",
    database="smart_home"
)
cursor = db.cursor()

# Function to capture and store iris data for a user
def capture_iris(username):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Iris Capture - Press s to Save, q to Quit', frame)

        # Press 's' to save the iris image
        if cv2.waitKey(1) & 0xFF == ord('s'):
            iris_image_path = f'static/iris_images/{username}_iris.jpg'
            cv2.imwrite(iris_image_path, gray_frame)  # Save the image
            print(f"Iris image saved at {iris_image_path}")

            # Insert data into the database
            
            insert_query = "INSERT INTO iris_data (username, iris_image_path) VALUES (%s, %s)"

            cursor.execute(insert_query, (username, iris_image_path))
            db.commit()
            break

        # Press 'q' to quit
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Capture iris data for two users
capture_iris("Charishma")
capture_iris("Thanusri")
