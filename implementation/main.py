import os
import rsaProcess

START_PAGE = """
  Implementation of RSA cryptographic algorithm using the Python package cryptography
  Code developet by
  Julio Quintero
  Andres Aponte
  
"""

OPTIONS = """
Select an option
  [1] Read Messages
  [2] Send Message
  [enter] exit
> """


def list_users():
  return set(map(lambda x: x.split('_')[0], os.listdir('./keys')))


if __name__ == '__main__':
  print(START_PAGE)
  owner = input('Enter your name: ').capitalize()
  option = ' '
  while option != '':
    option = input(OPTIONS)
    while option not in ['1', '2', '']:
      print(f'Error! {option} is not a valid option')
      option = input(OPTIONS)
    if option == '1':
      password = input('Enter the password of you private key\n> ')
      rsaProcess.decryption(owner, msg_path='./messages', password=password)
    if option == '2':
      current_keys = list_users()
      print('Plesa insert the name of the user who is the message to')
      for index, user in enumerate(current_keys, start=1):
        print(f'[{index}] {user}')
      user = input('> ').capitalize()
      rsaProcess.encryption(user, file_path='message.txt')
      print('Message send')
