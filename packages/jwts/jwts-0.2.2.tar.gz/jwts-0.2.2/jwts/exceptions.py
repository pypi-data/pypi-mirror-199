class JWTException(Exception):
    pass


class JWTDecodeException(JWTException):
    pass


class JWTEncodeException(JWTException):
    pass
