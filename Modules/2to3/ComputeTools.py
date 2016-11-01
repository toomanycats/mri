from MiscTools import MiscTools
import os

HOME = os.environ['HOME']

class GridTools(MiscTools):
    def __init__(self):
        pass

    def _call_w_qsub(self, program, options):
        cmd = 'echo "%(program)s" | qsub  %(options)s'

        cmd = cmd %{'program':program,
                    'options':options,
                    }

        # helpful when running in ipython, which is what I normally do
        print(cmd)

        out, err, errcode = self.call_shell_program(cmd, error=True)

        return out, err, errcode

    def qsub(self, program, name, queue, stdout=HOME, stderr=HOME):
        options = " -N %(name)s -q %(queue)s -e %(stderr)s -o %(stdout)s"

        options = options % {'name': name,
                             'queue': queue,
                             'stderr': stderr,
                             'stdout': stdout
                            }

        out, err, errcode = self._call_w_qsub(program, options)
        return out, err, errcode


def freesurfer_template():
    script = """
#!/usr/bin/bash

hostname

export PATH=/home/dcuneo/anaconda3/bin:$PATH
export PATH=/home/dcuneo/git_tools:$PATH
export PATH=/home/dcuneo/git_pipeline:$PATH
source activate py3

export PYTHONPATH=/home/dcuneo/git_pipeline:$PYTHONPATH
export PYTHONPATH=/home/dcuneo/git_python27_mri/Modules/2to3:$PYTHONPATH

#FreeSurfer class sets up up other enviroment var

python /home/dcuneo/git_pipeline/CommandLineProg/submit_FS.py --rootdir %(proj_root)s --subjectid %(sub_id)s --seriesdesc %(series_desc)s --inputpath %(input_path)s --step %(step)s

"""
    return script

def GradUnwarp_template():
    script = """
#!/usr/bin/bash

host=$(hostname)
echo -e "Host:$host\n"

export PATH=/home/dcuneo/anaconda3/bin:$PATH
export PATH=/home/dcuneo/git_pipeline:$PATH
source activate py3

export PYTHONPATH=/home/dcuneo/git_pipeline:$PYTHONPATH
export PYTHONPATH=/home/dcuneo/git_python27_mri/Modules/2to3:$PYTHONPATH

python /home/dcuneo/git_pipeline/submit_GU.py -r %(proj_root)s -p %(project)s -s %(sub_id)s -d %(desc)s
"""
