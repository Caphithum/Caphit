import re

def check_identify_code(code):
    """
    判断身份证号码是否合法
    :param code: 身份证号码，字符串类型
    :return: 布尔值，True表示合法，False表示不合法
    """
    if len(code) == 18:
        if re.match(r"(^\d{15}$)|(^\d{17}([0-9]|X)$)", code):
            return True
        else:
            return False
    else:
        return False


identify_code = input("请输入身份证号：")
if check_identify_code(identify_code):
    print("身份证号码合法！")
else:
    print("身份证号码不合法！")