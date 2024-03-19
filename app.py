from flask import Flask, render_template, request
from image_enhancement import enhance_image
from white_background import remove_background

app = Flask(__name__)

# Route for the landing page
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')

    if file:
        try:
            # Read the uploaded file as bytes
            file_bytes = file.read()

            # Enhance the uploaded image and get the enhanced image path
            enhanced_image_path = enhance_image(file_bytes)

            # Remove background and get the final image path
            final_image_path = remove_background(enhanced_image_path)

            if final_image_path:
                return render_template('index.html', final_image_path=final_image_path)
            else:
                return render_template('index.html', error='Failed to process the image')
        except Exception as e:
            return render_template('index.html', error='An error occurred while processing the image')

if __name__ == '__main__':
    app.run(debug=True)
