from handRecog.app import app, db
from handRecog.models.classifications import Classification
import cv2, os, numpy
from sklearn.neighbors import KNeighborsClassifier
from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename

recog = Blueprint('recog', __name__)

def getHuMoments(image):
    # Reads the image
    image = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    # Turns the image into HSV to take the black and white file after
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(image)

    # Make an edge sharpening through laplacian filter
    filteredValue = cv2.Laplacian(value, cv2.CV_8U)
    highlightedValue = cv2.subtract(value, filteredValue)

    # Equalizes the histogram to improve details
    image = cv2.equalizeHist(highlightedValue)

    # Creates an structuring element
    structuringElement = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)
    )

    # Turns the image into binary
    method = cv2.THRESH_BINARY_INV
    ret, binarizedImg = cv2.threshold(image, 135, 255, method)

    # Opening and closing
    processedImg = cv2.morphologyEx(
        binarizedImg, cv2.MORPH_CLOSE, structuringElement
    )

    processedImg = cv2.morphologyEx(
        processedImg, cv2.MORPH_OPEN, structuringElement
    )

    # Get moments and hu moments
    moments = cv2.moments(binarizedImg)
    huMoments = cv2.HuMoments(moments)

    return -numpy.sign(huMoments) * numpy.log10(numpy.abs(huMoments))

@recog.route('/admin', methods=['POST', 'GET'])
def train():
    if request.method == 'GET':
        return render_template('train.html')

    image = request.files['img']
    result = request.form['result']
    if not image or not result:
        return 'You can\'t submit without data' 
    
    huMoments = getHuMoments(image)
    classification = Classification(
        huMoments[0][0], 
        huMoments[1][0],
        huMoments[2][0],
        huMoments[3][0],
        huMoments[4][0],
        huMoments[5][0],
        huMoments[6][0],
        result
    )

    db.session.add(classification)
    db.session.commit()

    return render_template('train.html')

@recog.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html', result='')

    image = request.files['img']
    if not image:
        return 'You can\'t submit without data'

    classifications = Classification.query.all()

    featuresList = []
    classificationsList = []

    for c in classifications:
        featuresList.append([
            c.m1, c.m2, c.m3, c.m4, c.m5, c.m6, c.m7
        ])

        classificationsList.append([
            c.result
        ])
    
    knn = KNeighborsClassifier(3)
    knn.fit(featuresList, classificationsList)

    huMoments = getHuMoments(image)

    huMomentsList = []

    for hu in huMoments:
        huMomentsList.append(hu[0])

    result = knn.predict([huMomentsList])

    str_result = ""
    if result == 1:
        str_result = 'aberta'
    else:
        str_result = 'fechada'

    return render_template('resultado.html', resultado = str_result)


@recog.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')