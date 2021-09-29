#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2021/9/26 19:01
# @Author  : Qu Yuan
# @Site    :
# @File    : SFTPManager.py
# @Software: PyCharm

import paramiko
import os
import configparser

class SFTPManagerInstance:
    def __init__(self, sf, ssh2_client):
        self.sf = sf
        self.ssh2_client = ssh2_client

class SFTPManager:
    def __init__(self, config_path, section):
        self.config = config_path
        self.section = section

    def sftp_download_one_file(self, sftp_manager_instance, local_dir, remote_dir, remote_file_name, local_file_name):
        """

        :param sftp_manager_instance: sftp实例
        :param local_dir: 本地路径
        :param remote_dir: 远端路基
        :param remote_file_name: 远端文件名
        :param local_file_name: 本地新文件名
        :return:
        """
        # print('调用下载任务')
        try:
            if os.path.isdir(local_dir):  # 判断本地参数是目录还是文件
                remote_path = os.path.join(remote_dir, remote_file_name)
                local_path = os.path.join(local_dir, local_file_name)
                sftp_manager_instance.ssh2_client.get(remote_path, local_path)
                return True
            else:
                return False
        except Exception as e:
            print('下载出错： ', e)

    def get_all_files_name(self, sftp_manager_instance, remote_dir):
        """

        :param sftp_manager_instance: sftp实例
        :param remote_dir: 远端路径
        :return: 所有文件列表
        """
        return sftp_manager_instance.ssh2_client.listdir(remote_dir)

    # def sftp_download_files(self, sftp_manager_instance, local_dir, remote_dir, remote_file_name_list, local_file_name_list):
    #     """
    #
    #     :param sf: ssh_client对象
    #     :param local_dir: 本地路径
    #     :param remote_dir: 远端路径
    #     :param remote_file_name_query: 远端文件名模糊查询对象
    #     :param local_file_name: 本地新文件名
    #     :return:
    #     """
    #     try:
    #         if os.path.isdir(local_dir):  # 判断本地参数是目录还是文件
    #
    #             for file in remote_file_name_list:
    #                 remote_path = os.path.join(remote_dir, file)
    #                 #如果本地文件名为None，则使用不改名下载
    #                 if local_file_name_list is None:
    #                     local_path = os.path.join(local_dir, file)
    #                 else:
    #                     for local_name in local_file_name_list:
    #                         local_path = os.path.join(local_dir, local_name)
    #                         sftp_manager_instance.ssh2_client.get(remote_path, local_path)
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         print('下载出错： ', e)


    def get_config(self):
        """
        获取配置文件信息
        :return: 配置文件类
        """
        config = configparser.ConfigParser()
        config.read(self.config, encoding='UTF-8-sig')
        return config

    def sftp_connect(self, host, port, username, password):
        """

        :param port: 端口号
        :param username: 用户名
        :param password: 密码
        :return: sftp对象
        """
        sf = paramiko.Transport((host, port))
        sf.banner_timeout = 600
        sf.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(sf)
        sftp_manager_instance = SFTPManagerInstance(sf, sftp)
        return sftp_manager_instance

    def sftp_close(self, sftp_manager_instance):
        sftp_manager_instance.sf.close()
