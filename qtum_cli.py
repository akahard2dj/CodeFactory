import subprocess
import json


def qtum_cli(cmds: list):
    if isinstance(cmds, list):
        execute_cmd = list()
        execute_cmd.append('C:\\Program Files (x86)\\Qtum\\daemon\\qtum-cli.exe')
        for cmd in cmds:
            execute_cmd.append(cmd)

        proc = subprocess.Popen(execute_cmd, stdout=subprocess.PIPE)
        buf_str = ''
        for line in iter(proc.stdout.readline, b''):
            buf_str += line.decode('UTF-8').rstrip()

        try:
            res_json = json.loads(buf_str)
        except json.decoder.JSONDecodeError:
            res_json = buf_str

        return res_json

    else:
        raise TypeError
