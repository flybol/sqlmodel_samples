
from sqlmodel import SQLModel,Field,Relationship
from pydantic import SecretStr
class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class TeamPublic(TeamBase):
    id: int



class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None
    # 注意我们可以在 HeroBase 中声明 team_id，因为它可以被所有模型重用，在所有情况下它都是可选的整数。
    team_id: int | None = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    team: Team | None = Relationship(back_populates="heroes")

class HeroCreate(HeroBase):
    password: str

def hash_password(password: str) -> str:
    # Use something like passlib here
    return f"not really hashed {password} hehehe"

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: SecretStr | None = Field(default=None, description="登录密码", exclude=True)

    def to_update_model(self):
        """生成可以直接用于 sqlmodel_update 的字典"""
        data = self.model_dump(exclude_unset=True)
        # 如果传了密码，就把它转换成 hashed_password
        if self.password is not None:
            raw_pwd = self.password.get_secret_value()
            data.pop("password", None)  # 不让明文密码进入数据库
            data.update(hashed_password=hash_password(raw_pwd))
        print("更新数据：", data)
        return data

class HeroPublic(HeroBase):
    id: int


class HeroPublicWithTeam(HeroPublic):
    team:TeamPublic|None = None

class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []