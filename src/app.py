from flask import Flask, request, jsonify
import json
import uuid
from lib import similar_ranking, dragon
import pathlib

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    with open("../data.json") as f:
        wv_pres = json.load(f)
    with open("../prefectures.json") as f:
        prefectures = json.load(f)
    
    file = request.files['file']
    id=str(uuid.uuid4())
    input_path=f"./static/input_{id}.png"
    file.save(input_path)
    
    res = similar_ranking(input_path, wv_pres)
    output_pref = prefectures[res[0][1]]
    output_score = int(100 - res[0][0] / 90 * 100)

    input_image_path = "../dragon.png"
    output_image_path = f"./static/output_{id}.png"
    font_path = "../NotoSansJP-Medium.ttf"

    dragon(input_image_path,output_image_path,font_path,output_pref,output_score)
    open(output_image_path).write(output_pref)
    return jsonify({"id":id})


@app.route('/health-check',methods=['GET'])
def health_check():
    return jsonify({"message":"Hello World!"})

if __name__ == '__main__':
    app.run()