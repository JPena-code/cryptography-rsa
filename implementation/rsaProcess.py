import os
import json
from keyManagment import key_gen as __key_gen
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def encryption(owner='', *, path_key='./keys', file_path=''):
  public_key: rsa.RSAPublicKey = __key_gen(owner, path=path_key, password='')
  with open(file_path, 'rb') as msg:
    cyphert_text = public_key.encrypt(msg.read(),
                                      padding=padding.OAEP(
                                        mgf=padding.MGF1(hashes.SHA256()),
                                        algorithm=hashes.SHA256(),
                                        label=None))
  encrypted_path = f'./messages/{owner}.json'
  cyphert_text = str(int.from_bytes(cyphert_text, 'big'))
  messages = [cyphert_text]
  if os.path.isfile(encrypted_path):
    owner_dict = json.load(open(encrypted_path, 'r'))
    messages.extend(owner_dict.get('messages', []))
  with open(encrypted_path, 'w') as file:
    json.dump({'messages': messages}, file)


def decryption(owner='',
               *,
               msg_path='',
               path_key='./keys',
               file_path='./decrypted',
               password):
  private_key: rsa.RSAPrivateKey = __key_gen(owner,
                                             is_private=True,
                                             path=path_key,
                                             password=password)
  msg_path = f'{msg_path}/{owner}.json'
  with open(msg_path, 'r') as msg:
    owner_dict = json.load(msg)
    messages = owner_dict.get('messages', [])
    for msg in messages:
      msg = transfor(msg)
      message = private_key.decrypt(msg.encode(),
                                    padding=padding.OAEP(
                                      mgf=padding.MGF1(hashes.SHA256()),
                                      algorithm=hashes.SHA256(),
                                      label=None))
      print(message.decode())


def sign():
  pass


def verify():
  pass
