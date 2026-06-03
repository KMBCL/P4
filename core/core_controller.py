from controllers.action_runner import ActionRunner


class CoreController:

    def __init__(self, action_runner: ActionRunner) -> None:
        self.action_runner = action_runner

    def run(self):
        self.action_runner.run()
