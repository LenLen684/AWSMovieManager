import json
import bcrypt

def lambda_handler(event, context):
    print("event : ",event)
    method_type = event['httpMethod']
    response = ""
    if method_type == "POST":
        response = create(event)
    elif method_type == "DELETE":
        response = delete(event)
    elif method_type == "PUT":
        response = update(event)
    elif method_type == "GET":
        response = get(event)
    
    # printing for test purposes
    for x in get_users():
        print(x)

    if (response != ""):
        return{
            'statusCode': 200,
            'headers' : {'Content-Type': 'application/json'},
            'body' : json.dumps(response),
            'isBase64Encoded' : False,
            'multiValueHeaders' : {'Content-Type': ['application/json']}
        }
    else:
        return{
            'statusCode': 400,
            'headers' : {'Content-Type': 'application/json'},
            'body' : json.dumps("Bad Request"),
            'isBase64Encoded' : False,
            'multiValueHeaders' : {'Content-Type': ['application/json']}
        }


def create(event):
    params = event["headers"]
    if(params == None):
        return ""
    result = ""
    if(params.keys() >={"username","email","password","rank"}):
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(params["password"],salt)
        user = {
            "id": len(get_users())+1,
            "username":params["username"],
            "email": params["email"],
            "password":  password,
            "rank": params["rank"]
        }
        
        # Add to the in memory list

        result = {"Result" : "User created successfully",
                "User" : user}
    return result

def update(event):
    params = event["header"]
    if(params == None):
        return ""
    if (params.keys() >= {"id", "password"}):
        old_user = get(params["id"])
        salt = bcrypt.gensalt()
        new_password = bcrypt.hashpw(params["password"],salt)
        new_user = {
            "id": old_user["id"],
            "username": params["username"] if("username" in params) else old_user["username"],
            "email": params["email"] if("email" in params) else old_user["email"],
            "password": new_password,
            "rank": params["rank"] if("rank" in params) else old_user["rank"]
        }

        # I have to change this later when I need to update the database
        update_db(new_user)
        return {"Result": "Update Successful",
                "Old User": old_user,
                "New User": get(params["id"])}
    else:
        return ""
    
def delete(event):
    if(event == None):
        return ""
    # assuming I've already authenticated the account delete
    if("id" in event):
        for i in range(len(data)):
            if int(event["id"]) == data[i]["id"]:
                data.pop(i)
                return {"Result" : "Delete successful"}
    return ""

def get(id):
    found = False
    data = get_users()
    if(id == None):
        return data
    else:
        idnum = int(id)
        for i in range(len(data)):
            if("id" in data[i]):
                if data[i]["id"] == idnum:
                    found = True
                    return data[i]
        if(not found):
            return ""
    return data
    
# Figuring out a way to update without duplicates
# def duplicate_check(old, new):
#     for x in old:
#         for y in new:
#             if(x == y):
#                 new.remove(y)
#     return old + new


def get_users():
    return data

def update_db(item):
    delete(item)
    data.append(item)

#In Memory stuff from local
# with open('UserData.json') as file:
#     data = json.load(file)
data =[{
    "id": 0,
    "username":"Tester 0",
    "email": "johnny@apple.seed",
    "password": "pass", 
    "rank": "admin"
    }]