import subprocess
import pandas as pd
import os

from celescope.tools.step import Step, s_common
from celescope.tools import utils
from celescope.__init__ import HELP_DICT
from celescope.rna.mkref import Mkref_rna


class Starsolo(Step):
    """
    Starsolo class.
    """
    def __init__(self, args, display_title=None):
        super().__init__(args, display_title=display_title)

        self.readFilesIn = args.fq2 + ' ' + args.fq1
        self.genomeDir = args.genomeDir
        self.soloCBwhitelist = args.soloCBwhitelist
        self.outPrefix = f'{self.outdir}/{self.sample}_'
        
        self.genome = Mkref_rna.parse_genomeDir(args.genomeDir)
        self.refflat = self.genome['refflat']

        # out
        self.picard_region_log = f'{self.out_prefix}_region.log'
        self.STAR_solo_log = f'{self.outdir}/{self.sample}_Solo.out/Gene/Summary.csv'
        self.STAR_bam = f'{self.outPrefix}Aligned.sortedByCoord.out.bam'

    @utils.add_log
    def STAR_solo(self):
        """Run Starsolo"""
        cmd = [
            'STAR',
            '--runThreadN', str(self.thread),
            '--genomeDir', self.genomeDir,
            '--readFilesIn', self.readFilesIn,
            '--soloType', 'CB_UMI_Simple',
            '--soloCBwhitelist', self.soloCBwhitelist,
            '--soloCBstart', self.args.soloCBstart, '--soloCBlen', self.args.soloCBlen,
            '--soloUMIstart', self.args.soloUMIstart, '--soloUMIlen', self.args.soloUMIlen,
            '--soloBarcodeReadLength', '0', '--soloFeatures', 'Gene GeneFull SJ Velocyto ',
            '--outSAMattributes', 'NH HI nM AS CR UR CB UB GX GN sS sQ sM',
            '--outSAMtype', 'BAM SortedByCoordinate', '--readFilesCommand', 'zcat',
            '--outFileNamePrefix', self.outPrefix,
        ]
        cmd = ' '.join(cmd)
        self.STAR_solo.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)
    
    @utils.add_log
    def picard(self):
        """Run Picard"""
        cmd = [
            'picard',
            '-Xmx20G',
            '-XX:ParallelGCThreads=4',
            'CollectRnaSeqMetrics',
            'I=%s' % (self.STAR_bam),
            'O=%s' % (self.picard_region_log),
            'REF_FLAT=%s' % (self.refflat),
            'STRAND=NONE',
            'VALIDATION_STRINGENCY=SILENT']
        cmd = ' '.join(cmd)
        self.picard.logger.info(cmd)
        subprocess.check_call(cmd, shell=True)
    
    @staticmethod
    def parse_solo_res(STAR_solo_log):
        """parse Starsolo result.

        :param STAR_solo_log: STAR_solo_log
        :return dictionary: metric_dict
        """
        STAR_solo_log = pd.read_csv(STAR_solo_log, header=None)
        STAR_solo_log.fillna(0, inplace=True)
        metric_dict = dict(zip(STAR_solo_log[0], STAR_solo_log[1]))

        return metric_dict

    @utils.add_log
    def gen_html(self):

        metric_dict = self.parse_solo_res(self.STAR_solo_log)

        self.add_metric(
            name='Number of Reads',
            value=int(metric_dict['Number of Reads']),
            help_info='Total reads from FASTQ files.'
        )

        self.add_metric(
            name='Valid Reads',
            value=int(float(metric_dict['Reads With Valid Barcodes']) * int(metric_dict['Number of Reads'])),
            total=int(metric_dict['Number of Reads']),
            help_info='Reads With Valid Barcodes'
        )

        self.add_metric(
            name='Q30 Bases in CB+UMI',
            value=metric_dict['Q30 Bases in CB+UMI'],
            display=str(round(metric_dict['Q30 Bases in CB+UMI'] * 100, 2)) + '%',
            help_info='Percent of barcode and UMI base pairs with quality scores over Q30'
        )

        self.add_metric(
            name='Q30 Bases in RNA read',
            value=metric_dict['Q30 Bases in RNA read'],
            display=str(round(metric_dict['Q30 Bases in RNA read'] * 100, 2)) + '%',
            help_info='Percent of read base pairs with quality scores over Q30'
        )
    
    @utils.add_log
    def run_compress(self):
        target_dir = f'{self.outdir}/{self.sample}_Solo.out/Gene/filtered'
        if not os.path.exists(target_dir):
            target_dir = f'{self.outdir}/{self.sample}_Solo.out/Gene/raw'
            
        cmd = f'gzip {target_dir} -r'
        subprocess.check_call(cmd, shell=True)

    def run(self):
        self.STAR_solo()
        self.picard()
        self.gen_html()
        self.run_compress()


def starsolo(args):
    with Starsolo(args, display_title="Demultiplexing") as runner:
        runner.run()


def get_opts_starsolo(parser, sub_program=True):
    parser.add_argument('--genomeDir', help=HELP_DICT['genomeDir'], required=True)
    parser.add_argument('--soloCBwhitelist', help='barcode white list', required=True)
    parser.add_argument('--soloCBstart', help='barcode start position', required=True)
    parser.add_argument('--soloUMIstart', help='UMI start position', required=True)
    parser.add_argument('--soloCBlen', help='barcode lengths', required=True)
    parser.add_argument('--soloUMIlen', help='UMI lengths', required=True)

    if sub_program:
        parser.add_argument('--fq1', help='R1 fastq file. Multiple files are separated by comma.', required=True)
        parser.add_argument('--fq2', help='R2 fastq file. Multiple files are separated by comma.', required=True)
        parser = s_common(parser)