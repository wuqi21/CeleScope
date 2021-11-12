__STEPS__ = [
    'sample', 'barcode', 'cutadapt', 'consensus', 'star',  'star_fusion','featureCounts',
    'target_metrics', 'variant_calling', 'analysis_snp', 'count_fusion'
]
__ASSAY__ = 'snp_fusion'
IMPORT_DICT = {
    'star': 'celescope.rna'
}
