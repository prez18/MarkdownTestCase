# -*- coding: utf-8 -*-
from testcase import *
import re
import sys


class TestCaseDataStore:

    @staticmethod
    def read(path: str) -> [TestCase]:
        # マークダウンファイルの各行
        markdown_rows = []

        # マークダウンファイルの各行を取得する
        with open(path, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                markdown_rows.append(line)

        # マークダウンから取得した各行をテストケースの各要素としてパースする
        test_case_elements = TestCaseElementTranslator.translate(markdown_rows)
        # テストケースの各要素の順序不正や抜け漏れがないことを検証する
        if not StateTransitionValidation.validate(test_case_elements):
            sys.exit(1)

        # 検証が完了したため，テストケースのドメインオブジェクトに変換する
        test_target = []
        test_purpose = []
        test_condition = []
        for index, element in enumerate(test_case_elements):
            if type(element) is TestTarget:
                test_target.append(index)
            elif type(element) is TestPurpose:
                test_purpose.append(index)
            elif type(element) is TestCondition:
                test_condition.append(index)
        all_test_case: [TestCase] = []
        for index, condition in enumerate(test_condition):
            target: TestTarget = test_case_elements[list(filter(lambda x: x < condition, test_target))[-1]]
            purpose: TestPurpose = test_case_elements[list(filter(lambda x: x < condition, test_purpose))[-1]]
            precondition: [Item] = []
            procedure: [ProcedureItem] = []
            expected_value: [Item] = []
            derivation_method: [Item] = []
            remarks: [Item] = []
            tmp = condition + 2
            while len(test_case_elements) > tmp and type(test_case_elements[tmp]) is Item:
                precondition.append(test_case_elements[tmp])
                tmp += 1
            tmp += 1
            while len(test_case_elements) > tmp and type(test_case_elements[tmp]) is ProcedureItem:
                procedure.append(test_case_elements[tmp])
                tmp += 1
            tmp += 1
            while len(test_case_elements) > tmp and type(test_case_elements[tmp]) is Item:
                expected_value.append(test_case_elements[tmp])
                tmp += 1
            tmp += 1
            while len(test_case_elements) > tmp and type(test_case_elements[tmp]) is Item:
                derivation_method.append(test_case_elements[tmp])
                tmp += 1
            tmp += 1
            while len(test_case_elements) > tmp and type(test_case_elements[tmp]) is Item:
                remarks.append(test_case_elements[tmp])
                tmp += 1
            test_case = TestCase(target, purpose, test_case_elements[condition], precondition, procedure,
                                 expected_value, derivation_method, remarks)
            all_test_case.append(test_case)
        return all_test_case


class Const:
    TEST_TARGET = '- テスト対象: '
    TEST_PURPOSE = '    - テスト目的: '
    TEST_CONDITION = '        - テスト条件: '
    PRECONDITION = '            - 前提条件'
    PROCEDURE = '            - 手順'
    EXPECTED_VALUE = '            - 期待値'
    DERIVATION_METHOD = '            - 導出方法'
    REMARKS = '            - 備考'
    ITEM = '                - '
    PROCEDURE_ITEM = r'^                [0-9]+\. '
    COMMENT_ITEM = r' *# '


class TestCaseElementTranslator:

    @staticmethod
    def translate(markdown_lines: [str]) -> [TestCaseElement]:
        test_case_element = []
        for index, line in enumerate(markdown_lines):
            if line.startswith(Const.TEST_TARGET):
                test_case_element.append(TestTarget(value=line[len(Const.TEST_TARGET): -1]))
            elif line.startswith(Const.TEST_PURPOSE):
                test_case_element.append(TestPurpose(value=line[len(Const.TEST_PURPOSE): -1]))
            elif line.startswith(Const.TEST_CONDITION):
                test_case_element.append(TestCondition(value=line[len(Const.TEST_CONDITION): -1]))
            elif line.startswith(Const.PRECONDITION):
                test_case_element.append(Precondition(value=line[len(Const.PRECONDITION): -1]))
            elif line.startswith(Const.PROCEDURE):
                test_case_element.append(Procedure(value=line[len(Const.PROCEDURE): -1]))
            elif line.startswith(Const.EXPECTED_VALUE):
                test_case_element.append(ExpectedValue(value=line[len(Const.EXPECTED_VALUE): -1]))
            elif line.startswith(Const.DERIVATION_METHOD):
                test_case_element.append(DerivationMethod(value=line[len(Const.DERIVATION_METHOD): -1]))
            elif line.startswith(Const.REMARKS):
                test_case_element.append(Remarks(value=line[len(Const.REMARKS): -1]))
            elif line.startswith(Const.ITEM):
                test_case_element.append(Item(value=line[len(Const.ITEM): -1]))
            elif re.match(Const.PROCEDURE_ITEM, line):
                test_case_element.append(ProcedureItem(value=re.sub(Const.PROCEDURE_ITEM, "", line)[:-1]))
            else:
                print("{0}行目でエラーが発生しました．".format(index + 1))
                print("インデントも文法に含まれるので守る必要があります．タブ文字は使えません．半角スペースで表現してください．")
                print("また，「- テスト対象: 」や「1. 」「- 」などもフォーマットに含まれているので，アレンジするとエラーになります．")
                sys.exit(1)
        return test_case_element
