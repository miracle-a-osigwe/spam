import numpy as np
import joblib
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help="Add your text as a string")

stem = PorterStemmer() #text stemming
stopwordSet = set(stopwords.words('english')) #create a set of the stopwords


def preprocess(text):
    data = text
    for i in range(len(data)):
        message = data[i].lower() #using reqular expression to clean the text
        message = message.split() #split the words
        message = [stem.stem(word) for word in message if not word in stopwordSet]# stem each word not found in the stopword set
        data[i] = ' '.join(message) #join the data
    return data #return the data


# Prediction function
def predictions(text):
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    vectorized_text = vectorizer.transform(text)
    predict = model.predict(vectorized_text)
    pred_prob = model.predict_proba(vectorized_text)
    return [predict, pred_prob]

#@api.representation('application/json')
class PredictSpam(Resource):
    
    def get(self):
        #get the user query
        args = parser.parse_args()
        user_text = args['text']
        try:
            text = preprocess([user_text])
            prediction = predictions(text)
            result = prediction[0]
            probability = prediction[1]

            if result == 0:
                pred_text = "The text is Not a Spam"
                confidence = round(probability[0][0], 3)
            else:
                pred_text = "The text is a Spam"
                confidence = round(probability[0][1], 3)

            #create a json output
            output = {"prediction" : pred_text, "confidence level" : confidence}
        except Exception:
            output = {"KeyError" : "Wrong key, use text"}

        return jsonify(output)

#setup the api routing here
#route the url to the resource
api.add_resource(PredictSpam, '/')


if __name__ == "__main__":
    app.run(debug=True)