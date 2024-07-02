from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps(json.load(open("./prefectures.json")))

if __name__ == '__main__':
    app.run()