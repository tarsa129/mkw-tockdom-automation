import warnings


def combine_arguments(command_line_args: dict, file_args: list[dict]):
    combined_arguments:list[dict] = []

    if not file_args:
        return command_line_args

    command_line_args = {k: v for k, v in command_line_args.items() if v is not None}

    for i, file_arg_list in enumerate(file_args):
        for line_arg, line_value in command_line_args.items():
            if line_arg in file_arg_list:
                warnings.warn(f"Command line argument {line_arg}:{line_value} will override file argument {file_arg_list[line_arg]}")
        combined_arguments.append(file_arg_list | command_line_args)
    return combined_arguments
