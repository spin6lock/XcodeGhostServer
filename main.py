#encoding:utf8
from flask import Flask, request
import time
from struct import pack, unpack
from Crypto.Cipher import DES
from binascii import b2a_hex
import logging
logging.basicConfig(filename="xcode_ghost.log",
                level=logging.DEBUG)

app = Flask(__name__)
key = "stringWithFormat"

def decode(rawstr):
    package_len, command_len, version = unpack("!IHH", rawstr[:8])
    desstr = rawstr[8:]
    obj = DES.new(key[:8])
    plaintext = obj.decrypt(desstr)
    padding_char = plaintext[-1]
    decode_json = json.loads(plaintext[:-ord(padding_char)])
    return package_len, command_len, version, decode_json

def pop_warning(appname):
    ret = u'{ \
        "alertHeader":"Warning", \
        "alertBody":"你好，你手机上的%s感染了XcodeGhost，请更新，详情联系SA", \
        "appID":"0", \
        "cancelTitle":"确定", \
        "confirmTitle":"取消", \
        "scheme":"mqqopensdkapiV2://qzapp"}' %appname
    return ret

@app.route("/", methods=["POST"])
def index():
    raw = request.get_data()
    logging.debug("receive:%s", b2a_hex(raw))
    try:
        print decode(raw)
        _,_,_, info = decode(raw)
        appname = info["app"]
        return pop_warning(appname) 
    except Exception, err:
        pass
    return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
