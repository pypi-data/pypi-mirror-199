import os, re, json, collections
from subprocess import check_call
from dnbc4tools.tools.utils import judgeFilexits, change_path
from dnbc4tools.__init__ import __root_dir__
from dnbc4tools.tools.mkgtf import read_gtf

def write_config(genomeDir, species, gtf, chrM, blacklist, fasta, tag):
    if not os.path.exists(genomeDir):
        os.system('mkdir -p %s' % genomeDir)
    faidx_cmd = 'samtools faidx -o %s/genome.fa.fai %s' % (genomeDir, fasta)
    check_call(faidx_cmd, shell=True)
    genome_size = get_genome_size(genomeDir, species, gtf)
    get_tss_promoter(gtf, tag, genomeDir)
    ref_dict = collections.OrderedDict()
    ref_dict['species'] = str(species)
    ref_dict['genome'] = os.path.abspath(fasta)
    ref_dict['index'] = os.path.abspath('%s/genome.index' % genomeDir)
    ref_dict['chromeSize'] = os.path.abspath('%s/chrom.sizes' % genomeDir)
    ref_dict['tss'] = os.path.abspath('%s/tss.bed' % genomeDir)
    ref_dict['promoter'] = os.path.abspath('%s/promoter.bed' % genomeDir)
    if blacklist != 'None':
        ref_dict['blacklist'] = os.path.abspath(blacklist)
    else:
        ref_dict['blacklist'] = 'None'
    ref_dict['chrmt'] = get_chrM(chrM,genomeDir)
    ref_dict['genomesize'] = str(genome_size)
    with open(('%s/ref.json' % genomeDir), 'w', encoding='utf-8') as (jsonfile):
        json.dump(ref_dict, jsonfile, indent=4, ensure_ascii=False)
        jsonfile.write('\n')

def get_chrM(chrM,genomeDir):
    if chrM == 'auto':
        chrmtlist = ['chrM','MT','chrMT','mt','Mt']
        if os.path.exists(os.path.join(genomeDir,'genome.fa.fai')):
            with open(os.path.join(genomeDir,'genome.fa.fai'),'r') as file:
                chrlist =  [line.split()[0] for line in file]
                union = list(set(chrmtlist) & set(chrlist))
                if union:
                    chrMT = union[0]
                else:
                    chrMT = 'None'
        else:
            chrMT = 'None'
    else:
        chrMT = chrM
    print('Mitochondrial chromosome: %s'%chrMT)
    return chrMT

def get_genome_size(genomeDir,species,gtf):
    with open('%s/genome.fa.fai'%genomeDir,'r') as fai:
        with open('%s/chrom.sizes'%genomeDir,'w') as result:
            primary_contigs = get_primary_contigs(gtf)
            print('The remaining chromosomes are:')
            print(primary_contigs)
            chr_size = []
            for line in fai:
                line = line.strip()
                lst = line.split('\t')
                if lst[0] in primary_contigs:
                    result.write(lst[0]+'\t'+lst[1]+'\n')
                    chr_size.append(int(lst[1]))
    genome_size = sum(chr_size)

    if species in  ['Human','hg19','hg38', 'Homo_sapiens','GRCh38', 'GRCh37']:
        genome_size = 'hs'
    elif species in ['Mouse', 'mm10' ,'Mus_musculus','GRChm38']:
        genome_size = 'mm'
    elif species == 'Caenorhabditis elegans':
        genome_size = 'ce'
    elif species == 'Fruitfly':
        genome_size = 'dm'
    else:
        genome_size = genome_size
    return genome_size

