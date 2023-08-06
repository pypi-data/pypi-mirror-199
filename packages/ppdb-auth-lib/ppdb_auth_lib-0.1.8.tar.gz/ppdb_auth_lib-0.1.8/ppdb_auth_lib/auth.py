from datetime import datetime, timedelta
from enum import Enum

import jwt
from pydantic import BaseModel
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from starlette import status
from bson.objectid import ObjectId


from config.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, PRIVATE_SIGNATURE, BASE_URL_FE, BASE_URL

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Sesi telah berakhir, silahkan login kembali!",
    headers={"WWW-Authenticate": "Bearer"},
)
ROLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User tidak memiliki akses",
    headers={"WWW-Authenticate": "Bearer"},
)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{BASE_URL}ppdb/v2/auth/all/login"
)

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if type(v) == str:
            v = ObjectId(v)
        if not isinstance(v, ObjectId):
            raise ValueError("Object ID tidak valid")
        return str(v)


class JwtToken(BaseModel):
    name: str = None
    username: str = None
    email: str = None
    school_id: ObjectIdStr = None
    ppdb_id: ObjectIdStr = None
    user_id: ObjectIdStr = None
    role: str = None
    exp: int = None


class RoleType(str, Enum):
    ADMIN_SCHOOL = "ADMIN_SCHOOL"
    ADMIN_FINANCE = "ADMIN_FINANCE"
    ADMIN_SELECTION = "ADMIN_SELECTION"
    STUDENT = "STUDENT"
    SUPER_ADMIN = "SUPER_ADMIN"


def create_access_token(data: JwtToken, expires_delta: int):
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data.exp = expire
    encoded_jwt = jwt.encode(data.dict(), JWT_SECRET_KEY, JWT_ALGORITHM)

    return encoded_jwt


def get_current_user_data(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        data_token = JwtToken(
            name=payload.get("name"),
            username=payload.get("username"),
            email=payload.get("email"),
            school_id=str(payload.get("school_id")),
            ppdb_id=str(payload.get("ppdb_id")),
            user_id=str(payload.get("user_id")),
            role=payload.get("role"),
            exp=payload.get("exp")
        )
        data_token.role = str(data_token.role).replace(" ", "_")
        if str(security_scopes.scopes[0]).lower() == "*":
            print("Semua Role memiliki akases")
        elif RoleType[data_token.role] in security_scopes.scopes:
            print(f"Role {str(data_token.role).upper()} memiliki akases")
        elif RoleType[data_token.role] not in security_scopes.scopes:
            raise ROLE_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION
    return data_token


async def get_current_token_data(token: str = Depends(oauth2_scheme)):
    return token


async def create_refresh_token(response, token):
    try:
        payload = jwt.decode(token["access_token"], JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        data_token = JwtToken()
        data_token.name = payload.get("name"),
        data_token.username = payload.get("username"),
        data_token.email = payload.get("email"),
        data_token.school_id = str(payload.get("school_id")),
        data_token.ppdb_id = str(payload.get("ppdb_id")),
        data_token.user_id = str(payload.get("user_id")),
        data_token.role = payload.get("role")

        # cek token sekarang masih on atau gak
        if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
            # cek username masih ada atau tidak
            # if(await GetUserOr404ByUsername(payload.get("username"))):
            access_token = create_access_token(data_token, ACCESS_TOKEN_EXPIRE_MINUTES)
            # print(access_token)
            btoken = "Bearer " + str(access_token)
            response.headers["Authorization"] = btoken
            return {"access_token": access_token}

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


async def verify_private_endpoint_data(request_client: Request):
    header_signature = request_client.headers.get("X-TKI-Signature")
    if header_signature != PRIVATE_SIGNATURE:
        raise ROLE_EXCEPTION
