from XmindReader import XmindReader
from TestCaseGenerator import TestCaseGenerator


def main(xmind_path, save_folder, module, case_type, phase):
    xm = XmindReader(xmind_path)
    test_data_list = xm.get_test_data()
    file_name = xm.get_first_title()
    save_path = save_folder + '/' + file_name + '.csv'
    print(save_path)
    tc = TestCaseGenerator(save_path)
    tc.init_csv_data(test_data_list)
    tc.import_csv_data(module, case_type, phase)


if __name__ == '__main__':
    xmind_path = './ZentaoCaseBuilder/Xmind/aaa.xmind'
    save_folder = './ZentaoCaseBuilder/TestCase'
    module = '模块'
    case_type = '用例类型'
    phase = '适用阶段'

    main(xmind_path, save_folder, module, case_type, phase)

