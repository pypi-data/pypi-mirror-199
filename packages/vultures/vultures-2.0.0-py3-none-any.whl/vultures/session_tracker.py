import abc
import requests
import logging
import json

from tkinter import messagebox
from datetime import datetime

from .aes import AESCipher
from .rsa_crypto import RSA_Crypto, create_rsa_key_object, verify_signature
from .rsa_token import RSA_Token_Encryption, RSA_Token_Decryption

class Session(abc.ABC):
    # Dynamic instead of hardcoding in the future
    auth_server = "192.168.1.195"
    auth_server_check_login = f"{auth_server}/login"
    auth_server_challenge_token = f"{auth_server}/challenge_token"
    auth_server_verify_user = f"{auth_server}/verify_user"
    
    # High point of attack
    auth_get_server_uuid = f"{auth_server}/get_server_uuid"
    
    # Implement search_local_auth_db ater
    @classmethod
    def find_public_key(cls, uuid: str):
        public_key = search_local_auth_db(uuid)
        
        if public_key:
            return public_key
        else:
            return None
            # Log and raise error if not found
        
    @classmethod
    def get_server_uuid(cls):
        response = requests.get(cls.auth_get_server_uuid)
        
        if response.status_code == 200:
            server_uuid = response.json()["uuid"]
            
            if server_uuid != -1:
                return server_uuid
            else:
                pass
                # Log here
        else:
            pass
            # Log here
    """
    API Endpoint: /get_rsa_token
    Client Supplied: uuid: str
    Hidden knowns: users_public_key in database/cert list
    Server:
        Gets aes key and auth code from auth_server
        Sends back: encrypted rsa token
    """
    @classmethod
    def get_challenge_token(cls, uuid: str):
        response = requests.post(cls.auth_server_challenge_token, json = {"uuid": uuid})
        
        if response.status_code == 200:
            return response.json()["token"]
            
        return False

    @classmethod
    def decrypt_challenge_token(cls, user_rsa_cipher_obj, token: dict, server_uuid: str, server_public_key):
        message = user_rsa_cipher_obj.decrypt(token["data"]
                
        if verify_signature(user_rsa_cipher_obj, message, token["signature"], server_public_key): 
            return json.loads(message)
        else:
            pass
            # Log here
        return False        
        
    @classmethod
    def encrypt_token(cls, user_rsa_cipher_obj, token: dict, server_public_key):
        return user_rsa_cipher_obj.encrypt(token, server_public_key)
        
    @classmethod
    def verify_user(cls, username):
        response = requests.post(cls.auth_server_verify_user, json={"username": username})
        
        if response.status_code == 200:
            uuid = response.json()["accepted"]
            
            if uuid != -1:
                return uuid
        raise Exception("Need to add the uuid to the auth_db")
        
    def __init__(self, username, password, rsa_key_pair: dict):
        self.__uuid = self.verify_user()
        self.__logged_in = False
                
        self.username = username
        self.password = password
        self.public_key = rsa_key_pair["public_key"]
        self.private_key = rsa_key_pair["private_key"]
        
        self.rsa_cipher_obj = RSA_Crypto(keys = [self.public_key, self.private_key])
        
        self.refresh_server_credentials()
        
    def refresh_server_credentials(self):
        self.server_uuid = self.get_server_uuid()
        self.server_public_key = self.find_public_key(self.server_uuid)
        
    @abc.abstractmethod
    def check_login(self):
        pass
        
    @property
    def uuid(self):
        return self.__uuid
        
    @uuid.setter
    def uuid(self, identifier: str):
        self.__uuid = identifier
    
    @uuid.deleter
    def uuid(self):
        self.__uuid = None
    
    @property
    def logged_in(self):
        return self.__logged_in
    
    @logged_in.setter
    def logged_in(self, value: bool):
        self.__logged_in = value
        
    def log_out(self):
        self.logged_in = False
        
    def send_login(self):        
        json_data = {"uuid": self.uuid}
        json_data["data"] = self.encrypt_token({"username": self.username, "password": self.password))
         
        response = requests.post(self.auth_server_login, json=json_data)
        
        if response.status_code != 200:
            return False, response.status_code
        else:
            response_data = response.json()
            if response_data["accepted"]:
                # Response data will be server endpoint, aes, and time_of_use_code
                # Essentially a second RSA Token for application use
                return True, response_data["token"]
            else:
                return False, -1
        
class TkinterSession(Session):
    def __init__(self, username, password):
        super().__init__(username, password)
        
    def check_login(self):
        request_boolean, token = self.send_login()
        
        if request_boolean is False and token != -1:
            messagebox.showerror("Error", f"Server is not working right now: {self.server_uri}")
        elif token == -1:
            messagebox.showwarning("Access denied!", f"Credentials, {self.username} {self.password}, failed!")
        else:
            self.aesKey = token["aes_key"]
            self.auth_server_code = token["code"]
            self.time_of_use = token["time_of_use"]
            self.logged_in = True
            return True
        return False 
            
class RegularSession(Session):
    def __init__(self, username, password):
        super().__init__(username, password)
        
    def check_login(self):
        request_boolean, request_data = self.send_login()
        
        if request_boolean:
            self.aesKey = token["aes_key"]
            self.auth_server_code = token["code"]
            self.time_of_use = token["time_of_use"]
            self.logged_in = True
            return True
            
#------------------------------------
# Needs to be rigously tested
#------------------------------------
class MonitorSessions(dict):    
    logger = logging.getLogger(__name__)
    FORMAT = '%(name)s:%(levelname)s:%(message)s:%(asctime)s"
    handler = logging.FileHandler("/usr/Sphinx/logs/client_auth.log", mode="a")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    sessions = {}
    
    def __new__(mcs, name, bases, dictionary):
    
    def log_info(mcs, message, logger_type, setting_key = True, dictionary = {}):
        if setting_key:
            uuid = dictionary['uuid']
            key = {"uuid": uuid, "server_url": dictionary["server_url"], "encrypted_token": dictionary["encrypted_token"], timestamp: datetime.now().strftime("%m-%d-%y %H:%M:%S")}
            
            mcs.logger.info(json.dumps(key))
            
            if uuid not in sessions.keys():
                sessions[uuid] = [key]
            else:
                sessions[uuid].append(key)
        else:
            if logger_type == "warning":
                self.logger.warning(log_message)
            elif logger_type == "debug":
                self.logger.debug(log_message)
            elif logger_type == "critical":
                self.logger.critical(log_message)
            else:
                self.logger.info(log_message)           
            
# Not sure if you can do this
class SessionDict(dict, metaclass=MonitorSessions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def message(self):
        return f" was accessed in {self.__name__};"
    
    def __getitem__(self, key):
        log_message = f"{key} {self.message()}"
        
        if self.verify_user(username):
            val = super().__getitem__(key)
            self.log_info(log_message, "info")
            return val
        
        self.log_info(f"{log_message} but was not in the authentication database!", "warning")
        raise KeyError("Key doesn't exist!")
        
    # Need to fix
    # kwargs: uuid, server_url, encrypted token
    def __setitem__(self, key, val):
        log_message = f"{key} {self.message()}"
        
        # Check how to do this with abstract base classes!
        # Better way?!?!
        if isinstance(Session, val):
            super().__setitem__(key, val)
            self.log_info(log_message, "info", token)
            #self.logger.info(log_message)
            return True
        
        self.log_info(f"{log_message} {val} is not of Session type!", "warning")
        raise KeyError("Value is not of Session type!") 
