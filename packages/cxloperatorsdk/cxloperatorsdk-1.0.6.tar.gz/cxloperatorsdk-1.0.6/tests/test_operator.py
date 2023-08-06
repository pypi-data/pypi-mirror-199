from cxloperatorsdk.operator import Operator
from cxloperatorsdk.run_status import RunStatus

class SimpleOperator(Operator):
    def execute(self):
        pass

    def validate_config(self):
        return True

def test_base_operator():
    operator = Operator()
    operator.run()

    assert operator.status == RunStatus.FAILED

def test_good_operator():
    operator = SimpleOperator()
    operator.run()

    assert operator.status == RunStatus.SUCCESS

