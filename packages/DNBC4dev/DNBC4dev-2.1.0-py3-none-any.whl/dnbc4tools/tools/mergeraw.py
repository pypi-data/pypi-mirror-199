import os
from dnbc4tools.tools.utils import change_path,str_mkdir,judgeFilexits,read_anndata,write_matrix
from dnbc4tools.__init__ import __root_dir__

def create_rawMerge(rawMatrix,filterMatrix,barcode2cell):
    import warnings
    warnings.filterwarnings("ignore")
    adataRaw = read_anndata(rawMatrix)
    adataFilter = read_anndata(filterMatrix)
    alist = []
    with open(barcode2cell,'r') as beads2cell:
        for line in beads2cell:
            lst = line.strip().split('\t')
            alist.append(lst[0])
    adataMerge = adataFilter.concatenate(
        adataRaw[~adataRaw.obs.index.isin(alist)],
        index_unique=None,
        batch_key=None,join='outer',
        fill_value=0
        )
    adataMerge.var = adataMerge.var.drop(['gene_symbols-0','gene_symbols-1'],axis=1)
    return adataMerge


class MergeRaw:
    def __init__(self, args):
        self.rawmatrix = args.rawmatrix
        self.filtermatrix = args.filtermatrix
        self.barcodecell = args.barcodecell
        self.outdir = args.outdir

    def run(self):
        judgeFilexits(self.rawmatrix,self.filtermatrix,self.barcodecell,self.outdir)
        change_path()
        import warnings
        warnings.filterwarnings("ignore")
        print("\033[0;32;40mStart Analysis\033[0m")

        ## creat raw merge matrix
        adataMerge = create_rawMerge(
            self.rawmatrix,
            self.filtermatrix,
            self.barcodecell)
        
        str_mkdir('%s/rawMerge_matrix'%self.outdir)
        write_matrix(adataMerge,'%s/rawMerge_matrix'%self.outdir)
        print("\033[0;32;40mComplete\033[0m")

def mergeraw(args):
    MergeRaw(args).run()

def helpInfo_mergeraw(parser):
    parser.add_argument(
        '--rawmatrix', 
        metavar='PATH',
        help='The raw matrix that needs cell merging.', 
        type=str,
        required=True
        )
    parser.add_argument(
        '--filtermatrix', 
        metavar='PATH',
        help='The filter matrix that needs cell merging.', 
        type=str,
        required=True
        )
    parser.add_argument(
        '--barcodecell', 
        metavar='FILE',
        help='Combination file of cell barcode, comment hexadecimal.', 
        required=True
        )
    parser.add_argument(
        '--outdir', 
        metavar='PATH',
        help='Output diretory, [default: current directory].', 
        default=os.getcwd()
        )
    return parser