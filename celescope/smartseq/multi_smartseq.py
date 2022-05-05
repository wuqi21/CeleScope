import os
from celescope.smartseq.__init__ import __ASSAY__
from celescope.tools.multi import Multi


class Multi_smartseq(Multi):
    """
    ## Usage
    ```
        multi_starsolo\\
        --mapfile ./rna.mapfile\\
        --genomeDir /SGRNJ/Public/Database/genome/homo_mus\\
        --soloCBwhitelist /SGRNJ03/randd/cjj/celedev/smartseq/smart_seq2.bclist\\
        --mod shell
    ```
    """
    def starsolo(self, sample):
        step = 'starsolo'
        arr = self.fq_dict[sample]
        cmd_line = self.get_cmd_line(step, sample)
        cmd = (
            f'{cmd_line} '
            f'--fq1 {arr[0]} --fq2 {arr[1]} '
        )
        self.process_cmd(cmd, step, sample, m=30, x=self.args.thread)
    
    def mapping(self, sample):
        step = "mapping"
        cmd_line = self.get_cmd_line(step, sample)
        cmd = (
            f'{cmd_line} '
            f'--fq None'
        )
        self.process_cmd(cmd, step, sample, m=5, x=1)

    def count(self, sample):
        step = "count"
        cmd_line = self.get_cmd_line(step, sample)
        STAR_solo_log = f'{self.outdir_dic[sample]["starsolo"]}/{sample}_Solo.out/Gene/Summary.csv'
        cmd = (
            f'{cmd_line} '
            f'--STAR_solo_log {STAR_solo_log} '
        )
        self.process_cmd(cmd, step, sample, m=5, x=1)
    
    def analysis(self, sample):
        step = 'analysis'
        matrix_file = f'{self.outdir_dic[sample]["starsolo"]}/{sample}_Solo.out/Gene/filtered'
        cmd_line = self.get_cmd_line(step, sample)
        cmd = (
            f'{cmd_line} '
            f'--matrix_file {matrix_file} '
        )
        self.process_cmd(cmd, step, sample, m=10, x=1)


def main():
    multi = Multi_smartseq(__ASSAY__)
    multi.run()


if __name__ == '__main__':
    main()
