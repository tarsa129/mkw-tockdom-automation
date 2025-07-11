class BaseHandlerActionArgument:
    def __init__(self):
        self.name = ""

class BaseHandlerAction:
    def __init__(self):
        self.name = ""
        self.action_function = None
        self.used_args: list[BaseHandlerActionArgument] = []

    def add_argument(self, name, description=""):
        new_arg = BaseHandlerActionArgument()
        new_arg.name = name
        self.used_args.append(new_arg)

    def execute_action(self, args):
        arg_values = []
        for used_arg in self.used_args:
            if used_arg.name in args:
                arg_values.append(args[used_arg.name])
            else:
                arg_values.append(None)
        self.action_function(*arg_values)

class BaseHandler:
    def __init__(self):
        self.actions: list[BaseHandlerAction] = []

    def add_action(self, name, action_function, args):
        new_action = BaseHandlerAction()
        new_action.name = name
        new_action.action_function = action_function
        for arg in args:
            new_action.add_argument(arg)
        self.actions.append(new_action)
        return new_action

    def handle_action(self, args):
        name = args["action"]
        for action in self.actions:
            if action.name == name:
                action.execute_action(args)
                break