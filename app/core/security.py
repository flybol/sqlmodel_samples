from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    """验证密码"""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(raw_password: str):
    """密码加密"""
    return password_hash.hash(raw_password)
