# In the Flask application (app.py)

from flask import Flask, render_template, request, redirect, url_for
from image_enhancement import enhance_image
from white_background import remove_background
import os

app = Flask(__name__)

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('upload'))
    return render_template('index.html')

# Route for the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error='No file uploaded')

        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error='No file selected')

        if file:
            try:
                # Read the uploaded file as bytes
                file_bytes = file.read()

                # Enhance the uploaded image and get the enhanced image path
                enhanced_image_path = enhance_image(file_bytes)

                # Remove background and get the final image path
                final_image_path = remove_background(enhanced_image_path)

                if final_image_path:
                    # Pass only the filename to the template
                    final_image_filename = os.path.basename(final_image_path)
                    return render_template('upload.html', final_image_filename=final_image_filename)
                else:
                    return render_template('upload.html', error='Failed to process the image')
            except Exception as e:
                return render_template('upload.html', error='An error occurred while processing the image')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
