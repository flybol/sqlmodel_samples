

def test_dict_pop():
    dict_data = {"username":"user1","password":"<PASSWORD>","addresses":["a","b"]}
    value1 = dict_data.pop("password",None)
    value2 = dict_data.pop("addresses",None)
    print(dict_data)