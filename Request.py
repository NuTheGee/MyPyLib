import http.client, urllib.parse
import json

import Time

def MakeURL(host, path, query={}, tls=False):
    url = "https://" if tls else "http://"
    url += host + path
    if query != {}:
        url += "?" + urllib.parse.urlencode(query)
    return url

def MakeBody(query, header):
    if "Content-Type" in header.keys():
        content_type = header["Content-Type"].split(";")
        encoding = content_type[1].split("=")[1] if len(content_type) > 1 and "charset" in content_type[1] else "utf-8"
        if content_type[0] == "application/x-www-form-urlencoded":
            body = urllib.parse.urlencode(query).encode(encoding)
        elif content_type[0] == "application/json":
            body = json.dumps(query).encode(encoding)
    else:
        header["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
        body = urllib.parse.urlencode(query).encode("utf-8")
    return body

def Request(url, body=None, header={}):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(parsed_url.netloc)
    else:
        conn = http.client.HTTPConnection(parsed_url.netloc)
    path_query = parsed_url.path
    if parsed_url.query != "":
        path_query += "?" + parsed_url.query
    method = "GET" if body == None else "POST"
    conn.request(method, path_query, body, header)
    print("{} Request Start: {}".format(Time.GetTime(), url))
    resp = conn.getresponse()
    resp_header = resp.getheaders()
    resp_body = resp.read()
    conn.close()
    print("{} Request End: {}, {} Bytes".format(Time.GetTime(), resp.status, len(resp_body)))
    return (resp_header, resp_body)

def Download(url, folder="./", file_name=None):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme == "https":
        conn = http.client.HTTPSConnection(parsed_url.netloc)
    else:
        conn = http.client.HTTPConnection(parsed_url.netloc)
    path_query = parsed_url.path
    if parsed_url.query != "":
        path_query += "?" + parsed_url.query
    method = "GET"
    conn.request(method, path_query, None, {})
    print("{} Request Start: {}".format(GetTime(), url))
    resp = conn.getresponse()
    resp_header = resp.getheaders()
    resp_body = resp.read()
    conn.close()
    print("{} Request End: {}, {}Bytes".format(Time.GetTime(), resp.status, len(resp_body)))

    file_path = folder + parsed_url.path.split("/")[-1] if file_name == None else foldr + file_name
    with open(file_path, "wb") as f:
        print("{} File Write Start: {}".format(Time.GetTime(), file_path))
        f.write(resp_body)
        print("{} File Write End: {} Bytes".format(Time.GetTime(), len(resp_body)))
    return resp_header