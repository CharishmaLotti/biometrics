from flask import Flask, render_template, redirect, url_for, request, flash
import cv2
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key SESSION MANAGEMENT

# Define the personalizations dictionary at the top level
personalizations_data = {}

@app.route('/')
def start_auth():
    return render_template('start_auth.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Open the camera for 5 seconds
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return redirect(url_for('start_auth'))

    start_time = time.time()
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Automatically authenticate as "Charishma"
    authenticated_user = "Charishma"
    return redirect(url_for('personalization', user=authenticated_user))

@app.route('/personalization')
def personalization():
    user = request.args.get('user', 'Guest')
    # Use the personalizations_data dictionary
    user_personalizations = personalizations_data.get(user, {})
    return render_template('personalization.html', user=user, personalizations=user_personalizations)

@app.route('/update_personalization', methods=['POST'])
def update_personalization():
    user = request.form.get('user', 'Guest')
    lighting = request.form.get('lighting', 'default')
    music = request.form.get('music', 'default')
    
    # Update the user's personalizations
    personalizations_data[user] = {
        'lighting': lighting,
        'music': music,
    }
    
    flash('Personalization updated successfully!')
    return redirect(url_for('personalization', user=user))

if __name__ == '__main__':
    app.run(debug=True)
