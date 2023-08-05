import json

from cxloperatorsdk.run_status import RunStatus
from cxloperatorsdk.operator_exception import OperatorException

class Operator:
    def __init__(self, name = None):
        self.name = name

        self.status = None
        self.error = None

    # default implementation, assuming json format.
    def load_config(self):
        pass

    # validate operator's configuration. SDK Developer should override this method to validate
    # the passed in configuration. For operators that don't have/need a separate configuration file, simply
    # return True
    def validate_config(self):
        return False

    # prepare is a place holder/hook method, which allows operator developers to plug in all necessary preparations
    # before running the operator
    def prepare(self):
        # TODO: initialize and prepare the operator
        self.status = RunStatus.PENDING

    def run(self):
        self.load_config()
        valid = self.validate_config()

        if not valid:
            self.status = RunStatus.FAILED
            self.error = OperatorException('Invalid configuration')

            return

        try:
            self.prepare()

            self.status = RunStatus.RUNNING

            self.execute()

            self.status = RunStatus.SUCCESS
        except Exception as exp:
            self.status = RunStatus.FAILED
            self.error = exp

    # execute is the method where the real business logic is implemented. Operator developer must override this method
    # for an operator to work properly. The default implementation throws an OperatorException, which will always put
    # the operator in a failed state
    def execute(self):
        raise OperatorException('Failed')