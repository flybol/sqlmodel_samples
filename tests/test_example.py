def inc(x):return x + 1

def test_inc():
    assert inc(3) == 4

    
def f():
    raise SystemExit(1)

import pytest
def test_mytest():
    with pytest.raises(SystemExit):
        f()


import pytest


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()
# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)

@pytest.fixture
def user():
    return {"username": "john","role":"admin"}

def test_user_role(user): #测试函数参数同名即请求该 fixture。
    assert user["role"] == "admin","User role is not admin"


