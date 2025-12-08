from typing import get_type_hints


def print_class_fields_with_mro(cls):
    print(f"MRO: {[c.__name__ for c in cls.mro()]}")
    print("-" * 40)

    for base in cls.mro():
        # 跳过最底层的 object
        if base is object:
            continue

        # Pydantic / SQLModel 一般也有自己的基类，你可以选择性跳过
        # if base is SQLModel:
        #     continue

        hints = get_type_hints(base, include_extras=True)
        if not hints:
            continue

        print(f"【{base.__name__}】 声明的字段：")
        for name, typ in hints.items():
            print(f"  - {name}: {typ}")
        print()


def test_extends_fields():
    from app.models.user_model import User

    # print(User.__fields__)
    print_class_fields_with_mro(User)
