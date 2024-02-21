import datetime
import json
import os

import pikepdf
from django.http import FileResponse
from django.shortcuts import render
from rest_framework import generics, permissions
# Create your views here.
from rest_framework.response import Response
import io
from user_auth.services import itd_login, itd_dashboard_data, itd_refund_status, itd_intimation_data, \
    itd_proceeding_data, itd_download_files, itd_proceeding_details
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# import binascii
# import rsa
from sys import platform
import ast


class DashboardDataView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        # Generate a new RSA key pair
        # key = RSA.generate(2048)
        # public_key_pem = key.publickey().export_key()
        # print(public_key_pem)
        #
        # # Print the private key in PEM format
        # private_key_pem = key.export_key()
        # print(private_key_pem)

        # Save the public key to a file
        # with open("public_key.pem", "wb") as public_key_file:
        #      public_key_file.write(public_key_pem)
        # with open("private_key.pem", "wb") as private_key_file:
        #     private_key_file.write(private_key_pem)
        # Save the private key to a file
        # with open("public_key.pem", "rb") as public_key_file:
        #     public_key = RSA.import_key(public_key_file.read())
        # with open("private_key.pem", "rb") as private_key_file:
        #     private_key = RSA.import_key(private_key_file.read())
        # test_message = "Hello message to encrypt"
        #
        # message = ast.literal_eval(request.data['encrypted_message'])
        # params = request.query_params.dict()
        # cip_string = "Yei7wsgJlU0J2cos3Ne/mkWHVl9XyjUulE+uy+FPCGEUK1zEWyAycT8c4blJDSZG2hIW8cMtzkTktXZFYfuFXpizORAS1eKdywZ5KGdnNibqwpjZVkSJzdYudVczQQehFxVDTMve3fyJBSpJhIgZncBlbePmshNCZVuJPJ6dKPk="
        # message_bytes = message.encode('utf-8')
        # test_bytes = test_message.encode('utf-8')
        # cipher = PKCS1_OAEP.new(public_key)
        # encrypted_message = cipher.encrypt(test_bytes)
        # pri_cipher = PKCS1_OAEP.new(private_key)
        # decrypted_message = pri_cipher.decrypt(message)
        # print(decrypted_message.decode('utf-8'))
        # with open("rsa_mytb.pem", "rb") as key_file:
        #     private_key = RSA.import_key(key_file.read())
        #     cipher = PKCS1_OAEP.new(private_key)
        #     decrypted_message = cipher.decrypt(bytes(cip_string, 'ascii'))
        #     data_json = json.loads(decrypted_message)
        # if params['encrypted']:
        #     cipherText = request.data
        #     with open('rsa_mytb.pem', 'rb') as p:
        #         privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        #         text = decrypt(cipherText, privateKey)
        #         req_data = json.loads(text)
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        dashboard_data = itd_dashboard_data(username=request.data['username'], password=request.data['password'],
                                            auth_token=auth_token).json()
        if len(dashboard_data['message']) > 0:
            dashboard_data = json.loads(dashboard_data['message'])
            return Response(dashboard_data, status=200)
        else:
            return Response({"message": "No data found"}, status=400)


