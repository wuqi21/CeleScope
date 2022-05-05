from celescope.tools.step import Step, s_common
from celescope.smartseq.starsolo import Starsolo


class Count(Step):
    def __init__(self, args, display_title=None):
        super().__init__(args, display_title=display_title)

        self.STAR_solo_log = args.STAR_solo_log

    def add_solo_metrics(self):

        metric_dict = Starsolo.parse_solo_res(self.STAR_solo_log)

        self.add_metric(
            name='Estimated Number of Cells',
            value=int(metric_dict['Estimated Number of Cells']),
            help_info='The number of barcodes considered as cell-associated.'
        )

        self.add_metric(
            name='Fraction of Unique Reads in Cells',
            value=metric_dict['Fraction of Unique Reads in Cells'],
            display=str(round(metric_dict['Fraction of Unique Reads in Cells'] * 100, 2)) + '%',
            help_info='The fraction of uniquely-mapped-to-transcriptome reads with cell-associated barcodes.'
        )
        self.add_metric(
            name='Mean Reads per Cell',
            value=int(metric_dict['Mean Reads per Cell']),
            help_info='The number of valid reads divided by the estimated number of cells.'
        )
        self.add_metric(
            name='Median Reads per Cell',
            value=int(metric_dict['Median Reads per Cell']),
            help_info='The Median of valid reads divided by the estimated number of cells.'
        )

        self.add_metric(
            name='UMIs in Cells',
            value=int(metric_dict['UMIs in Cells']),
            help_info='Number of Total UMI in Cells.'
        )
        self.add_metric(
            name='Mean UMI per Cell',
            value=int(metric_dict['Mean UMI per Cell']),
            help_info='Number of Mean UMI in Cells.'
        )
        self.add_metric(
            name='Median UMI per Cell',
            value=int(metric_dict['Median UMI per Cell']),
            help_info='Number of Median UMI in Cells.'
        )

        self.add_metric(
            name='Mean Gene per Cell',
            value=int(metric_dict['Mean Gene per Cell']),
            help_info='Number of Mean Gene Count per Cells.'
        )
        self.add_metric(
            name='Median Gene per Cell',
            value=int(metric_dict['Median Gene per Cell']),
            help_info='Number of Median Gene Count per cells.'
        )
        self.add_metric(
            name='Total Gene Detected',
            value=int(metric_dict['Total Gene Detected']),
            help_info='Total Gene Detected.'
        )
        self.add_metric(
            name='Sequencing Saturation',
            value=metric_dict['Sequencing Saturation'],
            display=str(round(metric_dict['Sequencing Saturation'] * 100, 2)) + '%',
            help_info='The fraction of UMI originating from an already-observed UMI.'
        )

    def run(self):
        self.add_solo_metrics()


def count(args):
    with Count(args, display_title="Cells") as runner:
        runner.run()

def get_opts_count(parser, sub_program):
    if sub_program:
        s_common(parser)
        parser.add_argument('--STAR_solo_log', help='STARsolo log', required=True)
    return parser




