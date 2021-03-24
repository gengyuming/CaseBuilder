import csv
from XmindReader import XmindReader


class TestCaseGenerator:
    def __init__(self, csv_path):
        self.csv_file = open(csv_path, 'w', newline='')
        self.__headers__ = ['所属模块', '用例标题', '前置条件', '步骤', '预期', '关键词', '优先级', '用例类型', '适用阶段']
        self.__csv_writer__ = csv.DictWriter(self.csv_file, self.__headers__)
        self.__csv_writer__.writeheader()
        self._titles = []
        self._csv_data = []

    def get_headers(self):
        return self.__headers__

    def init_csv_data(self, test_data):
        titles = []

        for data in test_data:
            steps = data['test_case'].split('&-&')

            title = '_'.join(steps[:-2])
            # index = 1
            # while title + '_' + str(index) in titles:
            #     index += 1

            test_case = steps[-2]

            # self._titles.append(title + '_' + str(index))
            self._titles.append(title)
            self._csv_data.append({'title': title,
                                   'condition': data['condition'],
                                   'test_case': test_case,
                                   'expect': steps[-1],
                                   'level': data['level']})

    def import_csv_data(self, module, case_type, phase):
        if self._csv_data:
            for data in self._csv_data:
                row = {
                    '所属模块': module,
                    '用例标题': data['title'],
                    '前置条件': data['condition'],
                    '步骤': data['test_case'],
                    '预期': data['expect'],
                    '关键词': '',
                    '优先级': data['level'],
                    '用例类型': case_type,
                    '适用阶段': phase
                }

                self.__csv_writer__.writerow(row)
        else:
            print('缺失数据，请进行数据初始化后再重新执行！')


if __name__ == '__main__':
    xmind_path = './ZentaoCaseBuilder/Xmind/aaa.xmind'
    csv_save_path = './ZentaoCaseBuilder/TestCase/test_case.csv'
    xm = XmindReader(xmind_path)
    test_data_list = xm.get_test_data()
    tc = TestCaseGenerator(csv_save_path)
    tc.init_csv_data(test_data_list)
    tc.import_csv_data('模块', '用例类型', '适用阶段')
