import requests
import io
import shutil
import base64
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder


class AurastampImage(object):
    def __init__(self, server_url):
        default_server_url = 'https://api.aurastamp.com'
        if not server_url:
            server_url = default_server_url
        
        self.server_url = server_url

    def encode(self,
               image,
               message,
               hidden_image=None,
               model='the',
               return_type='base64',
               headers={}):
        
        field_data = {}
        field_data['file'] = ("filename", image)
        field_data['model_name'] = model
        field_data['message'] = message
        field_data['return_type'] = return_type
        if hidden_image:
            field_data['media'] = hidden_image

        m = MultipartEncoder(fields=field_data)
        r = requests.post(
            self.server_url+"/encode",
            data=m,
            headers={"Content-Type": m.content_type, **headers}
        )

        return r    

    def encode_local_file(self,
                          image_file_path,
                          message,
                          hidden_image_file_path=None,
                          output_path=None,
                          model='the',
                          return_type='base64',
                          headers={}):
                    
        field_data = {}
        image = Image.open(image_file_path)
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, image.format.lower())

        # image
        field_data['file'] = (image.filename, image_bytes_io)
        field_data['model_name'] = model
        field_data['message'] = message
        field_data['return_type'] = return_type
        if hidden_image_file_path:
            hidden_image = Image.open(hidden_image_file_path)
            field_data['media'] = hidden_image

        m = MultipartEncoder(fields=field_data)
        r = requests.post(
            self.server_url+"/encode",
            data=m,
            headers={"Content-Type": m.content_type,
                     **headers}
        )

        if output_path:
              with open(output_path, 'wb') as f:
                container = base64.b64decode(r.content)
                container_image = io.BytesIO(container)
                shutil.copyfileobj(container_image, f)         

        return r


    def decode(self,
               image,
               model='the',
               headers={}):
       
        field_data = {}
        field_data['file'] = ("filename", image)
        field_data['model_name'] = model

        m = MultipartEncoder(fields=field_data)
        r = requests.post(
            self.server_url+"/decode",
            data=m,
            headers={"Content-Type": m.content_type, **headers}
        )

        return r.json()

    def decode_local_file(self,
                          image_file_path,
                          model='the',
                          output_path=None,
                          headers={}):

        field_data = {}
        image = Image.open(image_file_path)
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, image.format.lower())

        # image
        field_data['file'] = (image.filename, image_bytes_io)
        field_data['model_name'] = model

        m = MultipartEncoder(fields=field_data)
        r = requests.post(
            self.server_url+"/decode",
            data=m,
            headers={"Content-Type": m.content_type,

                     **headers}
        )

        r = r.json()

        if output_path and r['secret_image']:
            secret_r = requests.get(r['secret_image'], stream=True)
            if secret_r.status_code == 200:
                with open(output_path, 'wb') as f:
                    secret_r.raw.decode_content = True
                    shutil.copyfileobj(secret_r.raw, f)         

        return r