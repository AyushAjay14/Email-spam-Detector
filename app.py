from flask import Flask, render_template, request
import pickle
import string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from stopwords import words
import os

os.system('python -m nltk.downloader punkt')
ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in words and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    text = ""
    ans = ""
    if request.method == 'POST':
        text = request.form.get('email-content')
        # 1. preprocess
        transformed_sms = transform_text(text)
        # 2. vectorize
        vector_input = tfidf.transform([transformed_sms]).toarray()
        # 3. predict
        result = model.predict(vector_input)
        # 4. Display
        if result == 1:
            ans = "SPAM"
        else:
            ans = "NOT SPAM"
    return render_template('index.html', ans=ans)


if __name__ == "__main__":
    app.run()
