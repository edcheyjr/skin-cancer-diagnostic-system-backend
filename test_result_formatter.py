# color code the tick emoji the test result in the terminal
def color_test_result(test_result):
    if test_result == 1:
        return '\033[32m' + 'passed ✅' + '\033[0m'
    elif test_result == 0:
        return '\033[31m' + 'failed ❌' + '\033[0m'
    else:
        return test_result
