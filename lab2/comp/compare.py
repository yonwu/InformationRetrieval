import json


def find_all_keys(file):
    with open(file, 'r') as f:
        rapps = json.loads(f.read())
        all_keys = list()
        for rapp in rapps:
            for key in rapp.keys():
                all_keys.append(key)
        return sorted(all_keys)


def find_all_rapps(file):
    with open(file, 'r') as f:
        rapps = json.loads(f.read())
        all_rapps= list()
        for rapp in rapps:
            for key in rapp.keys():
                if key == "serviceName":
                    all_rapps.append(rapp[key])
        return sorted(all_rapps)


if __name__ == "__main__":

    target_keys = find_all_keys('target.json')
    result_keys = find_all_keys('result.json')
    print(target_keys)
    print(result_keys)

    if target_keys == result_keys:
        print("equal")

    target_rapps = find_all_rapps('target.json')
    result_rapps = find_all_rapps('result.json')
    print(target_rapps)
    print(result_rapps)

    if target_rapps == result_rapps:
        print("equal")

