import os
from celescope.tools import analysis_wrapper
from celescope.tools.step import s_common
from celescope.__init__ import HELP_DICT


class Analysis(analysis_wrapper.Scanpy_wrapper):

    def __init__(self, args, display_title=None):

        super().__init__(args, display_title)

        self.matrix_file = args.matrix_file

        if not os.path.exists(self.matrix_file):
            self.matrix_file = f'{self.outdir}/../01.starsolo/{self.sample}_Solo.out/Gene/raw'

    def run(self):
        self.calculate_qc_metrics()
        self.write_mito_stats()


def analysis(args):
    with Analysis(args, display_title='Analysis') as runner:
        runner.run()


def get_opts_analysis(parser, sub_program):
    parser.add_argument('--genomeDir', help=HELP_DICT['genomeDir'], required=True)
    if sub_program:
        parser.add_argument(
            '--matrix_file',
            help='Required. Matrix_10X directory from step count.',
            required=True,
        )
        parser = s_common(parser)