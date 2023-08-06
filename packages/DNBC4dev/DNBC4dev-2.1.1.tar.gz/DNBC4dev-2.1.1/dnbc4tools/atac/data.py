import os
from collections import defaultdict
from dnbc4tools.tools.utils import str_mkdir,judgeFilexits,change_path,logging_call,hamming_distance,read_json
from dnbc4tools.__init__ import __root_dir__

detectNreads = 100000

def check_Dackdeaction_fq1(seq):
    if seq[0:6] == "TCTGCG" or seq[16:22] == "CCTTCC":
        return "nodarkreaction"
    elif len(seq) > 105:
        return "Other"
    else:
        return "darkreaction"
    
def check_Dackdeaction_fq2(seq):
    set_seq = 'AGATGTGTATAAGAGACAG'
    if hamming_distance(seq[0:19],set_seq) <=2 :
        return "nodarkreaction"
    else:
        return "darkreaction"
    
def fastqSeqReact(fq1,fq2):
    import pysam
    results_R1 = defaultdict(int)
    with pysam.FastxFile(fq1) as r1Fq:
        for fastq in range(detectNreads):
            try:
                record = r1Fq.__next__()
            except BaseException as e:
                print("\033[0;31;40mThere is not enough sequences to automatic identification!\033[0m")
                raise Exception('There is not enough sequences to automatic identification.')
            seq = record.sequence
            fq1Reaction = check_Dackdeaction_fq1(seq)
            if fq1Reaction:
                results_R1[fq1Reaction] += 1
    sorted_counts = sorted(results_R1.items(), key=lambda x: x[1], reverse=True)
    fq1Reaction, read_counts = sorted_counts[0][0], sorted_counts[0][1]
    percent = float(read_counts) / detectNreads
    if fq1Reaction == 'Other':
        raise Exception('The darkreaction are unable to be automatically determined.')
    if percent < 0.5:
        print("Valid chemistry read counts percent < 0.5")
        raise Exception('The darkreaction are unable to be automatically determined.')
    
    results_R2 = defaultdict(int)
    with pysam.FastxFile(fq2) as r2Fq:
        for fastq in range(detectNreads):
            try:
                record = r2Fq.__next__()
            except BaseException as e:
                print("\033[0;31;40mThere is not enough sequences to automatic identification!\033[0m")
                raise Exception('There is not enough sequences to automatic identification.')
            seq = record.sequence
            fq2Reaction = check_Dackdeaction_fq2(seq)
            if fq2Reaction:
                results_R2[fq2Reaction] += 1
    sorted_counts = sorted(results_R2.items(), key=lambda x: x[1], reverse=True)
    fq2Reaction, read_counts = sorted_counts[0][0], sorted_counts[0][1]
    percent = float(read_counts) / detectNreads
    if percent < 0.5:
        print("Valid chemistry read counts percent < 0.5")
        raise Exception('The darkreaction are unable to be automatically determined.')
    
    return fq1Reaction,fq2Reaction
        
