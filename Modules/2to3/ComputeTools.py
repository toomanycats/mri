from MiscTools import MiscTools

class GridTools(MiscTools):
    def __init__(self):
        pass

    def _call_w_qsub(self, program, options):
        cmd = 'echo "hostname;%(program)s" | qsub  %(options)s'

        cmd = cmd %{'program':program,
                    'options':options,
                    }

        # helpful when running in ipython, which is what I normally do
        print(cmd)

        out, err, errcode = self.call_shell_program(cmd, error=True)

        return out, err, errcode

    def qsub(self, program, name, queue):
        options = " -N %(name)s -q %(queue)s " %{'name': name,
                                                 'queue': queue
                                                 }

        out, err, errcode = self._call_w_qsub(program, options)
        return out, err, errcode


