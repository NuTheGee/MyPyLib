import re, json
import Request, Parse


Host = "tamuctf.com"
TLS = True
USER = ""
PASSWORD = ""
HEADER = {}


def Login(username, password):
    path = "/"
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url)
    session_cookie = ""
    for item in resp_header:
        if item[0] == "Set-Cookie" and "session" in item[1]:
            session_cookie = item[1].split(";")[0]
    #print(session_cookie)
    csrf_nonce = ""
    match = re.findall("csrf_nonce = \"([0-9a-f]+?)\"", resp_body.decode("utf-8"))
    if len(match) > 0:
        csrf_nonce = match[0]
    #print(csrf_nonce)
    
    path = "/login"
    url = Request.MakeURL(Host, path, {}, TLS)
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": session_cookie,
    }
    query = {
        "name": username,
        "password": password,
        "nonce": csrf_nonce,
    }
    body = Request.MakeBody(query, header)
    (resp_header, resp_body) = Request.Request(url, body, header)
    for item in resp_header:
        if item[0] == "Set-Cookie" and "session" in item[1]:
            session_cookie = item[1].split(";")[0]
    #print(session_cookie)
    HEADER["cookie"] = session_cookie
    return

def ListChals():
    path = "/chals"
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url, None, HEADER)
    chals = json.loads(resp_body.decode("utf-8"))
    return chals

def ChalSolves():
    path = "/chals/solves"
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url, None, HEADER)
    solves = json.loads(resp_body.decode("utf-8"))
    return solves

def TeamSolves(num):
    path = "/solves/" + str(num)
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url, None, HEADER)
    solves = json.loads(resp_body.decode("utf-8"))
    return solves

def ScoreBoard():
    path = "/scores"
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url, None, HEADER)
    result = json.loads(resp_body.decode("utf-8"))
    return result
        
def DetailChal(num):
    path = "/chals/" + str(num)
    url = Request.MakeURL(Host, path, {}, TLS)
    (resp_header, resp_body) = Request.Request(url, None, HEADER)
    chal = json.loads(resp_body.decode("utf-8"))
    return chal