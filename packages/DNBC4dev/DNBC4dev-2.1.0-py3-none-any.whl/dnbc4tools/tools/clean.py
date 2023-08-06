import os,glob
from dnbc4tools.tools.utils import change_path
from dnbc4tools.__init__ import __root_dir__

def sampleName(indir,samplename=None):
    all_sample = {
        'scRNA':[],
        'scATAC':[]
        }
    if samplename:
        for name in samplename.split(','):
            if os.path.exists('%s/%s/04.report/%s_scRNA_report.html'%(indir,name,name)):
                all_sample['scRNA'].append(name)
            elif os.path.exists('%s/%s/04.report/%s_scATAC_report.html'%(indir,name,name)):
                all_sample['scATAC'].append(name)
            else:
                print("The sample of %s was not found"%name)
                pass
    else:
        html_list = glob.glob('%s/*/04.report/*.html'%(indir))
        for html in html_list:
            if 'scRNA' in html:
                sample = html.split('/')[-1].split('_scRNA_')[0]
                all_sample['scRNA'].append(sample)
            elif 'scATAC' in html:
                sample = html.split('/')[-1].split('_scATAC_')[0]
                all_sample['scATAC'].append(sample)
            else:
                pass
    return all_sample

def remove_file(file):
    if(os.path.exists(file)):
        os.remove(file)
        print("Deleted " + str(file))

def remove_RNAfile(scRNAlist,indir):
    print('scRNA file: ',end='')
    print(scRNAlist)
    for sample in scRNAlist:
        remove_file('%s/%s/01.data/Index_reads.fq.gz'%(indir,sample))
        remove_file('%s/%s/01.data/cDNA_barcode_counts_raw.txt'%(indir,sample))
        remove_file('%s/%s/01.data/final_sorted.bam'%(indir,sample))
        remove_file('%s/%s/02.count/anno_decon_sorted.bam'%(indir,sample))
        remove_file('%s/%s/02.count/%s_CB_UB_count.txt'%(indir,sample,sample))
        remove_file('%s/%s/02.count/cell_count_detail.xls'%(indir,sample))

def remove_ATACfile(scATAClist,indir):
    print("\033[0;32;40mStart Analysis\033[0m")
    print('scATAC file: ',end='')
    print(scATAClist)
    for sample in scATAClist:
        remove_file('%s/%s/01.data/aln.bed'%(indir,sample))
        remove_file('%s/%s/02.decon/%s.barcodeCount.tsv'%(indir,sample,sample))
        remove_file('%s/%s/03.analysis/*.bdg'%(indir,sample))
        remove_file('%s/%s/03.analysis/saved_clustering.rds'%(indir,sample))
    print("\033[0;32;40mComplete\033[0m")

class Clean:
    def __init__(self, args):
        self.name = args.name
        self.indir = args.indir

    def run(self):
        change_path()
        sampleDict = sampleName(self.indir,self.name)
        if len(sampleDict['scRNA']) > 0 :
            remove_RNAfile(sampleDict['scRNA'],self.indir)
        if len(sampleDict['scATAC']) > 0 :
            remove_ATACfile(sampleDict['scATAC'],self.indir)
    
def clean(args):
    Clean(args).run()

def helpInfo_clean(parser):
    parser.add_argument(
        '--name',
        metavar='NAME',
        default=None,
        help='Sample name, [default is all sample in current directory]'
        )
    parser.add_argument(
        '--indir',
        metavar='DIR',
        help='The dir for cleaned up, [default: current directory].', 
        default=os.getcwd()
        )