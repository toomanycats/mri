from MiscTools import MiscTools
import os

HOME = os.environ['HOME']

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
host=$(hostname)
echo -e "Host:$host\n"

export PATH=/home/dcuneo/anaconda3/bin:$PATH
export PATH=/home/dcuneo/git_tools:$PATH
export PATH=/home/dcuneo/git_pipeline:$PATH
source activate py3

export PYTHONPATH=/home/dcuneo/git_pipeline:$PYTHONPATH
export PYTHONPATH=/home/dcuneo/git_python27_mri/Modules/2to3:$PYTHONPATH

export PATH=/netopt/rhel7/freesurfer/bin:$PATH
export PATH=/netopt/rhel7/freesurfer/mni/bin/:$PATH

export PERL5LIB=/netopt/rhel7/freesurfer/mni/lib/perl5/5.8.5:$PERL5LIB

export FREESURFER_HOME="/netopt/rhel7/freesurfer"
export FREESURFER_DIR="/data/sugrue1/FS_test"
export SUBJECTS_DIR="/data/surgrue1/FS_test"


python /home/dcuneo/git_pipeline/submit_FS.py --rootdir %(proj_root)s --subjectid %(sub_id)s --inputpath %(input_path)s --step %(step)s

"""
    return script


