# coding=utf-8
"""
@project_name:  ui_framework
@file:          base_driver.PY
@Author:        nong
@Time:          2021/8/10 9:17

"""
import os
import sys
from appium import webdriver
sys.path.append('../')


class BaseDriver:
    def android_driver(self, device: str, package: str, activity: str, port):
        """
        :param device: 设备名
        :param package: 启动的app的包名
        :param activity: 启动的app的activity名
        :param port: appium -p 端口号
        :return:
        """
        desirecaps = {
            "platformName": "Android",
            # automationName: UiAutomator2,
            "deviceName": f"{device}",
            # "app": f"{cts_path}",
            "appPackage": f"{package}",
            "appActivity": f"{activity}",
            # 跳过安装uiautomator2 服务
            # skipServerInstallation: True,
            # 跳过初始化
            #  skipDeviceInstallation: True
            "settings[waitForIdleTimeout]": 1,
            "newCommandTimeout": 2000,
            "noReset": True
        }
        driver = webdriver.Remote(f"http://127.0.0.1:{port}/wd/hub", desirecaps)
        driver.implicitly_wait(20)
        return driver

