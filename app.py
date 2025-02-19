from flask import Flask, request, jsonify, Response, render_template
from flask_restful import Api, Resource
from models import YOLOModel, FaceDetectionModel, LabelReadingModel
import io
from PIL import Image
from flask_cors import CORS
import cv2


app = Flask(__name__)
api = Api(app)
CORS(app)

# Home page route to serve index.html
@app.route("/")
def home():
    return render_template("index.html")

# RESTful API class for applying models
class ModelClass(Resource):
    def post(self, modelName):
        """
        RESTful endpoint to apply a model to an uploaded image (without saving).
        """
        try:
            if "file" not in request.files:
                return {"error": "No file uploaded"}, 400

            file = request.files["file"]

            if file.filename == "":
                return {"error": "No selected file"}, 400

            # Load the image in memory
            image = Image.open(file.stream)
            
            print(type(image), ".............................imagetype.flask..................")
            

            # Model processing
            if modelName == "YOLO":
                result_image = YOLOModel().process_image(image)
            elif modelName == "FaceDetection":
                result_image = FaceDetectionModel().process_image(image)
            elif modelName == "LabelReading":
                result_image = LabelReadingModel().process_image(image)
            else:
                return {"error": "Invalid model selected."}, 400


            _, buffer = cv2.imencode('.jpg', result_image)
            print(type(buffer), "*******************buffer")
            # return Response(img_io, mimetype="image/jpeg")
            return Response(buffer.tobytes(), content_type='image/jpeg')


        except Exception as e:
            return {"error": str(e)}, 500

# Adding the RESTful resource to the API
api.add_resource(ModelClass, "/ModelClass/<modelName>/")

if __name__ == "__main__":
    app.run(debug=True)