class Data:
    def __init__(self, args):
        self.name = args.name
        self.fastq1 = args.fastq1 
        self.fastq2 = args.fastq2
        self.threads = args.threads
        self.darkreaction = args.darkreaction
        self.customize = args.customize
        self.outdir = os.path.join(args.outdir,args.name)
        self.genomeDir = args.genomeDir
        self.bcerror = args.bcerror

    def seqStructure(self):
        r1ReactionList = []
        r2ReactionList = []
        for i in range(len(self.fastq1.strip().split(','))):
            fastq1 = os.path.abspath(self.fastq1.strip().split(',')[i])
            fastq2 = os.path.abspath(self.fastq2.strip().split(',')[i])
            if self.customize or self.darkreaction != 'auto':
                pass
            else:
                fq1Reaction,fq2Reaction = fastqSeqReact(fastq1,fastq2)
                r1ReactionList.append(fq1Reaction)
                r2ReactionList.append(fq2Reaction)
            
        if self.customize:
            read_format = self.customize
        elif self.darkreaction != 'auto':
            if self.darkreaction.strip() == 'R1':
                read_format = 'bc:0:19,r1:20:-1,r2:19:-1'
            elif self.darkreaction.strip() == 'R2':
                read_format = 'bc:6:15,bc:22:31,r1:65:-1'
            elif self.darkreaction.strip() == 'R1R2':
                read_format = 'bc:0:19,r1:20:-1'
            else:
                read_format = 'bc:6:15,bc:22:31,r1:65:-1,r2:19:-1'
        else:
            if len(set(r1ReactionList)) != 1 or len(set(r2ReactionList)) != 1:
               print('\033[0;31;40mmultiple chemistry found in cDNA!\033[0m')
               raise Exception('The darkreaction are unable to be automatically determined in fastq.') 
            else:
                print('\033[0;32;40mThe darkreaction automatically determined in fastq1 : %s\033[0m'%(r1ReactionList[0]))
                print('\033[0;32;40mThe darkreaction automatically determined in fastq2 : %s\033[0m'%(r2ReactionList[0]))
                if r1ReactionList[0] == 'darkreaction' and r2ReactionList[0] == 'darkreaction':
                    read_format = 'bc:0:19,r1:20:-1'
                elif r1ReactionList[0] == 'nodarkreaction' and r2ReactionList[0] == 'darkreaction':
                    read_format = 'bc:6:15,bc:22:31,r1:65:-1'
                elif r1ReactionList[0] == 'darkreaction' and r2ReactionList[0] == 'nodarkreaction':
                    read_format = 'bc:0:19,r1:20:-1,r2:19:-1'
                else:
                    read_format = 'bc:6:15,bc:22:31,r1:65:-1,r2:19:-1'
        return read_format

    def run(self):
        judgeFilexits(self.fastq1,self.fastq2,self.genomeDir)
        str_mkdir('%s/01.data'%self.outdir)
        str_mkdir('%s/log'%self.outdir)
        change_path()

        genomeDir = os.path.abspath(self.genomeDir)
        read_format = Data.seqStructure(self)
        indexConfig = read_json('%s/ref.json'%genomeDir)
        refindex = indexConfig['index']
        genome = indexConfig['genome']
        whitelist = '%s/config/whitelist_atac.txt'%__root_dir__

        chromap_cmd = "%s/software/chromap --preset atac --bc-error-threshold %s --trim-adapters -x %s -r %s -1 %s -2 %s -o %s/01.data/aln.bed --barcode %s --barcode-whitelist %s --read-format %s -t %s 2> %s/01.data/alignment_report.tsv "\
            %(__root_dir__,self.bcerror,refindex,genome,self.fastq1,\
            self.fastq2,self.outdir,self.fastq1,whitelist,\
            read_format,self.threads,self.outdir)
        print('\nBarcode processing, Alignment.')
        logging_call(chromap_cmd,'data',self.outdir)

def data(args):
    Data(args).run()

def helpInfo_data(parser):
    parser.add_argument(
        '--name', 
        metavar='NAME',
        help='Sample name.', 
        type=str,
        required=True
        )
    parser.add_argument(
        '--outdir', 
        metavar='PATH',
        help='Output diretory, [default: current directory].', 
        default=os.getcwd()
        )
    parser.add_argument(
        '--fastq1', 
        metavar='FASTQ',
        help='The input R1 fastq files.', 
        required=True
        )
    parser.add_argument(
        '--fastq2', 
        metavar='FASTQ',
        help='The input R2 fastq files.', 
        required=True
        )
    parser.add_argument(
        '--darkreaction',
        metavar='STR',
        help='Sequencing dark cycles. Automatic detection is recommended, [default: auto].', 
        default='auto'
        )
    parser.add_argument(
        '--customize',
        metavar='STR',
        help='Customize readstructure.'
        )
    parser.add_argument(
        '--threads',
        type=int, 
        metavar='INT',
        default=4,
        help='Number of threads used for the analysis, [default: 4].'
        )
    parser.add_argument(
        '--genomeDir',
        type=str, 
        metavar='PATH',
        help='Path of folder containing reference database.',
        required=True
        )
    parser.add_argument(
        '--bcerror',
        type=int,
        metavar='INT',
        default=1,
        help='Set the error tolerance for cell barcodes.'
        )
    return parser