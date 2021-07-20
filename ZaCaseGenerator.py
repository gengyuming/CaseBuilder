import csv
import configparser

from XmindReader import XmindReader


class TestCaseGenerator:
    """
    用例生成器
    """
    def __init__(self, file_path, file_type='csv'):
        self.config = configparser.RawConfigParser()
        self.config.read('./config.ini', 'utf-8')

        self.headers = [
            'Name',  # 用例名称
            'Precondition',  # 前置条件
            'Objective',  # 页面
            'Test Script (Steps) - Step',  # 测试脚本-步骤
            'Test Script (Steps) - Expected Result',  # 测试脚本-期待结果
            'Folder',  # 目录
            'Status',  # 状态
            'Priority',  # 优先级
            'Component',  # 组件
            'Labels',  # 标签
            'Owner'  # 创建者
        ]
        self.name_level = int(self.config.get('level', 'name'))
        self.precondition_level = int(self.config.get('level', 'precondition'))
        self.objective_level = int(self.config.get('level', 'objective'))
        self.step_level = int(self.config.get('level', 'step'))
        self.expect_level = int(self.config.get('level', 'expect'))

        attribute_list = ['name_level', 'precondition_level', 'objective_level', 'step_level', 'expect_level']
        for attribute in attribute_list:
            value = getattr(self, attribute)
            if value > 0:
                setattr(self, attribute, value-1)

        self.status = ['Draft', 'Deprecated', 'Approved']

        self.file_path = file_path

        if file_type.lower() == 'csv':
            self.csv_file = open(self.file_path, 'w', newline='')
            self.__csv_writer__ = csv.writer(self.csv_file)
            self.__csv_writer__.writerow(self.headers)
            self.csv_data = []

        self.connector = '&-&'

    def set_connector(self, connector):
        """
        设置连接符
        :param connector: str 连接符
        :return:
        """
        self.connector = connector

    def set_header_level(self, header_level):
        """
        设置字段层级
        :param header_level: dict
            header_list: [name_level, precondition_level, objective_level, step_level, expect_level]
            format: {'name_level': 1, 'precondition_level: 2}
        :return:
        """
        for header, level in header_level.items():
            if isinstance(level, int) or str(level).isdigit():
                setattr(self, header, int(level)-1)
            else:
                print(str(header) + ' is illegal')

    def init_csv_data(self, test_data, folder, status, component, owner):
        """
        初始化csv数据
        :param test_data:
        :param folder:
        :param status:
        :param component:
        :param owner:
        :return:
        """
        # row data
        name = ''
        objective = ''
        precondition = ''
        step_list = []
        expect_list = []
        priority = ''
        label = ''

        if status not in self.status:
            status = self.status[0]

        start = True
        for data in test_data:

            test_case = data['test_case'].split(self.connector)
            if start:
                name = test_case[self.name_level]
                objective = test_case[self.precondition_level]
                precondition = test_case[self.precondition_level]
                priority = data['priority']
                label = data['label']
                start = False

            tmp_name = test_case[self.name_level]
            tmp_objective = test_case[self.precondition_level]
            tmp_precondition = test_case[self.precondition_level]
            tmp_priority = data['priority']
            tmp_label = data['label']

            if name == tmp_name and tmp_precondition == precondition:
                step_list.append(test_case[self.step_level])
                expect_list.append(test_case[self.expect_level])
            else:
                step = '\n'.join(step_list)
                expect = '\n'.join(expect_list)
                print([name, precondition, objective, step, expect, folder, status, priority, component, label, owner])
                self.csv_data.append([name, precondition, objective, step, expect, folder, status, priority, component, label, owner])

                # reset row
                name = tmp_name
                objective = tmp_objective
                precondition = tmp_precondition
                step_list = []
                expect_list = []
                priority = tmp_priority
                label = tmp_label
                step_list.append(test_case[self.step_level])
                expect_list.append(test_case[self.expect_level])

        print(self.csv_data)
        self.import_csv_data()

    def import_csv_data(self):
        """
        导入csv数据
        :return:
        """
        if self.csv_data:
            for data in self.csv_data:
                gbk_data = []
                for item in data:
                    gbk_data.append(item.encode('gbk', 'replace').decode('gbk', 'replace'))

                self.__csv_writer__.writerow(gbk_data)

            print('csv数据导入成功')
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
                     folder='目录1/目录2',
                     status='ab',
                     component='组件',
                     owner='耿裕明')

