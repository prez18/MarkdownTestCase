# -*- coding: utf-8 -*-
class TestCaseElement:

    def __init__(self, value: str):
        self.value = value

    @property
    def description(self) -> str:
        return "TestCaseElement"


class BeginElement(TestCaseElement):

    @property
    def description(self) -> str:
        return "BeginElement"


class EndElement(TestCaseElement):

    @property
    def description(self) -> str:
        return "EndElement"


class TestTarget(TestCaseElement):

    @property
    def description(self) -> str:
        return "TestTarget"


class TestPurpose(TestCaseElement):

    @property
    def description(self) -> str:
        return "TestPurpose"


class TestCondition(TestCaseElement):

    @property
    def description(self) -> str:
        return "TestCondition"


class Precondition(TestCaseElement):

    @property
    def description(self) -> str:
        return "Precondition"


class Procedure(TestCaseElement):

    @property
    def description(self) -> str:
        return "Procedure"


class ExpectedValue(TestCaseElement):

    @property
    def description(self) -> str:
        return "ExpectedValue"


class DerivationMethod(TestCaseElement):

    @property
    def description(self) -> str:
        return "DerivationMethod"


class Remarks(TestCaseElement):

    @property
    def description(self) -> str:
        return "Remarks"


class Item(TestCaseElement):

    @property
    def description(self) -> str:
        return "Item"


class ProcedureItem(TestCaseElement):

    @property
    def description(self) -> str:
        return "ProcedureItem"


class TestCase:
    def __init__(self, test_target: TestTarget, test_purpose: TestPurpose, test_condition: TestCondition, precondition: [Item], procedure: [ProcedureItem],
                 expected_value: [Item], derivation_method: [Item], remarks: [Item]):
        self.test_target = test_target
        self.test_purpose = test_purpose
        self.test_condition = test_condition
        self.precondition = precondition
        self.procedure = procedure
        self.expected_value = expected_value
        self.derivation_method = derivation_method
        self.remarks = remarks

class StateTransitionValidation:

    @staticmethod
    def validate(elements: [TestCaseElement]) -> True:
        history = [BeginElement(value="")]
        for index, element in enumerate(elements):
            if StateTransitionValidation.can_transition(element, history):
                history.append(element)
            else:
                print("{0}行目でエラーが発生しました．".format(index + 1))
                print("テストケースの記載順序が不正であるか，記載が欠落しているようです．")
                return False
        end_element = EndElement(value="")
        if StateTransitionValidation.can_transition(end_element, history):
            return True
        else:
            print("エラーが発生しました．")
            print("ファイルの末尾の記載順序が不正であるか，記載が欠落しているようです．")
            return False

    @staticmethod
    def can_transition(to_element: TestCaseElement, on_history: [TestCaseElement]) -> True:
        if type(on_history[-1]) is BeginElement:
            return type(to_element) is TestTarget
        elif type(on_history[-1]) is TestTarget:
            return type(to_element) is TestPurpose
        elif type(on_history[-1]) is TestPurpose:
            return type(to_element) is TestCondition
        elif type(on_history[-1]) is TestCondition:
            return type(to_element) is Precondition
        elif type(on_history[-1]) is Precondition:
            return type(to_element) is Item or type(to_element) is Procedure
        elif type(on_history[-1]) is Item and type(
                list(filter(lambda x: type(x) is not Item, on_history))[-1]) is Precondition:
            return type(to_element) is Item or type(to_element) is Procedure
        elif type(on_history[-1]) is Procedure:
            return type(to_element) is ProcedureItem or type(to_element) is ExpectedValue
        elif type(on_history[-1]) is ProcedureItem and type(
                list(filter(lambda x: type(x) is not ProcedureItem, on_history))[-1]) is Procedure:
            return type(to_element) is ProcedureItem or type(to_element) is ExpectedValue
        elif type(on_history[-1]) is ExpectedValue:
            return type(to_element) is Item or type(to_element) is DerivationMethod
        elif type(on_history[-1]) is Item and type(
                list(filter(lambda x: type(x) is not Item, on_history))[-1]) is ExpectedValue:
            return type(to_element) is Item or type(to_element) is DerivationMethod
        elif type(on_history[-1]) is DerivationMethod:
            return type(to_element) is Item or type(to_element) is Remarks
        elif type(on_history[-1]) is Item and type(
                list(filter(lambda x: type(x) is not Item, on_history))[-1]) is DerivationMethod:
            return type(to_element) is Item or type(to_element) is Remarks
        elif type(on_history[-1]) is Remarks:
            return type(to_element) is Item or type(to_element) is TestTarget or type(
                to_element) is TestPurpose or type(to_element) is TestCondition or type(to_element) is EndElement
        elif type(on_history[-1]) is Item and type(
                list(filter(lambda x: type(x) is not Item, on_history))[-1]) is Remarks:
            return type(to_element) is Item or type(to_element) is TestTarget or type(
                to_element) is TestPurpose or type(to_element) is TestCondition or type(to_element) is EndElement
        else:
            return False