def get_tss_promoter(gtf, type, genomeDir):
    gtfread = read_gtf(gtf, type)
    tss_bed = set()
    promoter_bed = set()
    no_basic = True
    tssfile = open(('%s/tss.bed' % genomeDir), 'w', encoding='utf-8')
    promoterfile = open(('%s/promoter.bed' % genomeDir), 'w', encoding='utf-8')
    for type_cell in gtfread:
        if type_cell:
            if type_cell[0].startswith('#'):
                pass
            else:
                cell_lst = type_cell[0].split('\t')
                chrome = cell_lst[0]
                start = int(cell_lst[3])
                end = int(cell_lst[4])
                strand = cell_lst[6]
                if strand == '+':
                    tss_start = start - 1
                    tss_end = tss_start + 1
                    promoter_start = start - 1 - 2000
                    promoter_end = start + 2000
                elif strand == '-':
                    tss_start = end - 1
                    tss_end = tss_start + 1
                    promoter_start = end - 1 - 2000
                    promoter_end = end + 2000
                transcript_tags = re.findall('tag\\s["*](\\w+)*["*]', cell_lst[-1])
                pattern = re.compile('(\\S+?)\\s*"(.*?)"')
                aDict = collections.OrderedDict()
                for m in re.finditer(pattern, cell_lst[-1]):
                    key = m.group(1)
                    value = m.group(2)
                    aDict[key] = value
                else:
                    if 'gene_name' in aDict:
                        gene_id = aDict['gene_name']
                    else:
                        if 'gene_id' in aDict:
                            gene_id = aDict['gene_id']
                        else:
                            gene_id = ''
                    is_basic = 'basic' in transcript_tags
                    if is_basic:
                        no_basic = False
                    tss = (str(chrome), str(tss_start), str(tss_end), str(gene_id), '.', str(strand), is_basic)
                    promoter = (str(chrome), str(promoter_start), str(promoter_end), str(gene_id), is_basic)
                    tss_bed.add(tss)
                    promoter_bed.add(promoter)

    for tss in sorted(tss_bed, key=(lambda x: (x[0], int(x[1])))):
        if no_basic or tss[-1]:
            tssfile.write('\t'.join(tss[0:-1]) + '\n')
    for promoter in sorted(promoter_bed, key=(lambda x: (x[0], int(x[1])))):
        if no_basic or promoter[-1]:
            promoterfile.write('\t'.join(promoter[0:-1]) + '\n')
    tssfile.close()
    promoterfile.close()


def get_primary_contigs(gtf):
    contigs = []
    with open(gtf, 'r') as (gtffile):
        for line in gtffile:
            line = line.strip()
            if line.startswith('#'):
                pass
            elif line == '':
                pass
            else:
                lst = line.split('\t')
                if lst[2] == 'gene':
                    contigs.append(lst[0])
    primary_contigs = set(contigs)
    return primary_contigs


def atac_index(fasta, genomeDir):
    index_cmd = '%s/software/chromap --build-index --ref %s --output %s/genome.index' % (__root_dir__, fasta, genomeDir)
    print('chromap verison: 0.2.3-r407')
    print('runMode: genomeGenerate')
    print('genomeDir: %s' % os.path.abspath(genomeDir))
    check_call(index_cmd, shell=True)


class Ref:

    def __init__(self, args):
        self.ingtf = args.ingtf
        self.fasta = args.fasta
        self.genomeDir = args.genomeDir
        self.species = args.species
        self.tag = args.tag
        self.chrM = args.chrM
        self.blacklist = args.blacklist
        self.noindex = args.noindex

    def run(self):
        change_path()
        judgeFilexits(self.ingtf, self.fasta)
        print('\x1b[0;32;40mBuilding index for dnbc4tools atac\x1b[0m')
        if not self.noindex:
            atac_index(self.fasta, self.genomeDir)
        write_config(self.genomeDir, self.species, self.ingtf, self.chrM, self.blacklist, self.fasta, self.tag)
        print('\x1b[0;32;40mAnalysis Complete\x1b[0m')


def mkref(args):
    Ref(args).run()


def helpInfo_mkref(parser):
    parser.add_argument(
        '--ingtf',
        metavar='FILE',
        help='Path to the gtf file with annotations.'
        )
    parser.add_argument(
        '--fasta',
        metavar='FASTA',
        help='Path to the fasta file with the genome sequences.'
        )
    parser.add_argument(
        '--genomeDir',
        metavar='DIR',
        default=(os.getcwd()),
        help='Path to the directory where genome files are stored, [default: current dir].'
        )
    parser.add_argument(
        '--species',
        metavar='STR',
        default='undefined',
        help='Species name, [default: undefined].'
        )
    parser.add_argument(
        '--tag',
        metavar='STR',
        default='transcript',
        help='Select the type to generate bed, [default: transcript].'
        )
    parser.add_argument(
        '--chrM',
        metavar='STR',
        default='auto',
        help='Mitochondrial chromosome name, [default: auto].'
        )
    parser.add_argument(
        '--blacklist',
        metavar='FILE',
        default='None',
        help='Genomic regions that are known to exhibit high signal noise, [default: None].'
        )
    parser.add_argument(
        '--noindex',
        action='store_true',
        help='Only generate ref.json without constructing database.'
        )
    return parser