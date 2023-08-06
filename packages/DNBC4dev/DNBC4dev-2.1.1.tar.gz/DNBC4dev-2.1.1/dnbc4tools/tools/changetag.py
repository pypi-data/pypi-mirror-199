from dnbc4tools.tools.utils import change_path,judgeFilexits
from dnbc4tools.__init__ import __root_dir__

def change(inbam,outbam,tag1,tag2):
    import pysam
    samfile = pysam.AlignmentFile(inbam, "rb")
    outsam = pysam.AlignmentFile(outbam, "wb",header=dict(samfile.header))

    for sam in samfile:
        try:
            if sam.has_tag('UB'):
                Rtag1 = sam.get_tag(tag1)
                Rtag2 = sam.get_tag(tag2)
                sam.set_tag(tag1,Rtag2)
                sam.set_tag(tag2,Rtag1)
                outsam.write(sam)
        except KeyError:
            continue
    outsam.close()
    

class Changetag:
    def __init__(self, args):
        self.inbam = args.inbam
        self.outbam = args.outbam
        self.tag = args.tag

    def run(self):
        judgeFilexits(self.inbam)
        change_path()
        print("\033[0;32;40mStart Analysis\033[0m")
        tagsplit = self.tag.split(',')
        print("Using \"%s\" for Analysis"%self.tag)
        if len(tagsplit) == 2:
            change(self.inbam,self.outbam,tagsplit[0],tagsplit[1])
        else:
            raise Exception('The tag format or input is wrong.')
        print("\033[0;32;40mComplete\033[0m")

def changetag(args):
    Changetag(args).run()

def helpInfo_changetag(parser):
    parser.add_argument(
        '--inbam', 
        metavar='FILE',
        help='BAM file that is used as input .', 
        type=str,
        required=True
        )
    parser.add_argument(
        '--outbam', 
        metavar='FILE',
        help='BAM file that is generated as output.', 
        type=str,
        required=True
        )
    parser.add_argument(
        '--tag', 
        metavar='FILE',
        default='CB,DB',
        help='Tags that need to exchange content, [default: CB,DB]', 
        )
    return parser
