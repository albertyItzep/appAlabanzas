import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

PATH_INITIAL_DATA="./alabanzas"

client_R3 = boto3.client(
    'textract',
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name=''
)

def read_document(path: str):
    image_bytes=""
    try:
        with open(path,"rb") as document_file:
            image_bytes = document_file.read()
        return image_bytes
    except Exception as e:
        print("error al cargar imagen en bytes: "+e)
        return e

def get_text(image:bytes):
    try:
        response = client_R3.detect_document_text(
            Document={"Bytes":image}
        )
        texto_extraido=[]
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                texto_extraido.append(block['Text'])
        return texto_extraido
    except Exception as e:
        print("error al cargar imagen en bytes: "+e)
        raise e

def create_string(content):
    final_string = "-------------------------------------------\n"
    for x in content:
        final_string += x + "\n"
    final_string += "\n"
    return final_string

def save_string(text):
    try:
        f = open("alabanzas.txt", "a")
        f.write(text)
        f.close()
    except Exception as e:
        print("error al cargar imagen en bytes: "+e)
        raise e

#cargamos las imagenes
dir_content = os.listdir(PATH_INITIAL_DATA)

image_bytes = 0

for x in dir_content:
    image_bytes = read_document(PATH_INITIAL_DATA+"/"+x)
    array_block_text = get_text(image_bytes)
    text_extract = create_string(array_block_text)
    save_string(text_extract)
