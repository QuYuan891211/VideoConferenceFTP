#!/usr/bin/env python

# encoding: utf-8

# @Time    : 2020/7/25 10:51
# @Author  : Qu Yuan
# @Site    : 
# @File    : VideoConferenceService.py
# @Software: PyCharm
import os
import FTPManager
import SFTPManager
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import RemoteFilenameQuery

global config_path
config_path = r'E:\projects\pycharm\VideoConference\Background\docs\VideoConferenceConfig.ini'
global section_ftp
section_ftp = 'FTP'
global section_local
section_local = 'LOCAL'


class VideoConferenceService:
    def __init__(self, config_path, section_ftp, section_local):
        self.ftp_Manager = FTPManager.FTPManager(config_path, section_ftp)
        self.sftp_Manager = SFTPManager.SFTPManager(config_path, section_ftp)
        self.config_path = config_path
        self.section_ftp = section_ftp
        self.section_local = section_local

        self.config = self.sftp_Manager.get_config()
        self.host = self.config.get(section_ftp, 'host')
        self.port = self.config.get(section_ftp, 'port')
        self.username = self.config.get(section_ftp, 'username')
        self.password = self.config.get(section_ftp, 'password')
        self.local_dir = self.config.get(section_local, 'dir')
        self.target_normal = self.config.get(section_ftp, 'target_normal')
        self.target_EC = self.config.get(section_ftp, 'target_EC')
        self.target_GFS = self.config.get(section_ftp, 'target_GFS')
        self.target_GRAPES = self.config.get(section_ftp, 'target_GRAPES')
        self.fileName_normal1 = self.config.get(section_ftp, 'fileName_normal1')
        self.fileName_normal2 = self.config.get(section_ftp, 'fileName_normal2')
        self.fileName_normal3 = self.config.get(section_ftp, 'fileName_normal3')
        self.fileName_normal4 = self.config.get(section_ftp, 'fileName_normal4')
        self.fileName_allCity = self.config.get(section_ftp, 'fileName_allCity')

        # 日志
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler('%slog.log' % self.local_dir)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def get_file_info(self):
        """
        获取数据信息列表
        :return file_infos: 数据信息列表
        """

        # 获取配置文件信息

        self.ftp_Manager.ftp_connect(self.host, self.username, self.password)

        # 获取时间
        # self.ftp_Manager.getCreateTime()
        file_infos = self.ftp_Manager.get_filename("", self.target)
        # for f in file_infos:
        #     print(f)
        return file_infos

    # 判断本地是否有此路径
    def check_file(self, local_dir):

        if not os.path.exists(local_dir):
            return False
        else:
            # 读入文件
            return True
            # for f in files:

    def upload_files(self):
        # 1.检查是否存在路径
        local_dir = self.config.get(self.section_local, 'dir')
        self.ftp_Manager.ftp_connect(self.host, self.username, self.password)
        if self.check_file(local_dir):
            files = os.listdir(local_dir)
            remote_dir = self.config.get(self.section_ftp, 'target')
            count = 0
            for f in files:
                if '.txt' == os.path.splitext(f)[1] and 18 == len(f):
                    local_path = local_dir + f
                    fileDate = f[6:14]
                    now = datetime.date.today()
                    time_str = datetime.datetime.strftime(now, '%Y%m%d')
                    if time_str == fileDate:
                        new_filename = 'NMF_TRF_RI_CSDT_' + fileDate + '00_072h_OCE.txt'
                        remote_path = remote_dir + new_filename
                        is_success = self.ftp_Manager.upload_file(local_path, remote_path)
                        if is_success:
                            print('成功上传: ' + f)
                            count = count + 1
                        else:
                            print('上传失败：' + f)
        else:
            print('没有这个路径，请检查配置文件')
        print('海岛气象预报总共上传' + str(count) + '个文件')
        # localtime = time.asctime(time.localtime(time.time()))
        print(datetime.datetime.now())
        self.ftp_Manager.close_connect()

    # 下载
    def download_files(self):
        # 1. 链接
        sftp_manager_instance = self.sftp_Manager.sftp_connect(self.host, int(self.port), self.username, self.password)
        # 2. 城市预报下载
        self.download_normal(sftp_manager_instance)
        #3. EC文件下载
        self.download_EC(sftp_manager_instance)
        # 5.断开链接
        self.sftp_Manager.sftp_close(sftp_manager_instance)

    # 1. 下载swell.gif   SWH2.gif   SWH4.gif  SWH6.gif -Hs.png
    def download_normal(self, sftp_manager_instance):
        # 1. 不改名
        # local_path = os.path.join(self.local_dir, self.fileName_normal1)
        # local_dir = self.local_dir
        # remote_dir = self.target_normal
        # 1. 下载swell.gif   SWH2.gif   SWH4.gif  SWH6.gif
        remote_files = []
        remote_files.append(self.fileName_normal1)
        remote_files.append(self.fileName_normal2)
        remote_files.append(self.fileName_normal3)
        remote_files.append(self.fileName_normal4)

        # print(remote_path1)
        # 2. 下载指定文件swell.gif   SWH2.gif   SWH4.gif  SWH6.gif

        for remote_file in remote_files:
            is_success = self.sftp_Manager.sftp_download_one_file(sftp_manager_instance, self.local_dir,
                                                                  self.target_normal, remote_file,
                                                                  remote_file)
            # 2.1 记录日志
            self.save_log(is_success, remote_file)

        # 3. 下载城市文件 -Hs.png
        # remote_Filename_Query = RemoteFilenameQuery(-5, None, self.fileName_allCity)
        file_list = self.sftp_Manager.get_all_files_name(sftp_manager_instance, self.target_normal)
        for file in file_list:
            if file[-7:] == self.fileName_allCity:
                # 本地不需改名，所以本地文件和远端文件名一样
                is_success = self.sftp_Manager.sftp_download_one_file(sftp_manager_instance, self.local_dir,
                                                                      self.target_normal,
                                                                      file, file)
                # 3.1 记录日志
                self.save_log(is_success, file)

        #4. 下载EC文件
    def download_EC(self, sftp_manager_instance):
        #4.1 获取EC文件夹下所有文件名
        file_list = self.sftp_Manager.get_all_files_name(sftp_manager_instance, self.target_EC)
        EC_file_list = []
        for file in file_list:
            if file[0:2] == 'EC':
                EC_file_list.append(file)

        #4.2按照文件名从大到小排序,取前7个
        EC_file_list.sort(reverse=True)
        EC_target_file_list = EC_file_list[0:7]
        for file in EC_target_file_list:
            temp = file.split('_')
            local_file_name = temp[0] + '_' + temp[2]
            # print(local_file_name)
            is_success = self.sftp_Manager.sftp_download_one_file(sftp_manager_instance, self.local_dir,
                                                                  self.target_EC,
                                                                  file, local_file_name)
            # 3.1 记录日志
            self.save_log(is_success, file)

    def save_log(self, is_success, remote_file):
        """

        :param is_success: 是否下载成功
        :param remote_file: 下载的远端文件名
        :return:
        """
        now = datetime.datetime.now()
        if is_success:
            # print('已完成下载 :' + remote_file + ' 时间： ' + datetime.datetime.strftime(now, '%Y-%m-%d, %H:%M:%S'))
            self.logger.info('已完成下载文件: %s' % (remote_file))

        else:

            # print(remote_file + '下载失败, 请检查本地路径是否存在 ' + ' 时间： ' + datetime.datetime.strftime(now, '%Y-%m-%d, %H:%M:%S'))
            self.logger.error('文件下载失败, 请检查本地路径是否存在: %s  %s' % (remote_file))


def scheduleTask():
    times = 0;
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # scheduler.add_job(task, "cron", day_of_week="0-6", hour=19, minute=30)
    # scheduler.add_job(task, "cron", day_of_week="0-6", coalesce=True, misfire_grace_time=3600, hour=20, minute=20)
    scheduler.add_job(task, 'interval', seconds=60, id='task1')

    scheduler.start()


def task():
    videoConferenceService = VideoConferenceService(config_path, section_ftp, section_local)

    videoConferenceService.download_files()


if __name__ == "__main__":
    scheduleTask()
