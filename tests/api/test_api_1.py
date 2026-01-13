from utils import textfile_utils

SharedVarsDict = {"userID": ""}
file_name = "shared_variables.txt"

user_name = "mytest"
password = "PjJR3Q@bfвfh"

def test_create_user(api):
    data = {
        "userName": user_name,
        "password": password
    }
    response = api.post("/Account/v1/User", data)
    assert response.status_code == 201
    assert "userID" in response.json()

    SharedVarsDict = textfile_utils.read_dict_from_text_file(file_name)
    SharedVarsDict['userID'] = response.json()["userID"]
    textfile_utils.save_dict_to_text_file(file_name, SharedVarsDict)


def test_delete_user(api):
    SharedVarsDict = textfile_utils.read_dict_from_text_file(file_name)
    api.login(user_name, password)
    response = api.delete(f"/Account/v1/User/{SharedVarsDict['userID']}")
    assert response.status_code == 204


