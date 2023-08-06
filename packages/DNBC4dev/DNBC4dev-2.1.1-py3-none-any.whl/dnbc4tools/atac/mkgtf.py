from dnbc4tools.tools.utils import judgeFilexits,change_path
from dnbc4tools.__init__ import __root_dir__
from dnbc4tools.tools.mkgtf import *


class Mkgtf:
    def __init__(self, args):
        self.action = args.action
        self.ingtf = args.ingtf
        self.output = args.output
        self.include = args.include
        self.type = args.type

    def run(self):
        change_path()
        if self.action == 'mkgtf':
            judgeFilexits(self.ingtf)
            list = [ str(i) for i in self.include.split(',')]
            print("\033[0;32;40mUsing \"%s\" for Analysis\033[0m"%self.type)
            print("\033[0;32;40mThe types of genes obtained are:\033[0m")
            for i in list:
                print(i)
            filtergtf(self.ingtf,self.output,self.type,list)
            print("\033[0;32;40mAnalysis Complete\033[0m")

        if self.action == 'stat':
            judgeFilexits(self.ingtf)
            print("\033[0;32;40mUsing \"%s\" for Analysis\033[0m"%self.type)
            statgtf(self.ingtf,self.type,self.output)
            print("\033[0;32;40mAnalysis Complete\033[0m")

def mkgtf(args):
    Mkgtf(args).run()

def helpInfo_mkgtf(parser):
    parser.add_argument(
        '--action',
        metavar='SELECT',
        default='mkgtf', 
        choices=['mkgtf', 'stat'], 
        help='Select the action for your program, include mkgtf,stat, [default: mkgtf].'
        )
    parser.add_argument(
        '--ingtf', 
        metavar='FILE' ,
        help='Path to the gtf file with annotations.'
        )
    parser.add_argument(
        '--output',
        metavar='FILE', 
        help='Path to output file.'
        )
    parser.add_argument(
        '--include',
        metavar='STR',
        default = normal_include,
        help='Set the filter parameter in mkgtf, you can set up multiple separated by commas.'
        )
    parser.add_argument(
        '--type',
        metavar='STR', 
        default = 'gene_biotype',
        help='Set according to the tag of gene type in gtf attributes, [default: gene_biotype].'
        )
    return parser