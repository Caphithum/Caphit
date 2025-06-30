from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(100))
    image_data = db.Column(db.LargeBinary)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        image_data = io.BytesIO()
        image.save(image_data, format='JPEG')
        image_data = image_data.getvalue()

        new_image = ImageModel(image_name=file.filename, image_data=image_data)
        db.session.add(new_image)
        db.session.commit()
        return 'Image uploaded and saved to database', 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
