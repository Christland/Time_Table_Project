import pprint
from os import path
from typing import List

import numpy as np
import openpyxl
import pandas as pd
from openpyxl import Workbook, load_workbook

from features.exam.service import get_exam_id_from_name, get_exams

from .queries import use_query


def insert_students(cur, id, examId, periodId):
    params = {'periodId': periodId, 'examId': examId, 'id': id}
    return use_query(params=params, query_type='add-students')


def get_students(id=None):
    return use_query(params={'id': id}, query_type='get-students')


def read_student_groups():

    data = []
    file_path = path.join(path.dirname(path.abspath(__file__)), '../../../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    raw_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='students')
    for row in raw_data.to_dict('record'):
        data.append(
            tuple((value for value in row.values() if not pd.isna(value))))

    return data


def get_all_student_ids():
    all_students = read_student_groups()
    return [std[0] for std in all_students]


def get_exam_student_group(exam_name, std_groups):
    return [exam[0] for exam in std_groups if exam_name in exam]


def get_student_group_exams(std_id):
    student_group = read_student_groups()
    exams = [student[1:] for student in student_group if student[0] == std_id]
    exam_list = [list(elem) for elem in exams]
    return exam_list

def get_formated_std_data():
    std_groups = get_all_student_ids()
    std_dic = {}
    for std_group in std_groups:
        new_dic = {std_group: get_student_group_exams(std_group)}
        std_dic.update(new_dic)

    return std_dic


def __extract_exam_ids_from_name(exams: List[list]):
    res = []
    for group in exams:
        try:
            res.extend([get_exam_id_from_name(examCode=exam) for exam in group if exam not in [
                       'CAT 352', 'CAT 354', 'CAT 356', 'CAT 358', 'CAT 358', 'CAT 361', 'CAT 363']])
        except IndexError:
            pass
    return res


def get_std_group_with_exams():
    student_groups = get_all_student_ids()
    std_dic = []
    for std_group in student_groups:
        exams_codes = get_student_group_exams(std_group)[0]

        exams = []
        for code in exams_codes:
            try:
                exam = get_exams(examCode=code)[0]
                exams.append(exam)
            except IndexError:
                print('404', code)
                pass

        item = {
            'student_id': std_group,
            'exams': exams
        }
        std_dic.append(item)

    return std_dic


def get_specific_genes(std_id, chromosome):
    exams = get_student_group_exams(std_id)
    exams_ids = __extract_exam_ids_from_name(exams)
    genes = []
    for id in exams_ids:
        res = [gene for gene in chromosome if gene["exam_id"] == id]

        if not len(res):
            continue
        genes.extend(res)
    return genes


if __name__ == '__main__':
    ch = [{
        'exam_id': 1
    },
        {
        'exam_id': 2
    }]

    # insert_students(id = '1', examId = '10', periodId = '23')
    # std_groups = read_student_groups()
    # pprint.pprint(get_student_group_exams(2))
    # print(get_exam_student_group('ENGL 352', std_groups))
    # pprint.pprint(get_student_group_exams(get_exam(), read_student_groups()))
    pprint.pprint(get_specific_genes(1, ch))
