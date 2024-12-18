from fastapi import HTTPException

from db.exception.authorization import USER_EXIST, USER_DONT_EXIST, UNCORRECT_DATA


def authorization_service(authorization):
    async def auth_wrapper(*args, **kwargs):
        try:
            dict_tokens = await authorization(*args, **kwargs)
            return dict_tokens
        except USER_EXIST:
            raise HTTPException(400, detail="user exist")
        except USER_DONT_EXIST:
            raise HTTPException(400, detail="user not exist")
        except UNCORRECT_DATA:
            raise HTTPException(400, detail="uncorrect data")
    return auth_wrapper
