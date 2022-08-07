import base64
import os

from app.main.config import UPLOAD_FOLDER


def base64ToPngOrJpgConverter(img_data, img_id, test_id):
    arr = img_data.split(';')
    data = arr[0]
    print("=======================")
    print("data", data)
    print("=======================")

    base64_bytes = arr[1]
    data_type = data.split(':')[1]
    print('data_type', data_type)
    base64_bytes_data = base64_bytes.split(',')[1]
    if data_type == 'image/png':
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = f"test_sample_{img_id}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename).replace('\\\\', '/')
        with open(filepath, "wb") as fh:
            fh.write(base64.b64decode(base64_bytes_data))
    elif data_type == 'image/jpg' or data_type == 'image/jpeg':
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = f"test_sample_{img_id}_{test_id}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as fh:
            fh.write(base64.b64decode(base64_bytes_data))
    else:
        filepath = None
    return filepath, filename
