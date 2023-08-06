# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 9:23:56
# @Author  : Pane Li
# @File    : inrequest.py
"""
封装request， 使设备和平台都能来正常调用，统一入口，token过期时也能自动更新

"""
import base64
import logging
import os
import re
import sys
import time
import urllib3
import requests
from inhandtest.exception import ParameterValueError, UsernameOrPasswordError, TimeOutError, UpgradeFailedError, \
    ResourceNotFoundError
from inhandtest.file import file_hash
from inhandtest.tools import dict_in, dict_merge


class DmInterface:

    def __init__(self, username, password, platform='china'):
        """
        :param username  平台用户名
        :param password  平台密码
        :param platform: 'china'|'global' 平台是哪个环境,china国内 global 国际平台
        """
        self.platform = platform
        self.host = 'iot.inhand.com.cn' if platform == 'china' else 'iot.inhandnetworks.com'
        self.username = username
        self.api = InRequest(self.host, username, password, 'iot')

    def device_exist(self, sn: str, timeout=120, interval=5):
        """检查设备在平台账号下存在，如果超时都不存在就抛异常

        :param sn:
        :param timeout:
        :param interval:
        :return:
        """
        for i in range(0, timeout, interval):
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn})
            if response.json().get('total') == 1:
                logging.info(f'check {sn} device exist')
                break
            logging.info(f'check {sn} device is not exist, please wait for {interval}s')
            time.sleep(interval)
        else:
            raise TimeOutError(f'{self.host} {self.username} account not found device {sn}')

    def device_state(self, sn: list) -> list:
        """根据sn 转换属性 属性值有：  online: 在线|离线   1|0
                                       iccid:
                                       imei:
                                       imsi:
                                       version: 固件版本
                                       hwVersion: 硬件版本 'V1.0'
                                       bootVersion:  Bootloader版本  '1.1.3.r4956'
                                       sn: 序列号
                                       address
                                       id: 设备id
        :param sn: 列表
        :return: [{'sn': $sn, 'online': 1, 'iccid': '', 'imei'}]
        """
        result = []
        for sn_ in sn:
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn_}).json()
            if response.get('total') == 1:
                res = response.get('result')[0]
                result.append(
                    {'sn': sn_, 'online': res.get('online'), 'iccid': res.get('info').get('iccid'),
                     'imei': res.get('info').get('imei'), 'imsi': res.get('info').get('imsi'),
                     'version': res.get('info').get('swVersion'), 'hwVersion': res.get('info').get('hwVersion'),
                     'bootVersion': res.get('info').get('bootVersion'), 'address': res.get('address'),
                     'id': res.get('_id')})
            else:
                result.append(
                    {'sn': sn_, 'online': None, 'iccid': None, 'imei': None, 'imsi': None, 'swVersion': None,
                     'hwVersion': None, 'bootVersion': None, 'address': None, 'id': None})
        return result

    def add_device(self, sn: str):
        """添加设备，

        :param sn: 设备序列号
        :return:
        """
        while True:
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn})
            if response.json().get('total') == 0:
                self.api.send_request('api/devices', 'post',
                                      body={"name": sn + str(int(time.time())), "serialNumber": sn})
                logging.info(f"the {sn} device add success")
            else:
                break

    def assert_device_state(self, sn: str, state: dict, timeout=120, interval=5):
        """校验设备基本状态

        :param sn: 序列号
        :param state:
                        online: 在线|离线   1|0
                        iccid:
                        imei:
                        imsi:
                        version: 固件版本
                        hwVersion: 硬件版本 'V1.0'
                        bootVersion:  Bootloader版本  '1.1.3.r4956'
                        sn: 序列号
                        address
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :return: True or False
        """
        if state:
            for i in range(0, timeout, interval):
                result = self.device_state([sn])[0]
                for key, value in state.items():
                    if result.get(key) != value:
                        logging.info(f'the {sn} device {key} info value is {result.get(key)} not {value}')
                        break
                else:
                    logging.info(f"check {sn} device all state success")
                    break
                logging.info(f"check {sn} device state failed, please wait for {interval}s")
                time.sleep(interval)
            else:
                raise TimeOutError(f"the {sn} state {state} check failed")

    def send_config_online(self, sn: str or list, config: str):
        """下发配置， 多台时仍然是一台一台下发的， 注意逻辑 设备必须是在线的才能下发

        :param config: 配置命令，多个配置用'\n'隔开
        :param sn: 一台设备或多台设备
        :return: list 返回未成功下发配置的设备
        """
        body = {
            "deviceType": 0,
            "deviceContent": config,
            "deviceDesc": 'set running config'
        }
        sn = [sn] if isinstance(sn, str) else sn
        not_send_sn = []
        for sn_ in sn:
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn_})
            if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
                device_id = response.json().get('result')[0].get('_id')
                logging.info(f'the {sn_} device send config')
                self.api.send_request(f'/api/devices/{device_id}/config/set', 'post', param={'timeout': 30},
                                      body=body).json()
            else:
                not_send_sn.append(sn_)
                logging.error(f'the {sn} device not exist or offline, not send config')
        return not_send_sn

    def get_config_online(self, sn: str, config: str = None):
        """平台获取配置 设备需要在线

        :param sn: 序列号
        :param config: 对获取到的配置做校验 多条配置使用'\n'隔开， 为None时仅获取
        """
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            device_name = response.json().get('result')[0].get('name')
            task_state = self.api.send_request('api2/tasks/run', 'post',
                                               body={'name': "GET RUNNING CONFIG", 'objectId': device_id,
                                                     'priority': 30, 'objectName': device_name, 'timeout': 30000,
                                                     'type': "4"}).json().get('result').get('state')
            assert task_state == 3, "GET RUNNING CONFIG task status error!"
            config_content = self.api.send_request(f'api/devices/{device_id}/config', 'get').json().get('result').get(
                'content')
            if config:
                assert set(config.split('\n')).issubset(set(config_content.split('\n'))), f'config {config} not exist'
        else:
            raise ResourceNotFoundError(f'the {sn} device not exist or offline')

    def upgrade_firmware_online(self, sn: str, firmware: str, timeout=10 * 60, interval=10):
        """ 升级固件， 保障升级成功不然就会报错

        :param sn: 设备序列号
        :param firmware: 升级的固件，本地全路径
        :param timeout: 下发升级任务后，总体的升级超时时间， 单位秒 至少5分鐘
        :param interval: 升级任务检测间隔， 单位秒
        :return None or TimeOutError， 升级失败就报TimeOutError
        """

        def model(name):
            models = self.api.send_request('api/models', 'get',
                                           {'gateway': True, 'verbose': 100, 'limit': 0}).json().get('result')
            for model_ in models:
                if len(re.findall(model_.get('firmwareNamePattern'), name)) == 1:
                    return model_.get('name')

        def version(name):
            return 'V' + re.findall('V(.*).bin', name)[0]

        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1:
            device_id = response.json().get('result')[0].get('_id')
            device_name = response.json().get('result')[0].get('name')
            old_version = response.json().get('result')[0].get('info').get('swVersion')
            file_name = os.path.basename(firmware)
            if os.path.isfile(firmware) and old_version not in file_name:  # 确定版本不一样才升级撒，不然浪费资源
                get_firmware = self.api.send_request('api/firmware', 'get', {'name': file_name}).json()
                if get_firmware.get('total') == 0:
                    if os.path.exists(firmware):
                        param = {'filename': firmware, 'oid': 'undefined'}
                        upload_file = self.api.send_request('api/file/form', method='post', param=param,
                                                            params_type='form', file_path=firmware).json().get('result')
                        body = {'fid': upload_file['_id'], 'jobTimeout': 30, 'model': model(file_name),
                                'name': file_name,
                                'version': version(file_name), 'desc': 'auto test upload firmware'}
                        firmware_id = self.api.send_request('api/firmware', 'post', body=body, ).json().get(
                            'result').get(
                            '_id')
                    else:
                        raise FileNotFoundError(f'{firmware} not exist')
                else:
                    logging.info(f'This file {firmware} already exists on the cloud {self.host} {self.username}')
                    firmware_id = get_firmware.get('result')[0].get('_id')
                # 已完成固件上传
                job_id = self.api.send_request(f'api/device/{device_id}/upgrade', method='post',
                                               body={'deviceName': device_name, 'firmwareId': firmware_id,
                                                     'timeout': int(timeout / 60)}).json().get('result').get('_id')
                for i in range(0, timeout, interval):
                    time.sleep(interval)
                    job_response = self.api.send_request(f'/api2/tasks', method='get',
                                                         param={"verbose": 50, 'types': 6, 'object_id': device_id,
                                                                'limit': 100, 'cursor': 0}).json().get('result')
                    job = [job for job in job_response if job.get('_id') == job_id]
                    if len(job) == 1:
                        if job[0].get('_id') == job_id:
                            if job[0].get('state') == 3:
                                logging.info(f"upgrade to {file_name} success!")
                                break
                            elif job[0].get('state') == -1:
                                raise UpgradeFailedError(f'upgrade to {file_name} failed!')
                    else:
                        raise UpgradeFailedError('create upgrade task failed!')
                else:
                    raise TimeOutError('upgrade job check timeout')
            else:
                logging.info(f'{firmware} not is file or version of same ')

    def upgrade_firmware(self, sn: str or list, firmware: str):
        """ 升级固件，只管下发升级任务，不监督是否升级成功

        :param sn: 设备序列号
        :param firmware: 升级的固件，本地全路径
        :return None
        """

        def model(name):
            models = self.api.send_request('api/models', 'get',
                                           {'gateway': True, 'verbose': 100, 'limit': 0}).json().get('result')
            for model_ in models:
                if len(re.findall(model_.get('firmwareNamePattern'), name)) == 1:
                    return model_.get('name')

        def version(name):
            return 'V' + re.findall('V(.*).bin', name)[0]

        sn = [sn] if isinstance(sn, str) else sn
        devices = list(filter(lambda x: x.get('id'), self.device_state(sn)))
        if os.path.isfile(firmware) and devices:
            file_name = os.path.basename(firmware)
            get_firmware = self.api.send_request('api/firmware', 'get', {'name': file_name}).json()
            if get_firmware.get('total') == 0:
                if os.path.exists(firmware):
                    param = {'filename': firmware, 'oid': 'undefined'}
                    upload_file = self.api.send_request('api/file/form', method='post', param=param,
                                                        params_type='form', file_path=firmware).json().get('result')
                    body = {'fid': upload_file['_id'], 'jobTimeout': 30, 'model': model(file_name),
                            'name': file_name,
                            'version': version(file_name), 'desc': 'auto test upload firmware'}
                    firmware_id = self.api.send_request('api/firmware', 'post', body=body, ).json().get(
                        'result').get(
                        '_id')
                else:
                    raise FileNotFoundError(f'{firmware} not exist')
            else:
                logging.info(f'This file {firmware} already exists on the cloud {self.host} {self.username}')
                firmware_id = get_firmware.get('result')[0].get('_id')
            self.api.send_request(f'api/firmware/{firmware_id}/devices', method='post',
                                  body={'deviceIds': [device.get('id') for device in devices], 'deviceGroupIds': [], })
        else:
            logging.info(f'{firmware} not is file or device is not exist')

    def web_remote_online(self, sn: str):
        """封装远程web访问方法

        :param sn: str, 设备序列号
        :return: 远程web管理链接
        """
        server = 'ngrok.iot.inhand.com.cn:4443' if self.platform == 'china' else 'iot.inhandnetworks.com:4443'
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            device_name = response.json().get('result')[0].get('name')
            body = {"priority": 30, "timeout": 20000, "objectId": device_id, "objectName": device_name,
                    "name": "ngrok connect", "type": "23", "data": {"server": server, "proto": 'http', "port": 80}}
            for i in range(0, 3):
                try:
                    ngrok = self.api.send_request('api2/tasks/run', method='post', body=body).json()
                    if ngrok["result"]["data"]["response"]:
                        return ngrok["result"]["data"]["response"]
                except Exception as e:
                    logging.error(f"ngrok request failed reason is {e}, try {i + 2} again")
            else:
                raise Exception(f'Device {sn} get ngrok failed.')
        else:
            raise ResourceNotFoundError(f'the {sn} is not exist or offline')

    def reboot_online(self, sn: str):
        """DM平台设备重启
        """
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            logging.info(f'{self.host} send to {sn} reboot command')
            status = self.api.send_request(f'api/device/{device_id}/methods', 'post',
                                           body={'method': "reboot", 'timeout': 15000}).json().get('status')
            assert status == 'succeeded', 'reboot error!'
        else:
            raise ResourceNotFoundError(f'the {sn} is not exist or offline')

    def remote_maintenance_online(self, sn: str, protocol='http', port=80, local_host='192.168.2.1', action='connect',
                                  timeout=60, interval=2):
        """封装dm远程维护方法

        :param sn，必须在线
        :param protocol: str, 本地主机服务的协议, 'http'| 'https'| 'tcp'
        :param port: str, 本地主机的端口
        :param local_host: str, 本地主机的ip地址
        :param action: str, 是否连接远程维护隧道, 'connect'| 'disconnect'| 'delete'| 当为connect 时如果隧道不存在则自动新增
        :param timeout: int, 获取远程维护连接的最大超时时间
        :param interval: int, 获取远程维护连接的间隔时间
        :return: 当action='connect'时返回远程维护连接
        """
        action_dict = {'connect': True, 'disconnect': False}
        online_device = list(filter(lambda x: x.get('online') == 1, self.device_state([sn])))
        device = list(filter(lambda x: x.get('id'), self.device_state([sn])))

        def find_tunnel(device_id_):
            tunnels_ = self.api.send_request('/api/touch/tunnels', method='get',
                                             param={'verbose': 100, 'device_id': device_id_}).json().get('result')
            if tunnels_:
                for tunnel_ in tunnels_:
                    if tunnel_.get('proto') == protocol and tunnel_.get('localPort') == port and tunnel_.get(
                            'localAddress'):
                        return tunnel_.get('_id')

        if device:
            device_id = device[0].get('id')
            add_tunnel_body = {'verbose': 100, 'proto': protocol, 'name': str(round(time.time() * 1000)),
                               'localAddress': local_host, 'localPort': port, 'deviceId': device_id}
            if action == 'connect' and device[0].get('online'):
                tunnel_id = find_tunnel(device_id)
                if not tunnel_id:
                    self.api.send_request('/api/touch/tunnels', method='post', body=add_tunnel_body).json()
                    tunnel = add_tunnel['result']
                    logging.info(f'Add tunnel success, tunnel name is {tunnel["name"]}, id is {tunnel["_id"]}')


            for i in range(0, timeout, interval):
                try:
                    tunnels = self.api.request_json(url.tunnels(), method='get',
                                                    param={'verbose': 100, 'device_id': self.device_id},
                                                    expect='result')
                    for tunnel_ in tunnels['result']:
                        if tunnel_['proto'] == protocol and tunnel_['localAddress'] == local_host and tunnel_[
                            'localPort'] == port:  # 目标隧道已存在则使用目标隧道
                            tunnel = tunnel_
                            logging.info(
                                f'This tunnel is already exist, tunnel name is {tunnel["name"]}, id is {tunnel["_id"]}')
                            break
                    else:  # 目标隧道不存在则新建目标隧道
                        add_tunnel = self.api.request_json(url.tunnels(), method='post', body=add_tunnel_body,
                                                           expect='result')
                        tunnel = add_tunnel['result']
                        logging.info(f'Add tunnel success, tunnel name is {tunnel["name"]}, id is {tunnel["_id"]}')
                    if tunnel and action:  # 判断是否已有目标隧道且传入action
                        if action == 'connect' or action == 'disconnect':
                            action_tunnel = self.api.request_json(url.tunnels(tunnel_id=tunnel["_id"], action=action),
                                                                  method='put', expect='result')
                            if action_tunnel['result']['connected'] == action_dict[action]:
                                logging.info(f'Tunnel {tunnel["name"]} {action} success.')
                                if action == 'connect':
                                    remote_url = action_tunnel['result']['publicUrl']
                                    return remote_url
                                else:
                                    break
                            else:
                                logging.info(
                                    f'status {action_tunnel["connected"]} mismatch with the action {action}, {interval}s try again.')
                        if action == 'delete':
                            delete_tunnel = self.api.request_json(url.tunnels(tunnel_id=tunnel["_id"], action=action),
                                                                  method='delete', expect='result')
                            logging.info(f'Delete tunnel {delete_tunnel["result"]["name"]} success.')
                            break
                    if tunnel and not action:
                        break
                    time.sleep(interval)
                except Exception as e:
                    logging.warning(f"reason is {e}, {interval}s try again")
                    time.sleep(interval)
            else:
                raise Exception(f'Device {self.sn} get remote_maintenance failed.')


