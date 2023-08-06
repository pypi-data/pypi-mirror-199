import subprocess
import json
import ast


class Action:
    """
        Represents the action component of a `FiniteStateMachine`.
        In actions, user-defined functions are executed.
    """

    def __init__(self, package:str, module:str, function:str, params:set) -> None:
        """
            Description:
                Creates an Action object that runs the given function.

            Arguments:
                - package : `str` - name of the package of the user-defined function.
                - module : `str` - name of the module of the user-defined function.
                - function : `str` - name of the user-defined function.
                - params : `set` - set of parameter names, they must be variables
                stored in `StateMachineContext`.
        """
        self.__package = package
        self.__module = module
        self.__function = function
        self.__params = params


    def __generate_command(self, *args) -> str:
        """
            Description:
                Generates a one-line python script to run the given function
                implemented in the given module of the given package.
            
            Arguments:
                - **kwargs : `dict` - specific function parameters, they must be
                variables stored in `StateMachineContext`.

            Return:
                - `str` : generated command to run the user-defined function.
        """
        kwargs = args[0]
        arguments = ""

        for key, value in kwargs.items():
            if key in self.__params:
                if isinstance(value, str):
                    arguments += "{}='{}',".format(
                        key, value)
                else:
                    arguments += "{}={},".format(
                        key, value)

        return """python -c "from {}.{} import {}; print({}({}))""".format(
            self.__package, self.__module, self.__function, self.__function, arguments)


    def __run_command(self, runner_cmd) -> str:
        """
            Description:
                Runs the command previously generated and capture the output
                (via. print function used in the generated command).

            Arguments:
                - runner_cmd : `str` - commands generated with the given parameters.

            Return:
                - `str` : captured output from command line (can be casted).
        """
        return subprocess.run(
            args=runner_cmd,
            capture_output=True,
            shell=True,
            universal_newlines=True
        ).stdout


    def execute(self, context) -> dict:
        """
            Description:
                Executes the function embedded in action and returns the output
                as STRING, just for now.

            Arguments:
                - context : `StateMachineContext` - context of the state machine

            Return:
                - `dict` : dictionary stores used variables and the output
        """
        keyword_arguments = dict()
        for parameter in self.__params:
            value = context.get_variables().get(parameter)
            keyword_arguments[parameter] = value

        try:
            runner_command = self.__generate_command(keyword_arguments)
            raw_output = self.__run_command(runner_command)
            output = ast.literal_eval(raw_output)
            decoded_output = json.loads(json.dumps(output).replace("\'", "\""))
            return decoded_output

        except:
            return None