class RefundStatementData(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        refund_data = itd_refund_status(username=request.data['username'], password=request.data['password'],
                                        auth_token=auth_token).json()
        if len(refund_data['message']) > 0:
            refund_data = json.loads(refund_data['message'])
            return Response(refund_data, status=200)
        else:
            return Response({"message": "No data found"}, status=400)


class IntimationData(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        intimation_data = itd_intimation_data(username=request.data['username'], password=request.data['password'],
                                              auth_token=auth_token).json()
        if len(intimation_data['message']) > 0:
            intimation_data = json.loads(intimation_data['message'])
            return Response(intimation_data, status=200)
        else:
            return Response({"message": "No data found"}, status=400)


class ProceedingData(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        proceeding_data = itd_proceeding_data(username=request.data['username'], password=request.data['password'],
                                              auth_token=auth_token).json()
        proceeding_data = json.loads(proceeding_data['message'])
        for i in range(0, len(proceeding_data['eproceedingRequests'])):
            request_type = "GetEProceedingDetails#" + proceeding_data['eproceedingRequests'][i]['proceedingReqId']
            proceedingDetail = json.loads(itd_proceeding_details(username=request.data['username'],
                                                                 password=request.data['password'],
                                                                 auth_token=auth_token,
                                                                 request_type=request_type).json()['message'])[0]
            proceeding_data['eproceedingRequests'][i]['issuedOn'] = proceedingDetail['issuedOn']
            proceeding_data['eproceedingRequests'][i]['responseDueDate'] = proceedingDetail['responseDueDate']
            proceeding_data['eproceedingRequests'][i]['readFlag'] = proceedingDetail['readFlag']
            proceeding_data['eproceedingRequests'][i]['eProceedingDetails'] = proceedingDetail
            notices_request_type = "#".join(
                ['GetEProceedingNoticesDetails', proceedingDetail['proceedingReqId'], proceedingDetail['headerSeqNo']])
            noticesDetails = json.loads(itd_proceeding_details(username=request.data['username'],
                                                               password=request.data['password'],
                                                               auth_token=auth_token,
                                                               request_type=notices_request_type).json()['message'])
            if noticesDetails['docMap'] and len(noticesDetails['docMap']) > 0:
                docNo = list(noticesDetails['docMap'].keys())[0]
                proceeding_data['eproceedingRequests'][i]['eProceedingDetails']['noticeFile'] = "#".join([
                    "EProceedingsNotices", proceedingDetail['proceedingReqId'], proceedingDetail['headerSeqNo'], docNo])
            else:
                proceeding_data['eproceedingRequests'][i]['eProceedingDetails']['noticeFile'] = None
        if len(proceeding_data) > 0:
            # proceeding_data = json.loads(proceeding_data['message'])
            return Response(proceeding_data, status=200)
        else:
            return Response({"message": "No data found"}, status=400)


class AcknowledgementFile(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        request_type = "ackNum#" + request.data['ackNum'] + "#" + request.data['assmentYear']
        file_data = itd_download_files(username=request.data['username'], password=request.data['password'],
                                       auth_token=auth_token, request_type=request_type).content

        return FileResponse(io.BytesIO(file_data), filename=request_type + ".pdf", status=200)


class IntimationFile(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        request_type = "#".join(
            ["commRefNo", request.data['commRefNo'], request.data['assmentYear'], request.data['submitUserId']])
        file_data = itd_download_files(username=request.data['username'], password=request.data['password'],
                                       auth_token=auth_token, request_type=request_type).content
        dob = datetime.datetime.strptime(request.data['dob'], '%Y-%m-%d')
        password = request.data['submitUserId'].lower()
        zero_padding_remover = "-"
        if platform == 'win64' or platform == 'win32':
            zero_padding_remover = "#"
        password = password + dob.strftime("%d%" + zero_padding_remover + "m%Y")
        pdf_file = pikepdf.open(io.BytesIO(file_data), password=password)

        return FileResponse(pdf_file, filename=request_type + ".pdf", status=200)


class ProceedingNoticeFile(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        auth_token = itd_login(username="1234", password="Sinewave@T!5b)2^M").text.replace('"', "")
        request_type = request.data['noticeFile']
        file_data = itd_download_files(username=request.data['username'], password=request.data['password'],
                                       auth_token=auth_token, request_type=request_type).content
        return FileResponse(io.BytesIO(file_data), filename=request_type + ".pdf.gz", status=200)


from .eportal_tis import TIS
from .eportal_ais import AIS

class TISFile(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        file_path = TIS().test_tis(**request.data)
        try:
            with open(file_path, 'rb') as f:
                response = FileResponse(io.BytesIO(f.read()))
                response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
                return response
        except Exception as e:
            return Response({
                                "message": "File download failed. Please try again if the credentials are correct. This may happen due to unavailability of requested services.",
                                "status": "False"})

class AISFile(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        file_path = AIS().test_ais(**request.data)
        try:
            with open(file_path, 'rb') as f:
                response = FileResponse(io.BytesIO(f.read()))
                response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
                return response
        except Exception as e:
            return Response({
                                "message": "File download failed. Please try again if the credentials are correct. This may happen due to unavailability of requested services.",
                                "status": "False"})


from .test_form26as import TestForm26as


class Form26AS(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        file_path = TestForm26as().test_form26as(**request.data)
        try:
            with open(file_path, 'rb') as f:
                response = FileResponse(io.BytesIO(f.read()))
                response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
                return response
        except Exception as e:
            return Response({"message": "File download failed. Please try again if the credentials are correct. This may happen due to unavailability of requested services.",
                                "status": "False"})


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except Exception as e:
        raise e


def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key, ) == 'SHA-1'
    except:
        return False
