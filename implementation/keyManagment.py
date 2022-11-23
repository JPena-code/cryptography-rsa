import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def key_gen(owner: str, is_private=False, *, password: str):

  exists = True
  current_keys = set(map(lambda x: x.split('_')[0], os.listdir('./keys')))
  if owner not in current_keys:
    print('You do not have a key pair yet\nGenerating a pair...')
    password = input('Enter a password for you private key\n> ')
    exists = False

  def __load_key(owner, path, password):
    with open(f'{path}/{owner}_pr.pem',
              'rb') as key_pr, open(f'{path}/{owner}_pub.pem',
                                    'rb') as key_pub:
      public_key = serialization.load_pem_public_key(key_pub.read(),
                                                     backend=default_backend)
      if not is_private:
        return public_key
      private_key = serialization.load_pem_private_key(key_pr.read(),
                                                       password.encode(),
                                                       backend=default_backend)
      return private_key

  if exists:
    return __load_key(owner, './keys', password)

  private_key = rsa.generate_private_key(public_exponent=65537,
                                         key_size=2048,
                                         backend=default_backend)
  public_key = private_key.public_key()

  with open(f'./keys/{owner}_pr.pem',
            'wb') as private, open(f'./keys/{owner}_pub.pem', 'wb') as public:
    private_pem = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.TraditionalOpenSSL,
      encryption_algorithm=serialization.BestAvailableEncryption(
        password.encode()))
    public_pem = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo)
    private.write(private_pem)
    public.write(public_pem)
  if is_private:
    return private_key
  return public_key
