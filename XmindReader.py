import os
import zipfile
import json


class XmindReader:
    """
        Xmind解析器
    """
    def __init__(self, file_path):
        self.connector = '_'
        self.__zip_file__ = zipfile.ZipFile(file_path, 'r')
        self._content_json = json.loads(self.__zip_file__.read('content.json').decode())
        self._catalog = self.generate_catalog(self._content_json[0]['rootTopic'], [])
        self._test_data = []
        self._test_case = []
        self.__generate_test_data__(self._catalog)

    def generate_catalog(self, content_json, catalog):
        """
        生成目录结构
        :param content_json: Xmind原始JSON
        :param catalog: 用于递归临时存储目录
        :return: 目录结构
        格式: JSON
        备注: 原始JSON精简版, 仅保留3种标签:
        'title': 标题
        'notes': 笔记（前置条件）
        'children': 子节点
        """
        catalog.append({})
        for key in content_json:
            if key == 'title':
                catalog[-1]['title'] = content_json[key]
            if key == 'notes':
                catalog[-1]['notes'] = content_json['notes']['plain']['content']
            if key == 'children':
                catalog[-1]['children'] = []
                for child in content_json['children']['attached']:
                    self.generate_catalog(child, catalog[-1]['children'])

        return catalog

    def get_content_json(self):
        """
        获取Xmind原始JSON
        :return:
        """
        return self._content_json

    def get_catalog(self):
        """
        获取目录结构
        :return: dict, {'一级目录1': {'二级目录1':{}, '二级目录2': {}}}
        """
        return self._catalog

    def get_test_data(self):
        """
        获取测试数据
        :return: list, 每个用例步骤之间以"-"分割
        """
        return self._test_data

    def get_first_title(self):
        """
        获取根目录标题
        :return:
        """
        return self._catalog[0]['title']

    def get_test_case(self):
        for data in self._test_data:
            self._test_case.append(data['test_case'])

        return self._test_case

    def __generate_test_data__(self, catalog, test_case='', condition='', level=''):
        """
        生成测试用例
        :param catalog: 目录结构
        :param test_case: 递归临时存储测试用例
        :param condition: 前置条件
        :param level: 优先级
        :return:
        """
        level_match = {'priority-1': '1', 'priority-2': '2', 'priority-3': '3', 'priority-4': '4'}
        for topic in catalog:
            tmp_condition = condition
            if 'notes' in topic.keys():
                condition = topic['notes']
            if 'markers' in topic.keys():
                if topic['markers'][0]['markerId'] in level_match.keys():
                    level = level_match[topic['markers'][0]['markerId']]

            if 'children' in topic.keys():
                if test_case:
                    self.__generate_test_data__(topic['children'], test_case + self.connector + topic['title'], condition, level=level)
                else:
                    self.__generate_test_data__(topic['children'], topic['title'], condition, level=level)
            else:
                test_data = {'condition': condition, 'test_case': test_case + self.connector + topic['title'], 'level': level}
                self._test_data.append(test_data)
                print(test_data)

            condition = tmp_condition


if __name__ == '__main__':
    path = './ZentaoCaseBuilder/Xmind/管理后台123.xmind'
    xm = XmindReader(path)
    print(xm.get_catalog())
    print(xm.get_test_data())
    print(xm.get_test_case())
    print(xm.get_first_title())

