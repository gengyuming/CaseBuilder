import csv
import codecs

from XmindReader import XmindReader


class TestCaseGenerator:
    def __init__(self, file_path, file_type='csv'):

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

        self.status = ['Draft', 'Deprecated', 'Approved']

        self.file_path = file_path

        if file_type.lower() == 'csv':
            self.csv_file = open(self.file_path, 'w', newline='')
            self.__csv_writer__ = csv.writer(self.csv_file)
            self.__csv_writer__.writerow(self.headers)
            self.csv_data = []

    def set_headers(self, headers):
        self.headers = headers
        return self.headers

    def init_csv_data(self, test_data, folder, status, component, owner):
        index = 1
        for data in test_data:
            test_case = data['test_case'].split('&-&')
            name = test_case[0] + str(index).zfill(4)
            precondition = data['precondition']
            objective = test_case[1]
            step = []
            try:
                step = test_case[2:-1]
            except Exception as e:
                pass
            step = '-'.join(step)
            expect = test_case[-1]
            if status not in self.status:
                status = self.status[0]
            priority = data['priority']
            label = data['label']

            self.csv_data.append([name, precondition, objective, step, expect, folder, status, priority, component, label, owner])
            index += 1
        print(self.csv_data)
        self.import_csv_data()

    def import_csv_data(self):
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
    xmind_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\Xmind\通知センターTest.xmind'
    csv_save_path = 'D:\workspace\ZAGitlab\ZaTools\ZACaseBuilder\TestCase\CaseDemo.csv'
    xm = XmindReader(xmind_path)
    test_data_list = xm.get_test_data()

    tc = TestCaseGenerator(csv_save_path)
    tc.init_csv_data(test_data_list,
                     folder='目录1/目录2',
                     status='ab',
                     component='组件',
                     owner='耿裕明')

