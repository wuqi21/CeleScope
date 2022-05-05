from celescope.rna.star import Star
from celescope.rna.star import get_opts_star
from celescope.tools.plotly_plot import Pie_plot
from celescope.smartseq.starsolo import Starsolo

class Mapping(Star):
    def __init__(self, args, display_title=None):
        super().__init__(args, display_title=display_title)

        self.star_solo_prefix = f'{self.outdir}/../01.starsolo'
        self.picard_region_log = f'{self.star_solo_prefix}/{self.sample}_region.log'
        self.STAR_map_log = f'{self.star_solo_prefix}/{self.sample}_Log.final.out'
        self.STAR_solo_log = f'{self.star_solo_prefix}/{self.sample}_Solo.out/Gene/Summary.csv'
    
    def add_solo_metrics(self):

        metric_dict = Starsolo.parse_solo_res(self.STAR_solo_log)

        self.add_metric(
            name='Reads Uniquely Mapped to Gene',
            value=metric_dict['Reads Mapped to Gene: Unique Gene'],
            display=str(round(metric_dict['Reads Mapped to Gene: Unique Gene'] * 100, 2)) + '%',
            help_info='Reads Uniquely Mapped to Gene'
        )

        self.add_metric(
            name='Reads Uniquely and Multiply Mapped to Gene',
            value=metric_dict['Reads Mapped to Gene: Unique+Multiple Gene'],
            display=str(round(metric_dict['Reads Mapped to Gene: Unique+Multiple Gene'] * 100, 2)) + '%',
            help_info='Reads Uniquely and Multiply Mapped to Gene'
        )

    def run(self):
        self.get_star_metrics()
        self.add_other_metrics()
        self.add_solo_metrics()

        region_pie = Pie_plot(df_region=self.df_region).get_plotly_div()
        self.add_data(region_pie=region_pie)


def mapping(args):
    with Mapping(args, display_title="Mapping") as runner:
        runner.run()

def get_opts_mapping(parser, sub_program):
    get_opts_star(parser, sub_program)
