
# Python code to merge dict using a single
# expression
def merge_dicts(dict1, dict2):
    res = {**dict1, **dict2}
    print("+-------------------------------+")
    print("merged dictionary", res)
    print("+-------------------------------+")
    return res
