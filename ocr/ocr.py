import json
import os
from typing import List, Tuple

from google.cloud import vision
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from io import BytesIO

from ocr.patterns import DATE_PATTERN, DIGITS_PATTERN, LONG_INTEGER_PATTERN, NUMBER_OF_CONTRACT_PATTERN, PACKAGE_LIST_PATTERN, TERMS_OF_DELIVERY_PATTERN
from ocr.utils.save_image import save_image
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.get_image import get_image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ocr/vision_key.json'
client = vision.ImageAnnotatorClient()


def detect_text(image, google_vision_client):
    """ Detects text in an image"""

    image = vision.Image(content=image)
    response = google_vision_client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    else:
        texts = response.text_annotations
        ocr_text = []

        for text in texts:
            ocr_text.append(f"\r\n{text.description}")

    return texts, ocr_text


def scan_google_ocr(img_url: str,
                    regex_pattern: None,
                    bounding_box: Tuple[int, int, int, int] = None,
                    ):
    client = vision.ImageAnnotatorClient()
    
    image = get_image(img_url)

    if bounding_box is not None:
        image = image.crop(bounding_box)
        
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer_img = buffer.getvalue()

    texts, ocr_text = detect_text(buffer_img, client)
    out_data = []
    if regex_pattern is not None and ocr_text is not None:
        out_data = regex_pattern.findall(ocr_text[0])[0]

    return texts, ocr_text, out_data, image


def read_document(box_images, pdf_file):
    documents = []
    
    image_dir = f"media/{extract_document_name(str(pdf_file.file))}"
    os.makedirs(image_dir, exist_ok=True)
    
    constants_bb = {
        '09029': [
            dict(bb=(177, 251, 420, 340),
                regex_pattern=DATE_PATTERN),
            dict(bb=(906, 250, 1101, 341),
                regex_pattern=DIGITS_PATTERN),
        ],
        '04021':[
            dict(
                bb=(149, 193, 513, 293),
                regex_pattern=DATE_PATTERN),
            dict(
                bb=(455, 250, 652, 407),
                regex_pattern=DATE_PATTERN),
            dict(
                bb=(149, 193, 513, 293),
                regex_pattern=PACKAGE_LIST_PATTERN),
            dict(
                bb=(554, 239, 950, 340),
                regex_pattern=NUMBER_OF_CONTRACT_PATTERN),
            dict(
                bb=(405, 510, 693, 595),
                regex_pattern=TERMS_OF_DELIVERY_PATTERN),
        ],
        '02016':[
            dict(
                bb=(792, 169, 989, 246),
                regex_pattern=DIGITS_PATTERN),
            dict(
                bb=(407, 849, 600, 952),
                regex_pattern=DATE_PATTERN),
        ],
        '01207':[
            dict(
                bb=(784, 204, 1130, 326),
                regex_pattern=LONG_INTEGER_PATTERN),
            dict(
                bb=(725, 815, 853, 907),
                regex_pattern=DATE_PATTERN),
        ],
        '01707':[
            dict(
                bb=(877, 209, 1069, 280),
                regex_pattern=DIGITS_PATTERN),
            dict(
                bb=(756, 665, 936, 753),
                regex_pattern=DATE_PATTERN),
        ],
        '09015':[
            dict(
                bb=(859, 171, 1283, 249),
                regex_pattern=DIGITS_PATTERN),
        ],
        '06999': [
            dict(
                bb=(875, 584, 1065, 746),
                regex_pattern=DATE_PATTERN),
        ],
    }
    
    
    constants_fields = {
        '09029': ['date','number'],
        '04021': ['date', 'date contract', 'packages lists', 'numbers of contacts', 'terms of deliveries'],
        '02016': ['number','date'],
        '01207': ['number', 'date'],
        '01707': ['number','date'],
        '09015': ['number'],
        '06999': ['date']
    }


    for box in box_images:
        fields = []
        
        params_dict = dict(
            doc_path= box_images[box],
            doc_params= constants_bb[box],
        )    
        
        for i in range(len(params_dict['doc_params'])):
            doc_path = params_dict["doc_path"]
            bb = params_dict["doc_params"][i]["bb"]
            regex_pattern = params_dict["doc_params"][i]["regex_pattern"]
            texts, ocr_text, out_data, image = scan_google_ocr(img_url=doc_path,
                                                            regex_pattern=regex_pattern,
                                                            bounding_box=bb)
            
            fields.append({
                constants_fields[box][i]: out_data,
                'image': save_image(image_dir, f'{box}_{constants_fields[box][i]}', image)
            })
            
        documents.append(
            json.dumps({
                'name': box,
                'original_image': box_images[box],
                'fields': fields
            })
        )
        print(json.dumps({
                'name': box,
                'original_image': box_images[box],
                'fields': fields
            }))

    return documents