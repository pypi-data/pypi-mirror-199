import base64
import urllib.parse
import requests
from .config import API_KEY,SECRET_KEY





class result:

    def __init__(self,r1,r2,r3):

        self._str = r1
        self._split = r2
        self._list = r3


class l_result:

    def __init__(self,r1,r2,r3):

        self._str = r1
        self._split = r2
        self._dict = r3


def get_access_token():


    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """


    url = "https://aip.baidubce.com/oauth/2.0/token"

    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}

    return str(requests.post(url, params=params).json().get("access_token"))

def get_file_content_as_base64(Path, urlencoded=True):


    """
    获取文件base64编码

    :param path: 文件路径

    :param urlencoded: 是否对结果进行urlencoded

    :return: base64编码信息
    """


    with open(Path, "rb") as f:

        content = base64.b64encode(f.read()).decode("utf8")

        if urlencoded:

            content = urllib.parse.quote_plus(content)

    print(content)

    return content


def ocr(AbsolutePath):

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    content = get_file_content_as_base64(Path=AbsolutePath)


    payload = 'image='+content+'&language_type=CHN_ENG&detect_direction=true&detect_language=true&probability=true'

    headers = {

        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'

    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    """
    try:

        resp = ''
        for i in response.text['words_result']:

            resp += i['words'] + ' '
        ress = ''
        for i in response.text['words_result']:

            ress += i['words']
        resl = []
        for i in response.text['words_result']:

            resl.append(i['words'])


        return result(r1=ress,r2=resp,r3=resl)
    except:
    """

    return response.text


def high_accuracy_ocr(AbsolutePath):

    content = get_file_content_as_base64(Path=AbsolutePath)
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()


    payload = 'image='+content+'&language_type=CHN_ENG&detect_direction=true&detect_language=true&probability=true'

    headers = {

        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'

    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    # try:
    #
    #     resp = ''
    #     for i in response.text['words_result']:
    #
    #         resp += i['words'] + ' '
    #     ress = ''
    #     for i in response.text['words_result']:
    #
    #         ress += i['words']
    #     resl = []
    #     for i in response.text['words_result']:
    #
    #         resl.append(i['words'])
    #
    #
    #     return result(r1=ress,r2=resp,r3=resl)
    # except:

    return response.text


def Handwritten_ocr(AbsolutePath):

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=" + get_access_token()
    content = get_file_content_as_base64(Path=AbsolutePath)


    payload = 'image=' + content + '&language_type=CHN_ENG&detect_direction=true&detect_language=true&probability=true'

    headers = {

        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'

    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    # try:
    #
    #     resp = ''
    #     for i in response.text['words_result']:
    #
    #         resp += i['words'] + ' '
    #     ress = ''
    #     for i in response.text['words_result']:
    #
    #         ress += i['words']
    #     resl = []
    #     for i in response.text['words_result']:
    #
    #         resl.append(i['words'])
    #
    #
    #     return result(r1=ress,r2=resp,r3=resl)
    # except:

    return response.text


def ocr_with_location(AbsolutePath):

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=" + get_access_token()
    content = get_file_content_as_base64(Path=AbsolutePath)


    payload = 'image='+content+'&language_type=CHN_ENG&detect_direction=true&detect_language=true&probability=true'


    headers = {

        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'

    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    # resp = ''
    # for i in response.text['words_result']:
    #     resp += i['words'] + ' '
    # ress = ''
    # for i in response.text['words_result']:
    #     ress += i['words']
    # resd = {}
    # for i in response.text['words_result']:
    #     resd[i['words']] = i['location']
    #
    # return l_result(r1=ress, r2=resp, r3=resd)
    # try:
    #
    #     resp = ''
    #     for i in response.text['words_result']:
    #
    #         resp += i['words'] + ' '
    #     ress = ''
    #     for i in response.text['words_result']:
    #
    #         ress += i['words']
    #     resd = {}
    #     for i in response.text['words_result']:
    #
    #         resd[i['words']] = i['location']
    #
    #
    #     return l_result(r1=ress,r2=resp,r3=resd)
    # except:
    #
    return response.text