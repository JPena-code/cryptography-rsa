import re
import json
import random

START_MSG = """
  RSA Simulator developed by
    > Julio Quintero 
    > Andres Aponte
  
  Please select an option
    [1] Generat 🗝 
    [2] Encrypt a message
    [3] Decrypt a message
    [enter] Exit
> """


def gcd(a, b):
  if b == 0:
    return abs(a)
  return gcd(b, a % b)


def is_prime(n):
  """
    Check if a number is prime usign regex
  """
  return re.compile(r'^1?$|^(11+)\1+$').match('1' * n) is None


def random_prime():
  """
	  This function yield a random choice for 
    the list of prime numbers  that are store
	"""
  n = 101
  primes = [x for x in range(n) if is_prime(x)]
  while True:
    yield random.choice(primes)


def gen_keys(owner):
  p = q = 0
  while p == q and p * q < 127:
    p = next(random_prime())
    q = next(random_prime())
  n = p * q
  phi_n = (p - 1) * (q - 1)
  keys = {
    'modulos': n,
  }
  private = next(random_prime())
  while gcd(private, phi_n) != 1 or (private <= p or private <= q):
    private = next(random_prime())
  keys['private'] = private
  keys['public'] = pow(private, -1, phi_n)
  with open(f'{owner}_key.json', 'w') as key_files:
    json.dump(keys, key_files)


def encrypt(msg: str, public, modulos):
  msg_num = map(ord, msg)
  encrypted = []
  for num in msg_num:
    val = pow(num, public, modulos)
    encrypted.append(str(val))
  return encrypted


def decrypt(msg, private, modulos):
  decrypted = []
  for num in msg:
    val = pow(num, private, modulos)
    decrypted.append(chr(val))
  return ''.join(decrypted)


def rsa():
  option = input(START_MSG)
  while option != '':
    while option not in ['1', '2', '3']:
      option = input('Error! Enter a valid option\n> ')
    if option == '1':
      owner = input('Enter the name for the key owner\n> ').lower()
      gen_keys(owner)
      print('Done!')
    if option == '2':
      owner = input(
        'Enter the name of the person to this message goes to\n> ').lower()
      msg = input('Enter the message\n> ')
      keys = json.load(open(f'{owner}_key.json', 'r'))
      public = keys.get('public')
      modulos = keys.get('modulos')
      encrypted = encrypt(msg, public, modulos)
      print(f'The stream for the encrypted message is\n{", ".join(encrypted)}')
    if option == '3':
      owner = input(
        'Enter the name of the person of the message owner\n> ').lower()
      msg = input('Enter the strean of message encrypted\n> ').split(',')
      msg = map(lambda x: int(x.strip()), msg)
      keys = json.load(open(f'{owner}_key.json', 'r'))
      private = keys.get('private')
      modulos = keys.get('modulos')
      decrypted = decrypt(msg, private, modulos)
      print(decrypted)
    option = input('> ')
  print('Exit of Simulator')


if __name__ == "__main__":
  rsa()
