import csv
import codecs
import configparser

from CaseEnum import Priority, CaseStatus, ResultStatus
from XmindReader import XmindReader


class TestCaseGenerator:
    def __init__(self, file_path, file_type='csv'):
        self.config = configparser.RawConfigParser()
        self.config.read('./config.ini', 'utf-8')
        self.connector = self.config.get('common', 'connector')

        self.headers = [
            'Name',  # 用例名称
            'Precondition',  # 前置条件
            'Objective',  # 页面
            'Test Script (Step-by-Step) - Step',  # 测试脚本-步骤
            'Test Script (Step-by-Step) - Expected Result',  # 测试脚本-期待结果
            'Folder',  # 目录
            'Status',  # 状态
            'Priority',  # 优先级
            'Component',  # 组件
            'Labels',  # 标签
            'Owner'  # 创建者
        ]

        self.case_status = []

        for key, value in CaseStatus.__dict__.items():
            if '__' not in key:
                self.case_status.append(value)

        self.file_path = file_path

        if file_type.lower() == 'csv':
            self.csv_file = open(self.file_path, 'w', newline='', encoding='utf-8')
            self.__csv_writer__ = csv.DictWriter(self.csv_file, self.headers)
            self.__csv_writer__.writeheader()
            self.csv_file.write(codecs.BOM_UTF8.decode('utf-8'))
            self.csv_data = []

        self.priority_match = {'priority-1': Priority.PRIORITY_1,
                               'priority-2': Priority.PRIORITY_2,
                               'priority-3': Priority.PRIORITY_3}

    def __del__(self):
        try:
            self.csv_file.close()
        except Exception:
            pass

    def set_connector(self, connector):
        """
        设置连接符
        :param connector: str 连接符
        :return:
        """
        self.connector = connector

    def init_csv_data(self, test_data, status, component, owner):
        """
        初始化csv数据
        :param test_data: 用例数据
        :param status: 状态
        :param component: 组件
        :param owner: 创建者
        :return:
        """
        index = 1
        name = ''
        for data in test_data:
            test_case = data['test_case'].split(self.connector)

            # 用例名称 -> 2级目录的自增序号
            if not test_case[1] == name:
                index = 1
            name = test_case[1] + str(index).zfill(4)

            # 前置条件 -> 笔记
            precondition = data['precondition']

            # 页面 -> 2级目录
            objective = test_case[1]

            # 步骤 -> 3级目录到-2级目录的集合，以换行符分割
            step = []
            try:
                step = test_case[2:-1]
            except Exception as e:
                pass
            step = '\n'.join(step)

            # 期待结果 -> -1级目录
            expect = test_case[-1]

            # 目录
            folder = test_case[0]

            # 用例状态
            if status.upper() not in [s.upper() for s in self.case_status]:
                status = self.case_status[0]

            # 优先级
            priority = ''
            for mark in data['markers']:
                if mark in self.priority_match.keys():
                    priority = self.priority_match[mark]

            # 标签
            label = data['label']

            row = {
                'Name': name,
                'Precondition': precondition,
                'Objective': objective,
                'Test Script (Step-by-Step) - Step': step,
                'Test Script (Step-by-Step) - Expected Result': expect,
                'Folder': folder,
                'Status': status,
                'Priority': priority,
                'Component': component,
                'Labels': label,
                'Owner': owner
            }
            self.csv_data.append(row)
            index += 1
        print(self.csv_data)
        self.import_csv_data()

    def import_csv_data(self):
        """
        导入csv数据
        :return:
        """
        if self.csv_data:
            for data in self.csv_data:
                self.__csv_writer__.writerow(data)
        else:
            print('缺失数据，请进行数据初始化后再重新执行！')


if __name__ == '__main__':
    xmind_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\Xmind\调试脑图.xmind'
    # xmind_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\Xmind\通知センターTest.xmind'
    csv_save_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\TestCase\CaseDemo.csv'
    xm = XmindReader(xmind_path)
    test_data_list = xm.get_test_data()

    tc = TestCaseGenerator(csv_save_path)
    tc.init_csv_data(test_data_list,
                     status='ab',
                     component='组件',
                     owner='耿裕明')
