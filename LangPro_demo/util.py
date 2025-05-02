import subprocess

class ExternalToolError(RuntimeError):
    def __init__(self, cmd, output):
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return f'''Error running command: {self.cmd}\n\n{self.output}'''


def run_tool(cmd, input=None):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if input is not None:
        input = input.encode()

    out, _ = proc.communicate(input)
    if proc.returncode != 0:
        raise ExternalToolError(cmd, out)
    return out.decode()
