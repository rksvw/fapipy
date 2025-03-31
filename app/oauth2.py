from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret Key
# Algorithm
# Expression Time


SECRET_KEY = "au4riojraofdj09q4uroiq4jrjqewijr0q34rj0q34jroiajfdlkvmlakfjlasdjfioeqoru4oquroijaklfaklf0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    ecoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return ecoded_jwt
