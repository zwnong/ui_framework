#!/user/bin/env python
# encoding: utf-8
"""
@author: zwnong
@project: HogwartsSDE17
@file: base_page.py
@time: 2021/3/9 21:52
"""
import os
from time import sleep

import yaml
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from decorator.handle_black_list import handle_black
from utils.get_file import GetFile
from utils.logger import log


class BasePage:
    def __init__(self, driver: WebDriver = None):
        self.driver = driver

    @handle_black
    def find(self, locator, element):
        """
        重构查找元素
        :param locator: 定位方式
        :param element: 元素信息
        :return:
        """
        # appium_log.debug('find' + element)
        return WebDriverWait(self.driver, 10, 0.1).until(lambda x: x.find_element(locator, element))
        # return self.driver.find_element(locator, element)
        # black_list = ['//android.widget.TextView[@resource-id="com.xueqiu.android:id/tv_agree" and @text="同意"]',
        #               '//android.widget.TextView[@resource-id="com.xueqiu.android:id/tv_left" and @text="取消"]']
        # try:
        #     return self.driver.find_element(locator, element)
        # except Exception:
        #         for i in black_list:
        #             ele_path = self.finds(locator, i)
        #             if len(ele_path) > 0:
        #                 ele_path[0].click()
        #         return self.find(locator, element)
        # black_list = ['//android.widget.TextView[@resource-id="com.xueqiu.android:id/tv_agree" and @text="同意"]',
        #               '//android.widget.TextView[@resource-id="com.xueqiu.android:id/tv_left" and @text="取消"]']
        # try:
        #     return self.driver.find_element(locator, element)
        # except Exception:
        #     for i in black_list:
        #         ele_path = self.finds(locator, i)
        #         if len(ele_path) > 0:
        #             ele_path[0].click()
        #             return self.find(locator, element)

    def find_and_click(self, locator, element):
        """
        重构查找元素并点击
        :param locator: 定位方式
        :param element: 元素信息
        :return:
        """
        self.find(locator, element).click()

    def find_and_sendkeys(self, locator, element, value):
        return self.find(locator, element).send_keys(value)

    def finds(self, locator, value):
        return self.driver.find_elements(locator, value)

    def web_driver_wait(self, locator, value):
        return WebDriverWait(self.driver, 10, 0.1).until(lambda x: x.find_element(locator, value))

    # def get_yaml_data(self, file_path=None, value=None):
    #     if file_path is None:
    #         self.file_path = r'../config\data.yaml'
    #     else:
    #         self.file_path = file_path
    #     data = yaml.safe_load(open(str(self.file_path), 'r', encoding='utf-8'))
    #     try:
    #         value = data.get()
    #     except EOFError:
    #         value = None
    #     return value

    def lunch_driver(self):
        self.driver.launch_app()

    # 获取屏幕的宽高
    def get_size(self):
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        return width, height

    # 向左边滑动
    def swipe_left(self):
        # [100,200]
        x1 = self.get_size()[0] / 10 * 9
        y1 = self.get_size()[1] / 2
        x = self.get_size()[0] / 10
        self.driver.swipe(x1, y1, x, y1, 2000)

    # 向右边滑动
    def swipe_right(self):
        # [100,200]
        x1 = self.get_size()[0] / 10
        y1 = self.get_size()[1] / 2
        x = self.get_size()[0] / 10 * 9
        self.driver.swipe(x1, y1, x, y1, 2000)

    # 向上滑动
    def swipe_up(self):
        # [100,200]direction
        x1 = self.get_size()[0] / 2
        y1 = self.get_size()[1] / 10 * 9
        y = self.get_size()[1] / 10
        self.driver.swipe(x1, y1, x1, y, 2000)

    # 向下滑动
    def swipe_down(self):
        x1 = self.get_size()[0] / 2
        y1 = self.get_size()[1] / 10
        y = self.get_size()[1] / 10 * 9
        self.driver.swipe(x1, y1, x1, y, 2000)

    def swipe_on(self, direction=None):
        if direction == 'up':
            self.swipe_up()
        elif direction == 'down':
            self.swipe_down()
        elif direction == 'left':
            self.swipe_left()
        else:
            self.swipe_right()

    @handle_black
    def swipe_find(self, function_name, num=10, file_path=None):
        """
        # 上下滑动查找元素
        :param file_path:
        :param function_name:
        :param num:
        :return:
        """
        if file_path is None:
            file_path = fr'{self.father_path()}\yaml\main_page.yml'
        else:
            file_path = file_path
        get_file = GetFile(file_path)
        elements = get_file.get_value(function_name)
        for element in elements:
            for i in range(num):
                if i == num - 1:
                    self.driver.implicitly_wait(5)
                    raise NoSuchElementException(f'滑动{num}次，没找到元素')

                self.driver.implicitly_wait(1)
                try:
                    # 查找元素并点击
                    # return self.find_and_click(MobileBy.XPATH,element.get('element'))
                    return self.driver.find_element(MobileBy.XPATH, element.get('element')).click()

                    # 仅返元素是否为真
                    # element = self.driver.find_element(MobileBy.XPATH, element.get('element'))
                    # self.driver.implicitly_wait(5)
                    # return element
                except Exception:
                    self.swipe_up()

    def parse(self, yaml_path, fun_name):
        """
        # 解析关键字 解析yaml文件并调用相应的方法 实现相应功能
        :param yaml_path: yaml文件路径
        :param fun_name: yaml文件定义的方法名
        :return:
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            functance = yaml.load(f)
        steps = functance.get(fun_name)
        for step in steps:
            if step.get('action') == 'find_and_click':
                self.find_and_click(step.get('locator'), step.get('element'))
            elif step.get('action') == 'find_and_sendkeys':
                self.find_and_sendkeys(step.get('locator'), step.get('element'), step.get('contents'))

    def screenshot(self):
        return self.driver.get_screenshot_as_png()

    def get_web_view(shelf, driver):
        webview = driver.contexts
        for viw in webview:
            if 'WEBVIEW_cn.com.open.mooc' in viw:
                driver.switch_to.context(viw)
                break
        driver.find_element_by_link_text('C').click()
        try:
            driver.find_element_by_id('cn.com.open.mooc:id/left_icon').click()
        except Exception as e:
            driver.switch_to.context(webview[0])
            driver.find_element_by_id('cn.com.open.mooc:id/left_icon').click()
            raise e


    def pwd_path(self):
        return os.getcwd()

    def father_path(self):
        father_path = os.path.abspath(os.path.dirname(self.pwd_path()) + os.path.sep + ".")
        return father_path

    def grader_father_path(self):
        grader_father_path = os.path.abspath(os.path.dirname(self.pwd_path()) + os.path.sep + "..")
        return grader_father_path

    def get_yml_value(self, file_path, *args):
        return GetFile(file_path=file_path).get_value(args)

    def isElement(self, locator, ele):
        """
        Determine whether elements exist
        Usage:
        isElement(By.XPATH,"//a")
        """
        sleep(1)
        flag = None
        try:
            if locator == "id":
                # self.driver.implicitly_wait(60)
                self.driver.find_element_by_id(ele)
            elif locator == "xpath":
                # self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(ele)
            elif locator == "class":
                self.driver.find_element_by_class_name(ele)
            elif locator == "link text":
                self.driver.find_element_by_link_text(ele)
            elif locator == "partial link text":
                self.driver.find_element_by_partial_link_text(ele)
            elif locator == "name":
                self.driver.find_element_by_name(ele)
            elif locator == "tag name":
                self.driver.find_element_by_tag_name(ele)
            elif locator == "css selector":
                self.driver.find_element_by_css_selector(ele)
            flag = True
        except NoSuchElementException as e:
            flag = False
        finally:
            return flag
