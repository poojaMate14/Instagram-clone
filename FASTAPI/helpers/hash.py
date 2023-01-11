from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash:
    @staticmethod
    def bcrypt(plain_password: str):
        return pwd_cxt.hash(plain_password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)