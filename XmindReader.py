import os
import zipfile
import json

import configparser


class XmindReader:
    """
        Xmind解析器
    """

    def __init__(self, file):
        self.config = configparser.RawConfigParser()
        self.config.read('./config.ini', 'utf-8')
        self.connector = self.config.get('common', 'connector')
        self.__zip_file__ = zipfile.ZipFile(file, 'r')
        self.content_json = json.loads(self.__zip_file__.read('content.json').decode())
        self.sheet = self.get_sheet(0)
        self.root_topic = self.__get_root_topic__(self.sheet)
        self.root_topic_title = self.root_topic['title']
        self.catalog = self.generate_catalog(self.root_topic, [])
        self.test_data = []
        self.test_case = []
        self.generate_test_data(self.catalog)

    def get_sheet(self, index):
        """
        获取画布
        :param index:
        :return:
        """
        if isinstance(index, int):
            sheet = self.content_json[index]
        elif isinstance(index, str):
            for sheet_content in self.content_json:
                if sheet_content['title'] == index:
                    sheet = sheet_content
                    break
            else:
                raise Exception(f'未找到{index}画布(sheet)')
        else:
            sheet = {}
            raise TypeError

        self.sheet = sheet

        return sheet

    @staticmethod
    def __get_root_topic__(sheet):
        """
        获取根话题
        :param sheet: 画布
        :return:
        """
        root_topic = sheet['rootTopic']

        return root_topic

    @staticmethod
    def __get_title__(topic):
        """
        获取标题
        :return:
        """
        title = topic['title']

        return title

    @staticmethod
    def __get_notes__(topic):
        """
        获取笔记
        :param topic:
        :return:
        """
        notes = topic['notes']['plain']['content']

        return notes

    @staticmethod
    def __get_labels__(topic):
        """
        获取标签
        :param topic:
        :return:
        """
        labels = topic['labels']

        return labels

    @staticmethod
    def __get_callout__(topic):
        """
        获取标注
        :param topic:
        :return:
        """
        callout = topic['callout']['title']

        return callout

    @staticmethod
    def __get_markers__(topic):
        """
        获取标记
        :param topic:
        :return:
        """
        markers = []
        for mark in topic['markers']:
            markers.append(mark['markerId'])

        return markers

    @staticmethod
    def __get_summaries__(topic):
        """
        获取概要
        :param topic:
        :return:
        """
        summaries = []
        for index in range(len(topic['summaries'])):
            summary_range = eval(topic['summaries'][index]['range'])
            summaries.append(
                {'title': topic['children']['summary'][index]['title'],
                 'range': summary_range,
                 'start': summary_range[0],
                 'len': summary_range[1] - summary_range[0]}
            )

        return summaries

    @staticmethod
    def __get_children__(topic):
        """
        获取子话题
        :return:
        """
        children = topic['children']['attached']

        return children

    def generate_catalog(self, topic, catalog=None):
        """
        生成目录结构
        :param topic: 目录
        :param catalog: 用于递归临时存储目录
        :return: 目录结构
        格式: JSON
        备注: 原始JSON精简版, 保留标签如下:
        'title': 标题
        'notes': 笔记（前置条件）
        'labels': 标签(简短描述)
        'callout': 标注(待定)
        ’markers': 标记（优先级） list
        'summaries': 概要 list
            title ---> 标题
            range ---> 范围
            start ---> 其实索引
            len ---> 长度
        'children': 子节点  list
        """
        catalog.append({})
        for key in topic.keys():
            if key == 'title':
                catalog[-1]['title'] = self.__get_title__(topic)
            if key == 'notes':
                catalog[-1]['notes'] = self.__get_notes__(topic)
            if key == 'labels':
                catalog[-1]['labels'] = self.__get_labels__(topic)
            if key == 'callout':
                catalog[-1]['callout'] = self.__get_callout__(topic)
            if key == 'markers':
                catalog[-1]['markers'] = self.__get_markers__(topic)
            if key == 'summaries':
                catalog[-1]['summaries'] = self.__get_summaries__(topic)
            if key == 'children':
                catalog[-1]['children'] = []
                children = self.__get_children__(topic)
                for child in children:
                    self.generate_catalog(child, catalog[-1]['children'])

        return catalog

    def get_content_json(self):
        """
        获取Xmind原始JSON
        :return:
        """
        return self.content_json

    def get_catalog(self):
        """
        获取目录结构
        :return: dict, {'一级目录1': {'二级目录1':{}, '二级目录2': {}}}
        """
        return self.catalog

    def get_test_data(self):
        """
        获取测试数据
        :return: list, 每个用例步骤之间以"-"分割
        """
        return self.test_data

    def get_first_title(self):
        """
        获取根目录标题
        :return:
        """
        return self.catalog[0]['title']

    def get_test_case(self):
        for data in self.test_data:
            self.test_case.append(data['test_case'])

        return self.test_case

    def generate_test_data(self, catalog, test_case='', precondition='', label='', priority='', status='', summaries=None):
        """
        生成测试用例
        :param catalog: 目录结构
        :param test_case: 递归临时存储测试用例
        :param precondition: 前置条件
        :param label: 标签
        :param priority: 优先级
        :param status: 状态
        :param summaries: 概要
        :return:
        """
        priority_match = {'priority-1': 'High',
                          'priority-2': 'Normal',
                          'priority-3': 'Low'}

        status_match = {'tag-yellow': 'pending',
                        'tag-red': 'failed',
                        'tag-green': 'pass'}

        for index in range(len(catalog)):
            topic = catalog[index]
            summary = ''
            if summaries:

                for s in summaries:
                    if index in range(s['range'][0], s['range'][1] + 1):
                        summary = s['title']

            if 'notes' in topic.keys():
                precondition = topic['notes']

            if 'labels' in topic.keys():
                label = '\n'.join(topic['labels'])

            if 'markers' in topic.keys():
                for mark in topic['markers']:
                    if mark in priority_match.keys():
                        priority = priority_match[mark]
                    if mark in status_match.keys():
                        status = status_match[mark]

            if 'summaries' in topic.keys():
                summaries = topic['summaries']

            if 'children' in topic.keys():
                if test_case:
                    tmp_case = test_case + self.connector + topic['title']
                else:
                    tmp_case = topic['title']
                self.generate_test_data(catalog=topic['children'],
                                        test_case=tmp_case,
                                        precondition=precondition,
                                        label=label,
                                        priority=priority,
                                        status=status,
                                        summaries=summaries)

            else:
                if summary:
                    final_case = test_case + self.connector + topic['title'] + self.connector + summary
                else:
                    final_case = test_case + self.connector + topic['title']

                test_data = {'precondition': precondition,
                             'label': label,
                             'test_case': final_case,
                             'priority': priority,
                             'status': status}

                self.test_data.append(test_data)


if __name__ == '__main__':
    path = r'D:\workspace\MyGithub\CaseBuilder\Xmind\调试脑图.xmind'
    xm = XmindReader(path)
    # print(xm.content_json)
    print(xm.get_catalog())
    print(xm.get_test_data())
    # print(xm.get_test_case())
    # print(xm.get_first_title())
    print(xm.root_topic_title)
