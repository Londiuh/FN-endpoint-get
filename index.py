import requests
from base64 import b64encode
import json
import random
import string

class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m" 
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

token = None

def getToken():
    global token
    if token != None:
        print(color.GREEN + "Token already generated, auth code not requiered" + color.END)
        return token
    print(color.PURPLE + "Insert auth code:" + color.END)
    authCode = input()
    id_secret = "ec684b8c687f479fadea3cb2ad83f5c6:e1f31c211f28413186262d37a13fc84d"
    h = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"basic {str(b64encode(id_secret.encode('utf-8')), 'utf-8')}"
    }
    b = {
            "grant_type": "authorization_code",
            "code": authCode
    }
    r = requests.post("https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token", headers=h, data=b)
    #print(r.text)
    r = json.loads(r.text)
    if "access_token" in r:
        token = r["access_token"]
        print(color.GREEN + f"Token: {token}\nExpires at: {r['expires_at']}" + color.END)
        return token
    else:
        if "errorCode" in r:
            print(color.RED + f"[ERROR] {r['errorCode']}" + color.END)
        else:
            print(color.RED + "[ERROR] Unknown error" + color.END)
        return False

def getEndpoint():
    getToken_result = getToken()
    if getToken_result:
        print(color.PURPLE + "Insert endpoint:" + color.END)
        endpoint = input()
        if endpoint.lower().find("epicgames.com") != -1:
            try:
                h = {"Authorization": f"bearer {getToken_result}"}
                r = requests.get(endpoint, headers=h)
                print(r.text)
                print(color.CYAN + "Do you want to save the response into a json file? " + color.GREEN + "Y | N" + color.END)
                saveFile = input()
                if saveFile.lower() == "y" or saveFile.lower() == "yes":
                    random_name = "".join(random.choice(string.ascii_lowercase) for i in range(5))
                    with open(f"{random_name}.json", "x") as f:
                        try:
                            f.write(r.text)
                            print(color.YELLOW + f"File successfully saved (./{random_name}.json)" + color.END)
                        except Exception as e:
                            print(color.RED + f"[ERROR] Couldn't save the file ({e})" + color.END)
            except:
                print(color.RED + "[ERROR] Something went wrong :(" + color.END)
        else:
            print(color.RED + "[ERROR] Invalid endpoint, insert a valid Fortnite endpoint" + color.END)
    getEndpoint()

getEndpoint()
