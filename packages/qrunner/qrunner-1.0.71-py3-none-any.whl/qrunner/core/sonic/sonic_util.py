import requests

from qrunner.utils.config import config


class SonicUtil:
    """sonic远程交互"""

    def __init__(self, host, username, password):
        # 进行登录，获取SonicToken
        payload = {"userName": username, "password": password}
        res = requests.post(host + '/api/controller/users/login', json=payload)
        sonic_token = res.json().get('data')
        self.headers = {"SonicToken": sonic_token}


if __name__ == '__main__':
    sonic_host = config.get_sonic('host')
    sonic_username = config.get_sonic('username')
    sonic_password = config.get_sonic('password')
    sonic = SonicUtil(sonic_host, sonic_username, sonic_password)