class InRequest:

    def __init__(self, host: str, username: str, password: str, type_='device', protocol='https', port=443):
        """支持设备，平台登录及操作API, 自动识别地址

        :param host:  主机地址，如果是平台的就填写平台server，如果是设备就填写设备的地址
        :param username:  用户名
        :param password: 密码
        :param type_: device|iot|ics|star|iscada|iwos  区分平台和设备
        :param protocol: 协议，当前只支持http https
        :param port: 端口
        """
        self.protocol = protocol
        self.host = host
        self.username = username
        self.password = password
        self.headers = {}
        self.type_ = type_
        self.port = port
        self.__login()

    def __url_pre(self, path: str):
        """host+path

        :param path:  请求路径
        :return:
        """
        if path.startswith('/'):
            return self.protocol + '://' + self.host + ':' + str(self.port) + path
        else:
            return self.protocol + '://' + self.host + ':' + str(self.port) + '/' + path

    def __login(self):
        if self.type_ in ('iot', 'ics', 'iwos'):
            self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
            param = {
                'client_id': '17953450251798098136',
                'client_secret': '08E9EC6793345759456CB8BAE52615F3',
                'grant_type': 'password',
                'type': 'account',
                'autoLogin': 'true',
                'password_type': 2,
                'pwdType': 'pwd',
                "username": self.username,
                "password": file_hash(self.password)}
            response = self.send_request('/oauth2/access_token', method='post', param=param).json()
            self.headers = {'Authorization': 'Bearer ' + response['access_token']}
        elif self.type_ in ('iscada', 'star'):
            settings_url = '/api/v1/erlang/frontend/settings' if self.type_ == 'iscada' else '/api/v1/frontend/settings'
            res_setting = self.send_request(settings_url, 'get', expect='result').json()
            # erlang 登录地址不一样，需要重新指向
            authority = res_setting['result']['authProvider']['authority']
            protocol_re = self.protocol
            host_re = self.host
            self.protocol = authority.split('://')[0]
            self.host = authority.split('://')[-1]
            param = {
                'client_id': res_setting['result']['authProvider']['clientId'],
                'client_secret': res_setting['result']['authProvider']['clientSecret'],
                'grant_type': 'password',
                'scope': 'offline',
                "username": self.username,
                "password": self.password,
                # "type": 'account'
            }
            response = self.send_request('/oauth2/token', method='post', param=param, params_type='form')
            self.headers = {'Authorization': 'Bearer ' + response['access_token']}
            self.protocol = protocol_re
            self.host = host_re
        elif self.type_ == 'device':
            username_password = '%s:%s' % (self.username, self.password)
            base_auth = base64.b64encode(username_password.encode()).decode()
            self.headers = {'Authorization': 'Basic %s' % base_auth}
            resp = self.send_request('v1/user/login', 'post').json()
            self.headers['Authorization'] = 'Bearer ' + resp['results']['web_session']

    def send_request(self, path, method, param=None, body=None, expect=None, file_path=None,
                     params_type='json', header=None, code=200, auth=True):
        """封装http请求，根据请求方式及参数类型自动判断使用哪些参数来发送请求

        :param path: 请求路径
        :param method: 请求方法
        :param param: 请求中的参数,
        :param body: post请求中的body，当消息体为json时使用
        :param expect: 期望包含的结果
        :param file_path: 文件路径，用于文件上传或者下载文件
        :param params_type: 参数类型，用于post请求，参数值：form|json
        :param header: 请求头 只支持字典
        :param code: 验证返回code
        :param auth: 是否认证， 默认需要的
        :return:
        """
        header = dict_merge(self.headers, header) if auth else header
        urllib3.disable_warnings()  # 去除https warnings提示
        method = method.upper()
        params_type = params_type.upper()
        url = self.__url_pre(path)
        if method == 'GET':
            res = requests.get(url=url, params=param, headers=header, verify=False)
            if file_path:
                with open(file_path, 'w', encoding='UTF-8') as f:
                    f.write(res.text)
        elif method == 'POST':
            if params_type == 'FORM':
                if file_path:
                    if self.type_ == 'device':
                        files = {
                            'file': (
                                os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
                        res = requests.post(url, params=param, files=files, headers=header, verify=False)
                    else:
                        with open(file_path, 'rb') as f:
                            file_info = {"file": f}
                            res = requests.post(url, data=param, files=file_info, headers=header, verify=False)
                else:
                    res = requests.post(url=url, data=param, headers=header, verify=False)
            elif params_type == 'JSON':
                res = requests.post(url=url, params=param, json=body, headers=header, verify=False)
            else:
                res = requests.post(url=url, headers=header, verify=False)
        elif method == 'DELETE':
            if body:
                if params_type == 'JSON':
                    res = requests.delete(url, headers=header, json=body, verify=False)
                else:
                    res = requests.delete(url, headers=header, data=body, verify=False)
            else:
                res = requests.delete(url, params=param, headers=header, verify=False)
        elif method == 'PUT':
            if params_type == 'JSON':
                res = requests.put(url, json=body, params=param, headers=header, verify=False)
            else:
                res = requests.put(url, data=param, headers=header, verify=False)
        else:
            raise ParameterValueError(f"requests method {method} not support")
        logging.info(f'Requests Method:[{method}] Code: {res.status_code} URL: {url}, Param: {param}, Body: {body}')
        if res.status_code != 401:
            if self.type_ == 'device':
                if res.status_code == 404:
                    raise Exception('not support API login')
                if res.status_code == 200 and 'login' in path:
                    if 'error' in res.json().keys():
                        raise UsernameOrPasswordError
            res.encoding = 'utf-8'  # 如返回内容有中文的需要编码正确
            try:
                logging.info(f'Requests Response json is {res.json()}')
            except Exception:
                logging.warning(f'Requests Response json is None')
        else:
            # 当token过期时，统一重新登录后再次调API
            self.__login()
            res = self.send_request(path, method, param, body, expect, file_path, params_type, header, code)
        if code:
            assert res.status_code == code, '返回状态不一致'
        if expect:
            if isinstance(expect, list):
                if len(expect) > 0:
                    for i in expect:
                        if isinstance(i, str) or isinstance(i, int):
                            assert str(i) in res.text, f"Response text {res.text} Does not contain {i}"
                        elif isinstance(i, dict):
                            dict_in(res.json(), i)
            elif isinstance(expect, dict):
                dict_in(res.json(), expect)
            elif isinstance(expect, str) or isinstance(expect, int):
                assert str(expect) in res.text, f"Response text {res.text} Does not contain {expect}"
            else:
                raise ValueError('expect param type error！')
        return res


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, stream=sys.stdout)
    testApi = DmInterface('liwei@inhand.com.cn', '12345678')
    testApi.web_remote('RF3052213006490')
    # print(re.findall('V(.*).bin', 'IR9-V1.0.0.r10190.bin')[0])
    # # testApi.get_config_online('RF3052213006490', 'dhcpd_start=192.168.2.3')
    # # testApi.assert_device_state('RF3052213006491', state={'online': 0})
