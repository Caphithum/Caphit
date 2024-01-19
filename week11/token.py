import requests

# 请替换为你自己的个人访问令牌
token = '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'

# 构建API请求的URL
url = 'https://api.github.com/user/repos'

# 添加个人访问令牌到请求头部
headers = {
    'Authorization': f'token {token}'
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应是否成功
if response.status_code == 200:
    # 解析响应的JSON数据
    repos = response.json()

    # 打印仓库名
    for repo in repos:
        print(repo['name'])
else:
    print(f"API请求失败,状态码: {response.status_code}")