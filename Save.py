import json
import Time

def JSON(data, file_name, directory="./"):
    file_path = directory + file_name + ".json"
    with open(file_path, "wt") as f:
        print("{} File Write Start: {}".format(Time.GetTime(), file_path))
        content = json.dumps(data, ensure_ascii=False)
        f.write(content)
        print("{} File Write End: {} Bytes".format(Time.GetTime(), len(content)))
    return