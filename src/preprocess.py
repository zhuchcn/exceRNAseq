from snakemake.shell import shell
from utils import SlurmJob


if snakemake.params.get('use_scratch'):
    slurm = SlurmJob()
    slurm.setUp()
    sample = snakemake.wildcards.sample
    prefix = f'{slurm.scratch}/{sample}'
    log = f'{slurm.scratch}/{sample}.htsStats.log'
else:
    log = snakemake.log
    prefix = snakemake.params.prefix


shell(f"""
    hts_Stats -L {log} -U {snakemake.input} | \\
    hts_AdapterTrimmer -A -L {log} -a {snakemake.params.adapter} | \\
    hts_QWindowTrim -n -A -L {log} | \\
    hts_NTrimmer -n -A -L {log}  | \\
    hts_Stats -A -L {log} -f {prefix}
""")

if snakemake.params.get('use_scratch'):
    shell(f"""
    mv {slurm.scratch}/{sample}_SE.fastq.gz  {snakemake.output}
    mv ){slurm.scratch}/{sample}.htsStats.log  {snakemake.log}
    """)
    slurm.tearDown()
