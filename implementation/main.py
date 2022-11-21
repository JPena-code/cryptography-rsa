from keyManagment import key_gen
import rsaProcess

if __name__ == '__main__':
  # key_gen('Julio', path='./', password='prueba')
  # key_gen('Julio', password='prueba')
  # rsaProcess.encryption('Julio', file_path='./prueba.txt')
  rsaProcess.decryption('Julio', msg_path='./messages', password='prueba')
  print('Funciona')