# crawler/scheduler.py


from .workflow import Workflow


class Scheduler:
    def __init__(
            self,
            workflow: Workflow,
    ):
        self.workflow = workflow

    def start(self):
        self.workflow.start()
