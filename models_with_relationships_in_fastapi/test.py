from pydantic import BaseModel, SecretStr
data = {"username":"user1","password":"<PASSWORD>"}
data.pop("password",None)
print(data)

class UserCreate(BaseModel):
    username: str
    password: SecretStr


user = UserCreate(username="alice", password="123456")

print(user)
# UserCreate( username='alice', password=SecretStr('**********'))