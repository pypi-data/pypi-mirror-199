# -*- coding: utf-8 -*-
# @Time    : 2023/3/21 10:13:10
# @Author  : Pane Li
# @File    : table_tr.py
"""
table_tr

"""
import logging

from playwright.sync_api import Locator


class Table:

    def __init__(self, columns: list, table_locator: Locator, unique_columns: list, select_option_locale: dict,
                 log_desc=None):
        """

        :param columns: [("acl_name", 'input'), ('action', 'select')] 说明列的表名以及 类型， 类型现在只支持三种('input'、'select'、'check')
        :param table_locator: table_locator 定位
        :param unique_columns:  确认唯一的列资源名称，
        :param select_option_locale: 选择项国际化 , 在选择时只接收label, 不支持value选择， 因为查找时也使用的label
        """
        self.columns = columns  # 列名要与实际的列相对应，不能多也不能少 [("acl_name", 'input'), ('action', 'select')]
        self.table_locator = table_locator
        self.unique_columns = unique_columns  # 重复列名
        self.tr = self.table_locator.locator('//tbody').locator('//tr')
        self.select_option_locale = select_option_locale
        self.log_desc = log_desc

    def __filter_td_index(self, contain_check=False, **kwargs):
        expect_result = []
        for input_key, input_value in kwargs.items():
            if not contain_check:
                result = list(filter(lambda a: a[0] == input_key and a[1] != 'check' and a[0] in self.unique_columns,
                                     self.columns))  # 排除掉check
            else:
                result = list(filter(lambda a: a[0] == input_key, self.columns))
            if len(result) == 1:
                expect_result.append((self.columns.index(result[0]), input_value, result[0][1]))  # 找出td是第几个，也及值
        return expect_result

    def __edit_add(self, **kwargs):
        for column in self.__filter_td_index(True, **kwargs):
            if column[1] is not None:
                if column[2] == 'input':
                    self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.fill(str(column[1]))
                elif column[2] == 'select':
                    option = self.select_option_locale.get(column[1]) if self.select_option_locale.get(
                        column[1]) else str(column[1])
                    self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.select_option(option)
                elif column[2] == 'check':
                    if column[1] in ('check', 'Yes', '是', 'yes'):
                        self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.check()
                    else:
                        self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.uncheck()
                else:
                    raise Exception(f'not support this type {column[2]}')

    def exist(self, find_one=True, **kwargs):
        """ 传入的资源是否存在, 对于check 项是不计入重复选项的，因为勾选其实只是开启功能而已

        :param find_one
        :param kwargs:
        :return:
        """
        search_tr = []
        expect_result = self.__filter_td_index(**kwargs)
        if expect_result:
            for tr_nth in range(0, self.tr.count()):
                for result_ in expect_result:
                    if self.tr.nth(tr_nth).locator('//td').nth(result_[0]).inner_text() != str(result_[1]):
                        break
                else:
                    search_tr.append(tr_nth)
                    if find_one:
                        break
        return search_tr

    def add(self, **kwargs):
        self.__edit_add(**kwargs)
        for i in range(0, self.tr.get_by_role('button').count()):
            if 'onAdd()' in self.tr.get_by_role('button').nth(i).get_attribute('onclick') and self.tr.get_by_role(
                    'button').nth(i).is_enabled():
                self.tr.get_by_role('button').nth(i).click()
                if self.log_desc is not None:
                    logging.info(f'add table {self.log_desc} success')
                break

    def delete(self, **kwargs):
        find_tr = self.exist(find_one=True, **kwargs)
        if find_tr:
            self.tr.nth(find_tr[0]).locator('//td').nth(0).click()
            for i in range(0, self.tr.get_by_role('button').count()):
                if 'onDelete()' in self.tr.get_by_role('button').nth(i).get_attribute(
                        'onclick') and self.tr.get_by_role('button').nth(i).is_enabled():
                    self.tr.get_by_role('button').nth(i).click()
                    if self.log_desc is not None:
                        logging.info(f'delete table {self.log_desc} success')
                    break

    def delete_all(self):
        nth = 1
        while self.tr.count() > nth + 2:
            self.tr.nth(nth).locator('//td').nth(0).click()
            try:
                for i in range(0, self.tr.get_by_role('button').count()):
                    if 'onDelete()' in self.tr.get_by_role('button').nth(i).get_attribute(
                            'onclick') and self.tr.get_by_role('button').nth(i).is_enabled():
                        self.tr.get_by_role('button').nth(i).click()
                        break
            except TimeoutError:
                nth = nth + 1
        logging.info('table resource all delete')

    def edit(self, old: dict, new: dict):
        find_tr = self.exist(find_one=True, **old)
        if find_tr:
            self.tr.nth(find_tr[0]).locator('//td').nth(0).click()
            self.__edit_add(**new)
            for i in range(0, self.tr.get_by_role('button').count()):
                if 'onOK()' in self.tr.get_by_role('button').nth(i).get_attribute('onclick') and self.tr.get_by_role(
                        'button').nth(i).is_enabled():
                    self.tr.get_by_role('button').nth(i).click()
                    if self.log_desc is not None:
                        logging.info(f'edit table {self.log_desc} success')
                    break
