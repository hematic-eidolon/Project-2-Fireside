import hashlib  # NOQA
import tty
import sys
import termios


class authenticator:

  def __init__(self) -> None:
    self.passwordHash = b"P\xa6\x82ic\xbc\xeb\x93\xcc\xbf\tA\x07B\x19E\x9bl\xcfJ\xd7\x12\xac\xcc\xcd\xea\xaa\x8d'\x85P\xf5"

  def checkPassword(self, passwordToValidate: str) -> bool:
    inputHash = hashlib.sha256(passwordToValidate.encode()).digest()
    return inputHash == self.passwordHash

  def getPassword(self):
    password = ''
    sys.stdout.write("Password: ")
    sys.stdout.flush()
    oldTerminal = termios.tcgetattr(sys.stdin)
    try:
      tty.setcbreak(sys.stdin.fileno())
      while True:
        char = sys.stdin.read(1)
        if char == '\r' or char == '\n':
          sys.stdout.write('\n')
          return password
        elif char == '\x7f' and password:
          password = password[:-1]
          sys.stdout.write('\b \b')  # backspace clause
        else:
          password += char
          sys.stdout.write('*')
        sys.stdout.flush()
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldTerminal)

  def getPasswordAndAuthenticate(self):
    return self.checkPassword(self.getPassword())

def returnHash(strIn: str):
  return hashlib.sha256(strIn.encode()).digest()

def checkPass(correctHash, inputstring):
  return returnHash(inputstring) == correctHash