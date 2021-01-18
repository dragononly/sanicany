from cnocr import CnOcr
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from cnstd import CnStd
import requests
import urllib.request
import os
import sys
app = Sanic("App Name")
CORS(app)
cn_ocr = CnOcr()
std = CnStd()


@app.route("/ocr")
def test(request):
    myreq = request.get_args(keep_blank_values=True)
    imgsrc = myreq["imgsrc"][0]
    name = myreq["name"][0]
    urllib.request.urlretrieve(imgsrc, filename=name)
    box_info_list = std.detect(name)
    arr = []
    for box_info in box_info_list:
        cropped_img = box_info['cropped_img']  # 检测出的文本框
        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        arr.append(ocr_res)
    #res = ocr.ocr(name)
    os.remove(name)
    return json({"hello": arr})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, auto_reload=True)
