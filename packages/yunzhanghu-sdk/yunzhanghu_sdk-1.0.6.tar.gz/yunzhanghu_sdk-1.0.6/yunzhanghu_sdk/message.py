# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import abc
import base64
import hashlib
import hmac
import json
import random
import time

import pyDes
import rsa
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


class Signer(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, data):
        return NotImplemented

    @abc.abstractmethod
    def sign(self, mess, timestamp, data):
        return NotImplemented

    @abc.abstractmethod
    def encrypt_type(self):
        return NotImplemented


class Des3EncryptAndHmacSign(Signer):
    def __init__(self, app_key, des3key):
        self.__app_key = app_key
        self.__des3key = des3key

    def encrypt_type(self):
        return "sha256"

    def encrypt(self, data):
        data = bytes(data, encoding="utf8")
        key = bytes(self.__des3key[0:8], encoding="utf8")
        return base64.b64encode(
            pyDes.triple_des(self.__des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).encrypt(data))

    def sign(self, mess, timestamp, encrypt_data):
        signPairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (
            str(encrypt_data, encoding="utf-8"), mess, timestamp, self.__app_key)
        app_key = bytes(self.__app_key, encoding="utf8")
        signPairs = bytes(signPairs, encoding="utf8")
        return hmac.new(app_key, msg=signPairs, digestmod=hashlib.sha256).hexdigest()


class Des3EncryptAndRSASign(Signer):
    def __init__(self, app_key, public_key, private_key, des3key):
        self.__public_key = RSA.importKey(public_key)
        self.__private_key = RSA.importKey(private_key)
        self.__app_key = app_key
        self.__des3key = des3key

    def encrypt_type(self):
        return "rsa"

    def encrypt(self, data):
        data = bytes(data, encoding="utf8")
        key = bytes(self.__des3key[0:8], encoding="utf8")
        return base64.b64encode(
            pyDes.triple_des(self.__des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).encrypt(data))

    def sign(self, mess, timestamp, encrypt_data):
        sign_pairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (
            bytes.decode(encrypt_data), mess, timestamp, self.__app_key)
        signer = Signature_pkcs1_v1_5.new(self.__private_key)
        digest = SHA256.new()
        digest.update(sign_pairs.encode("utf8"))
        sign = signer.sign(digest)
        return base64.b64encode(sign)


class ReqMessage(object):
    """
    ReqMessage 请求消息体
    """

    def __init__(self, encrypt, data):
        """
        :param encrypt: 加密方式
        :type data: {} 请求信息
        :param data: 请求信息
        """
        self.__encrypt = encrypt
        self.data = None
        if data is not None:
            self.data = json.dumps(data, ensure_ascii=False)

    def pack(self):
        if self.data is None:
            return None
        timestamp = int(time.time())
        mess = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxy', 10))
        encrypt_data = self.__encrypt.encrypt(self.data)
        return {
            "data": encrypt_data,
            "mess": mess,
            'timestamp': timestamp,
            "sign": self.__encrypt.sign(mess, timestamp, encrypt_data),
            "sign_type": self.__encrypt.encrypt_type()
        }


class RespMessage(object):
    """
    RespMessage 返回信息
    """

    def __init__(self, des3key, content, req_data, req_param, headers):
        self.__des3key = des3key
        self.__content = content
        dic = json.loads(content)
        self.__req_param = req_param
        self.__req_data = req_data
        self.__code = dic['code'] if 'code' in dic else None
        self.__message = dic['message'] if 'message' in dic else None
        self.__data = dic['data'] if 'data' in dic else None
        self.__request_id = headers['request-id']

    def decrypt(self):
        if self.__data is None:
            return self

        if self.__des3key is not None and self.__req_param is not None \
                and 'data_type' in self.__req_param and \
                self.__req_param['data_type'] == 'encryption':
            self.__data = json.loads(triple_des_decrypt(self.__des3key, self.__data))
        return self

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    @property
    def content(self):
        return self.__content

    @property
    def request_id(self):
        return self.__request_id


def triple_des_decrypt(des3key, data):
    """ 3DES 解密

    :type des3key: string
    :param des3key: 3DES 密钥

    :type data: string
    :param data: 待解密数据

    :return: 解密结果
    """
    data = bytes(data, encoding="utf8")
    key = bytes(des3key[0:8], encoding="utf8")
    return pyDes.triple_des(des3key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5).decrypt(base64.b64decode(data))


def verify_sign_rsa(public_key, app_key, data, mess, timestamp, signature):
    """ RSA 公钥验签

    :type public_key: string
    :param public_key: 云账户公钥

    :type app_key: string
    :param app_key: App Key

    :type data: string
    :param data: data

    :type mess: string
    :param data: 随机字符串

    :type timestamp: int
    :param data: 时间戳

    :type signature: string
    :param signature: 异步通知签名

    :return: 校验结果
    """
    sign_pairs = "data=" + data + "&mess=" + mess + "&timestamp=" + timestamp + "&key=" + app_key
    rsa.verify(sign_pairs, signature, public_key)


def verify_sign_hmac(app_key, data, mess, timestamp, signature):
    """HMAC 验签

    :type app_key: string
    :param app_key: App Key

    :type data: string
    :param data: data

    :type mess: string
    :param data: 随机字符串

    :type timestamp: int
    :param data: 时间戳

    :type signature: string
    :param signature: 异步通知签名

    :return: 校验结果
    """
    sign_pairs = "data=%s&mess=%s&timestamp=%d&key=%s" % (data, mess, timestamp, app_key)
    return hmac.new(app_key.encode('utf-8'), msg=sign_pairs, digestmod=hashlib.sha256).hexdigest() == signature


def notify_decoder(public_key, app_key, des3key, data, mess, timestamp, signature):
    res_data, verify_result = "", False
    if verify_sign_rsa(public_key, app_key, data, mess, timestamp, signature):
        res_data = triple_des_decrypt(des3key, data)
        verify_result = True
    return verify_result, res_data
