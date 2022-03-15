from sanic import Sanic
from sanic.response import text, file, raw, json
from io import BytesIO, FileIO
from uuid import uuid4
from hashlib import sha1, sha224, sha256

import asyncio
import qrcode
import random

app = Sanic("EnigmaDemo")

@app.get("/")
async def index(request):
    return await file('index.html')

@app.get("/gen")
async def gen(request):
    data = request.args.get('data', random.randint(10**16, 10**17))
    # to_encode = f"[ENCRYPTED][{data}]"
    to_encode = f"[ENCRYPTED][{sha1(str(data).encode()).hexdigest()}]"
    buf = BytesIO()
    filename = f'generated/{uuid4()}.png'

    qr = await asyncio.get_event_loop().run_in_executor(None, qrcode.make, to_encode)
    qr.save(filename)
    # image = qr.get_image()
    # bytess = image.tobytes()
    # bytess = BytesIO(image.tobytes())

    # return raw(bytess, content_type='image/jpeg')
    # return await file(filename)
    return json({"path": filename})


app.static("/generated", "generated")
app.static("/styles", "styles.css")
