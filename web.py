from flask import Flask, render_template, request
from ocr import init_model, read_image

import io
from PIL import Image
import time
import base64

app = Flask(__name__)
e_ocr, m_ocr = init_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',
    )

@app.route("/translate", methods=['GET','POST'])
def translate_image():
        buffered = io.BytesIO()
        # print(request.form['image'])
        imgdata = base64.b64decode(request.form["image"])
        # read_image(io.BytesIO(request.data), e_ocr, m_ocr)
        # img_bytes = request.data[request.data.index(',')+1:]
        # img_data = io.BytesIO(request.args["image"])
        # print(request.form["image"])
        # # print(type(img_data))
        img = Image.open(io.BytesIO(imgdata))
        # img.thumbnail((1000,1000), resample = Image.Resampling.LANCZOS)
        # print(img.size)
        # print("please wait")
        # img.show()
        img = read_image(img, e_ocr, m_ocr)
        # time.sleep(2)
        # print("translated")
        # img.show()
        img.save(buffered, format="PNG")
        # print(json.loads(request.data))

        return(base64.b64encode(buffered.getvalue()))

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug = True)