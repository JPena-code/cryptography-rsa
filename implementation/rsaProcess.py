import os
import json
from time import sleep
from keyManagment import key_gen as __key_gen
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def encryption(owner='', *, path_key='./keys', file_path=''):
  public_key: rsa.RSAPublicKey = __key_gen(owner, password='')
  with open(file_path, 'rb') as msg:
    cyphert_text = public_key.encrypt(msg.read(),
                                      padding=padding.OAEP(
                                        mgf=padding.MGF1(hashes.SHA256()),
                                        algorithm=hashes.SHA256(),
                                        label=None))
  encrypted_path = f'./messages/{owner}.json'
  messages = [cyphert_text.hex()]
  if os.path.isfile(encrypted_path):
    owner_dict = json.load(open(encrypted_path, 'r'))
    messages.extend(owner_dict.get('messages', []))
  with open(encrypted_path, 'w') as file:
    json.dump({'messages': messages}, file)
  sleep(20)


def decryption(owner='',
               *,
               msg_path='',
               path_key='./keys',
               file_path='./decrypted',
               password):
  private_key: rsa.RSAPrivateKey = __key_gen(owner,
                                             is_private=True,
                                             password=password)
  msg_path = f'{msg_path}/{owner}.json'
  if not os.path.isfile(msg_path):
    with open(msg_path, 'w') as file:
      json.dump({}, file)
  with open(msg_path, 'r') as msg:
    owner_dict = json.load(msg)
    messages = owner_dict.get('messages', [])
    if not messages:
      print('You do not have messages yet')
      return
    print(f'You have {len(messages)} messages')
    for index, msg in enumerate(messages, start=1):
      bytesMsg = bytes.fromhex(msg)
      message = private_key.decrypt(bytesMsg,
                                    padding=padding.OAEP(
                                      mgf=padding.MGF1(hashes.SHA256()),
                                      algorithm=hashes.SHA256(),
                                      label=None))
      print(f'\t[{index}] > {message.decode()}')
      sleep(10)