import io
import os
import uuid
from config import conf
from common.log import logger
from tools.tool import tool
from common.tmp_dir import TmpDir


@tool("Get Image Description", return_direct=False)
def image2text(image_path: str) -> str:
    """
    useful when you want to know what is inside the photo. receives image_path as input.
    The input to this tool should be a string, representing the image_path.
    """
    try:
        import requests

        url = 'http://{}:{}/i2t'.format(conf().get('gpu_host', 'http://192.168.7.161'),
                                        conf().get('image2text_port', 7861))
        resp = requests.post(url=url, files={'file': open(image_path, 'rb')})
        text = resp.json().get('message')
        logger.info("image2text result: " + str(text))
        if 'error' not in text:
            return text
    except Exception as e:
        logger.error("image2text catch a error: " + str(e))
    return ""


@tool("Generate Image From Text", return_direct=False)
def text2image(query: str) -> str:
    """
        useful when you want to generate an image from a user input text and send to user
        like: generate an image of an object or includes some objects.
        The input to this tool should be a string, representing a prompt for AI art generation model.
        A prompt consisting of 6~12 compact but vivid phrases, each of which are separated with commas,
        describing the subject, location, style, color, lighting, artist of the image.
        Scenery example: Fujiyama, snow, winter, outdoors, sky, day, landscape, water, blue sky, waterfall,
        tree, nature, lake, river, cloudy sky, award winning photography, Bokeh, Depth of Field, HDR, bloom,
        Chromatic Aberration, Photorealistic, extremely detailed, trending on artstation, art by midjourney.
        Person example: 1girl, petite, small breasts, long hair, blonde hair, witch hat, slightly smile,
        purple eyes, star shaped pupils, underwater, kelp, aquarium, looking at viewer, solo, water splash,
        alice in wonderland dress, long socks, stripe blue socks, floating, rim lights, cinematic lighting.
    """
    try:
        import webuiapi
        from PIL import Image

        api = webuiapi.WebUIApi(host=conf().get('gpu_host', 'http://192.168.7.161'),
                                port=conf().get('sd_config', {}).get('port', 7860))
        response = api.txt2img(
            prompt=_build_prompt_text(query),
            negative_prompt=_build_nagetive_prompt_text(),
            sampler_name='DPM++ SDE Karras',
            cfg_scale=9,
            steps=conf().get('sd_config', {}).get('steps', 30),
            width=conf().get('sd_config', {}).get('width', 512),
            height=conf().get('sd_config', {}).get('height', 512)
        )
    except Exception as e:
        logger.error("call txt2img api error: " + str(e))
        return None
    image_bytes = io.BytesIO()
    response.image.save(image_bytes, format="PNG")

    image = Image.open(image_bytes)
    image_path = os.path.join(TmpDir().path(), f'output{str(uuid.uuid4())}.png')
    image.save(image_path)

    return image_path


# todo
def _build_prompt_text(text):
    now_model = _get_model()
    base_prompt = "(best quality, ultra-detailed, masterpiece, RAW photo:1.2), <lora:ForegroundPlantV11:0.3>"
    text = base_prompt + ", ((" + text + "))"
    if 'chilloutmix' in now_model:
        # this is real style
        base_prompt += ", <lora:cuteGirlMix4V10:0.6>, mix4, <lora:Korean-doll-likeness:0.6>, radiosity" \
                       ", (realistic, photo-realistic:1.37), professional lighting, photon mapping, " \
                       "physically-based rendering"
    elif 'counterfeit' in now_model:
        # this is anime style
        base_prompt += ', <lora:majoNoTabitabiElainaV30:0.3>, 8k wallpaper, elaborate features' \
                       ', (extremely detailed CG, beautiful detailed eyes, intricate detailed:1.2)'
    lora_list = conf().get('sd_config', {}).get('lora', {})
    if lora_list.get('howlsMovingCastIeInterior', False):
        # https://civitai.com/models/14605/howls-moving-castle-interior-scenery-lora-ghibli-style-v3
        text += f", <lora:howlsMovingCastleInteriorV3:{lora_list['howlsMovingCastIeInterior']}>"
    if lora_list.get('pastelMixStylizedAnime', False):
        # 粉彩混合lora https://civitai.com/models/5414/pastel-mix-stylized-anime-model
        text += f", <lora:pastelMixStylizedAnime:{lora_list['pastelMixStylizedAnime']}>"
    if lora_list.get('standingFullBodyWithBackgroundStyle', False):
        # 带背景立绘/背景付き立ち絵 https://civitai.com/models/16997/standing-full-body-with-background-style-lora
        text += f", <lora:standingFullBodyWithBackgroundStyleV10Offset:{lora_list['standingFullBodyWithBackgroundStyle']}>"
    return text


def _get_model():
    import webuiapi

    api = webuiapi.WebUIApi(host=conf().get('gpu_host', 'http://192.168.7.161'),
                            port=conf().get('sd_config', {}).get('port', 7860))
    options = api.get_options()
    now_model_name = options.get('sd_model_checkpoint', '')
    if now_model_name:
        logger.info("now model is: " + str(now_model_name))
    return now_model_name


def _build_nagetive_prompt_text():
    now_model = _get_model()
    base_prompt = "(worst quality:2), (low quality:2), (normal quality:1.5), ((monochrome)), ((grayscale)), " \
                  "bad anatomy, (logo, text), ugly, (interlocked fingers, Ugly Fingers:1.2), " \
                  "(interlocked fingers:1.2), (extra digit and hands and fingers and legs and arms:1.4), " \
                  "(deformed fingers:1.2), (long fingers:1.2), (bad-artist-anime), Multiple arms, Multiple legs, " \
                  "poorly drawn face, (by bad-artist:1.2), (nsfw:1.5)"
    if 'chilloutmix' in now_model:
        base_prompt += ", skin spots, acnes, skin blemishes, age spot"
    elif 'counterfeit' in now_model:
        base_prompt += ", EasyNegative"
    return base_prompt
