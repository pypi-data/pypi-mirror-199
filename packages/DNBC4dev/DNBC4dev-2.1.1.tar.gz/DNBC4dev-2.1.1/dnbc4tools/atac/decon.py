import os
from dnbc4tools.tools.utils import str_mkdir,judgeFilexits,change_path,logging_call,read_json
from dnbc4tools.__init__ import __root_dir__

class Decon:
    def __init__(self,args):
        self.name = args.name
        self.outdir = os.path.join(args.outdir,args.name)
        self.threads = args.threads
        self.genomeDir = args.genomeDir
        self.forcefrag = args.forcefrag

    def run(self):
        judgeFilexits(self.genomeDir)
        str_mkdir('%s/02.decon'%self.outdir)
        str_mkdir('%s/log'%self.outdir)
        change_path()

        genomeDir = os.path.abspath(self.genomeDir)
        indexConfig = read_json('%s/ref.json'%genomeDir)
        blacklist = indexConfig['blacklist']
        tss = indexConfig['tss']
        chrmt = indexConfig['chrmt']
        chromeSize = indexConfig['chromeSize']

        d2c_cmd = ["%s/software/d2c/bin/d2c merge -i %s/01.data/aln.bed --fb 20000 -o %s/02.decon -c %s -n %s --bg %s --ts %s --sat --bt1 CB --log %s/02.decon"\
            %(__root_dir__,self.outdir,self.outdir,self.threads,self.name,chromeSize,tss,self.outdir)]
        if self.forcefrag:
            d2c_cmd += ['--bf %s'%self.forcefrag]
        if chrmt != 'None':
            d2c_cmd += ['--mc %s'%chrmt]
        if blacklist != 'None':
            d2c_cmd += ['--bl %s'%blacklist]
        d2c_cmd = ' '.join(d2c_cmd)
        print('\nCell calling, Deconvolution.')
        logging_call(d2c_cmd,'decon',self.outdir)

def decon(args):
    Decon(args).run()

def helpInfo_decon(parser):
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
        '--forcefrag', 
        metavar='INT',
        help='Minimum number of fragments to be thresholded.'
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
    return parser