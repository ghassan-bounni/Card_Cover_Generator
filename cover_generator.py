import os
import logging
import dotenv
import requests
import boto3
from PIL import Image
from rembg import remove
from botocore.exceptions import ClientError

dotenv.load_dotenv()


def generate_card_images(reason_keywords, orientation="portrait", clean="n"):
    # using stable-diffusion api to generate image for card
    if orientation == "portrait":
        width = 1024
        height = 744
    else:
        width = 744
        height = 1024
    output = []
    for i in range(len(reason_keywords)):
        json = {
            "key": os.environ["SD_API_KEY"],
            "model_id": os.environ["SD_MODEL_ID"],
            "enhance_prompt": "no",
            "samples": 1,
            "webhook": "",
            "track_id": "",
            "prompt": f"{reason_keywords[i]}, sticker, symmetric, highly detailed sticker, vector illustration,"
                      f" rich colors, smooth and clean vector curves, no jagged lines, minimalist, white background,"
                      f"illustration",
            "negative_prompt": "realistic real low quality multiple, text, logo",
            "num_inference_steps": 31,
            "seed": "null",
            "guidance_scale": 7,
            "width": width,
            "height": height,
            "scheduler": "EulerAncestralDiscreteScheduler",
        }
        response = requests.post(os.environ["SD_TEXT2IMG_URL"], json=json, timeout=60)
        res = response.json()["output"]
        res_id = response.json()["id"]

        while not res:
            response = requests.post(
                os.environ["SD_FETCH_URL"],
                json={"key": os.environ["SD_API_KEY"], "request_id": res_id},
                timeout=60,
            )
            if response.json()["status"] == "success":
                res = response.json()["output"]
                break
            elif response.json()["status"] == "failed":
                print(f"retrying img {i}")
                i = i - 1
                break

        if not response.json()["status"] == "failed":
            output.append(res[0])

    if clean == "y":
        cleaned = []
        for url in output:
            cleaned.append(remove_bg(url))
        return {
            "original": output,
            "cleaned": cleaned,
            "upscale": upscale_images(output),
            "cleaned_upscale": upscale_images(cleaned),
        }

    return {
        "original": output,
        "upscale": upscale_images(output),
    }


def upscale_images(img_urls):
    # using stable-diffusion api to upscale image
    upscale_urls = []
    for img_url in img_urls:
        json = {
            "key": os.environ["SD_UPSCALE_URL"],
            "url": img_url,
            "scale": 2,
            "webhook": "null",
            "face_enhance": "false",
        }
        response = requests.post(os.environ["SD_UPSCALE_URL"], json=json, timeout=60).json()
        upscale_urls.append(response["output"])

    return upscale_urls


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
    )
    try:
        _ = s3_client.upload_file(file_name, bucket, object_name)
        s3_url = f"https://{os.environ['S3_BUCKET_NAME']}.s3.amazonaws.com/{object_name}"
    except ClientError as error:
        logging.error(error)
        return False, None
    return True, s3_url


def remove_bg(url):
    file_name = f"images/{url.split('/')[-1]}"
    output_path = f"images/clean/{url.split('/')[-1]}"
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(r.content)
    try:
        input_img = Image.open(file_name)
        output = remove(input_img)
        output.save(output_path)
    except IOError as error:
        print(str(error))

    res, url = upload_file(output_path, os.environ['S3_BUCKET_NAME'])
    if not res:
        print("Upload failed")

    os.remove(file_name)
    os.remove(output_path)

    return url
