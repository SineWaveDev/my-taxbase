import requests
from requests.exceptions import HTTPError
from my_taxbase_service.settings import SMS_AUTH_KEY, SMS_TEMPLATE_ID, SMS_SENDER_ID

ITDService_URL = "http://itdservices.sinewave.co.in/api/"


def itd_login(username, password):
    url = ITDService_URL + "Login"
    response = requests.post(url, {"UserName": username, "Password": password})
    if response.status_code == 200:
        return response
    else:
        raise HTTPError("Invalid credentials")


def itd_dashboard_data(username, password, auth_token):
    url = ITDService_URL + "common/GetData"
    headers = {
        "Authorization": auth_token
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": "GetDashBoardData"
    }, headers=headers)
    while len(response.json()['message']) < 3 and retry_count < 2:
        response = requests.post(url, {
            "UserName": username,
            "Password": password,
            "RequestType": "GetDashBoardData"
        }, headers=headers)
        retry_count += 1
    return response


def itd_refund_status(username, password, auth_token):
    url = ITDService_URL + "common/GetData"
    headers = {
        "Authorization": auth_token
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": "GetRefundStatementData"
    }, headers=headers)
    while len(response.json()['message']) < 3 and retry_count < 2:
        response = requests.post(url, {
            "UserName": username,
            "Password": password,
            "RequestType": "GetRefundStatementData"
        }, headers=headers)
        retry_count += 1
    return response


def itd_intimation_data(username, password, auth_token):
    url = ITDService_URL + "common/GetData"
    headers = {
        "Authorization": auth_token
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": "GetIntimationData"
    }, headers=headers)
    while len(response.json()['message']) < 3 and retry_count < 2:
        response = requests.post(url, {
            "UserName": username,
            "Password": password,
            "RequestType": "GetIntimationData"
        }, headers=headers)
        retry_count += 1
    return response


def itd_proceeding_data(username, password, auth_token):
    url = ITDService_URL + "common/GetData"
    headers = {
        "Authorization": auth_token
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": "GetEProceedingData"
    }, headers=headers)
    while len(response.json()['message']) < 3 and retry_count < 2:
        response = requests.post(url, {
            "UserName": username,
            "Password": password,
            "RequestType": "GetEProceedingData"
        }, headers=headers)
        retry_count += 1
    return response


def itd_download_files(username, password, auth_token, request_type):
    url = ITDService_URL + "DownloadFiles/DownloadFile"
    headers = {
        "Authorization": auth_token,
        "Accept-Encoding": "gzip, deflate, br"
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": request_type
    }, headers=headers)

    return response


def itd_proceeding_details(username, password, auth_token, request_type):
    url = ITDService_URL + "common/GetData"
    headers = {
        "Authorization": auth_token
    }
    retry_count = 0
    response = requests.post(url, {
        "UserName": username,
        "Password": password,
        "RequestType": request_type
    }, headers=headers)

    return response


def send_sms(mobile, data, template_id):
    url = "https://control.msg91.com/api/v5/flow/"
    headers = {
        "authkey": SMS_AUTH_KEY
    }
    params = {
        "template_id": template_id,
        "sender": SMS_SENDER_ID,
        "short_url": 0,
        "mobiles": str(mobile)
    }
    params.update(data)
    response = requests.post(url, json=params, headers=headers)
    pass
