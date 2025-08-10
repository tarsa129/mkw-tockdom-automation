class BaseHandlerActionArgument:
    def __init__(self, name="", value=None, description=""):
        self.name = name
        self.value = value
        self.description = description

    @classmethod
    def create_new_arg(cls, argument):
        if isinstance(argument, dict):
            new_arg = BaseHandlerActionArgument(**argument)
        elif isinstance(argument, str):
            new_arg = BaseHandlerActionArgument(argument)
        else:
            new_arg = BaseHandlerActionArgument(value=argument)
        return new_arg

class BaseHandlerAction:
    def __init__(self):
        self.name = ""
        self.action_function = None
        self.used_args: list[BaseHandlerActionArgument] = []
        self.description = ""

    def add_argument(self, argument):
        new_arg = BaseHandlerActionArgument.create_new_arg(argument)
        self.used_args.append(new_arg)

    def add_arguments(self, args):
        for arg in args:
            self.add_argument(arg)

    def execute_action(self, args):
        arg_values = []
        for used_arg in self.used_args:
            if used_arg.name in args:
                arg_values.append(args[used_arg.name])
            else:
                arg_values.append(used_arg.value)
        self.action_function(*arg_values)

class BaseHandler:
    def __init__(self):
        self.actions: list[BaseHandlerAction] = []

    def add_action(self, name, action_function, args, description = ""):
        new_action = BaseHandlerAction()
        new_action.name = name
        new_action.action_function = action_function
        new_action.add_arguments(args)
        new_action.description = description
        self.actions.append(new_action)
        return new_action

    def handle_action(self, args):
        name = args["action"]
        for action in self.actions:
            if action.name == name:
                action.execute_action(args)
                break