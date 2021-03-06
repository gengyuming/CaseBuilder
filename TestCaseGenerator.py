import csv
import codecs
import configparser

from XmindReader import XmindReader


class TestCaseGenerator:
    """
    用例生成器
    """

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

        self.status = ['Draft', 'Deprecated', 'Approved']

        self.file_path = file_path

        if file_type.lower() == 'csv':
            self.csv_file = open(self.file_path, 'w', newline='', encoding='utf-8')
            self.__csv_writer__ = csv.writer(self.csv_file)
            self.csv_file.write(codecs.BOM_UTF8.decode('utf-8'))
            self.__csv_writer__.writerow(self.headers)
            self.csv_data = []

    def __del__(self):
        self.csv_file.close()

    def set_connector(self, connector):
        """
        设置连接符
        :param connector: str 连接符
        :return:
        """
        self.connector = connector

    def init_csv_data(self, test_data, folder, status, component, owner):
        """
        初始化csv数据
        :param test_data: 用例数据
        :param folder: 目录
        :param status: 状态
        :param component: 组件
        :param owner: 创建者
        :return:
        """
        if status not in self.status:
            status = self.status[0]

        step_list = []
        expect_list = []
        for index in range(len(test_data)):
            data = test_data[index]
            test_case = data['test_case'].split(self.connector)

            name = test_case[self.name_level]
            objective = test_case[self.objective_level]
            precondition = test_case[self.precondition_level]
            priority = data['priority']
            label = data['label']

            step_list.append(test_case[self.step_level])
            expect_list.append(test_case[self.expect_level])

            if index < len(test_data) - 1:
                next_test_case = test_data[index + 1]['test_case'].split(self.connector)
                next_name = next_test_case[self.name_level]
                next_precondition = next_test_case[self.precondition_level]

                if name != next_name or precondition != next_precondition:
                    step = '\n'.join(step_list)
                    expect = '\n'.join(expect_list)
                    self.csv_data.append([name, precondition, objective, step, expect, folder, status, priority, component, label, owner])
                    step_list = []
                    expect_list = []
            else:
                step = '\n'.join(step_list)
                expect = '\n'.join(expect_list)
                self.csv_data.append([name, precondition, objective, step, expect, folder, status, priority, component, label, owner])

        self.import_csv_data()

    def import_csv_data(self):
        """
        导入csv数据
        :return:
        """
        if self.csv_data:
            for data in self.csv_data:
                row = {
                    'Name': data['Name'],
                    'Precondition': data['Name'],
                    'Objective': data['Name'],
                    'Test Script (Step-by-Step) - Step': data['Name'],
                    'Test Script (Step-by-Step) - Expected Result': data['Name'],
                    'Folder': data['Name'],
                    'Status': data['Name'],
                    'Priority': data['Name'],
                    'Component': data['Name'],
                    'Labels': data['Name'],
                    'Owner': data['Name']
                }

                self.__csv_writer__.writerow(row)
        else:
            print('缺失数据，请进行数据初始化后再重新执行！')


if __name__ == '__main__':
    # xmind_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\Xmind\调试脑图.xmind'
    xmind_path = r'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\Xmind\test_TMP&case(1).xmind'
    csv_save_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\TestCase\CaseDemo.csv'
    xm = XmindReader(xmind_path)
    test_data_list = xm.get_test_data()

    tc = TestCaseGenerator(csv_save_path)
    tc.init_csv_data(test_data_list,
                     folder='/通知中心/test',
                     status='Draft',
                     component='None',
                     owner='gengyuming')
