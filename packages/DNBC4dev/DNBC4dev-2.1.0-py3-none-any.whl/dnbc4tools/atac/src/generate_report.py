import pandas as pd
import os
import argparse
import json
from datatable import dt, f
from dnbc4tools.__init__ import __version__


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def get_json(genomedir):
    with open(genomedir + '/ref.json','r',encoding='utf8') as fp:
        json_data = json.load(fp)
        chrMT=json_data['chrmt']
        species = json_data['species']
    return chrMT,species

def get_stat(path,sample,genomedir):
    stat = dict()
    with open(path + '/01.data/alignment_report.tsv', 'r', encoding='utf8') as fp:
        for line in fp:
            line = line.strip()
            if 'Number of reads:' in line:
                stat['read_pairs'] = int(int(line.split(': ')[1].split('.')[0])/2)
            if 'Number of barcodes in whitelist' in line:
                stat['read_pairs_whitelist'] = int(line.split(': ')[1].split('.')[0])
            if 'Number of corrected barcodes' in line:
                stat['read_corrected'] = int(line.split(': ')[1].split('.')[0])
            if 'Number of mapped reads:' in line:
                stat['read_mapped'] = int(line.split(': ')[1].split('.')[0])
            if 'Number of uniquely mapped reads' in line:
                stat['properly_reads'] = int(int(line.split(': ')[1].split('.')[0])/2)
    stat['frac_valid_barcode'] = str(round((stat['read_pairs_whitelist'] + stat['read_corrected'])/stat['read_pairs']*100,2))+'%'
    stat['map_rate'] = str(round(100*stat['read_mapped']/(2*(stat['read_pairs_whitelist'] + stat['read_corrected'])),2))+'%'

    with open(path + '/02.decon/%s.d2cCutoff.tsv'%sample, 'r', encoding='utf8') as fp:
        for line in fp:
            line = line.strip()
            if 'bead_cutoff' in line:
                stat['bead_thres'] = int(float(line.split('\t')[1]))
            if 'cor_cutoff' in line:
                stat['jaccard_thres'] = str(round(float(line.split('\t')[1]),5))

    fragment_df = pd.read_csv(os.path.join(path,"02.decon/%s.fragments.tsv.gz"%sample),encoding="utf-8",header=None,sep="\t",compression='gzip')
    fragment_df.rename(columns={0:"chr",1:"start",2:"end",3:"cellbarcode",4:"fragment"},inplace=True)
    total_fragment = len(fragment_df)
    nucleosomefree = len(fragment_df[(fragment_df['end'] - fragment_df['start'])<147])
    mononucleosome = len(fragment_df[((fragment_df['end'] - fragment_df['start'])<=294) & ((fragment_df['end'] - fragment_df['start'])>=147)])
    stat['nc_free_region'] = str(round(int(nucleosomefree)*100/int(total_fragment),2))+'%'
    stat['mono_nc_region'] = str(round(int(mononucleosome)*100/int(total_fragment),2))+'%'

    stat['bead_number'] = int(len(open(path + '/02.decon/%s.barcodeMerge.tsv'%sample, 'r').readlines()))

    chrMT,species=get_json(genomedir)
    stat['species'] = str(species)
    all_bed = dt.fread(path + '/01.data/aln.bed',header=False)
    chrM_num = all_bed[f.C0 == chrMT,:]['C4'].sum()[0,0]
    all_num = all_bed['C4'].sum()[0,0]
    stat['mit_rate']  = str(round(float(chrM_num*100/all_num),2))+'%'
    return stat


def get_args_from_file(path,sample,genomedir):
    csv = [path+'/03.analysis/cell_report.csv',\
    path+'/03.analysis/library.QC.csv']
    stat = get_stat(path,sample,genomedir)
    stat['samplename'] = str(sample)
    stat['version'] = __version__
    stat['ref_path'] = str(genomedir)
    
    for i in range(len(csv)):
        if i==0:
            df = pd.read_csv(open(csv[i]),encoding="utf_8",dtype=str,header=None,sep=":")
            stat['estimate_num_of_cell'] = df[1][0]
            stat['median_frag_per_cell'] = df[1][1]
            stat['median_frac_peaks'] = df[1][2]
            stat['median_frac_tss'] = df[1][3]

        if i==1:
            df = pd.read_csv(open(csv[i]),encoding="utf_8",dtype=str,header=None,sep=":")
            stat['frac_frag_overlap'] = df[1][0]
            stat['call_peak_number'] = df[1][1]
            stat['overlap_call_peak'] = df[1][2]
            stat['percent_dup'] = df[1][3]

    plot_file = [
    path+'/04.report/div/barcode_rank.div',\
    path+'/04.report/div/jaccard_rank.div',\
    
    path+'/04.report/base64/plot3_DropBeadsnum.base64',\
    path+'/04.report/base64/plot4_QC.base64',\
    path+'/04.report/base64/plot5_InterSize.base64',\
    path+'/04.report/base64/plot6_TSS.base64',\
    path+'/04.report/base64/plot7_Cluster_peak.base64',\
    path+'/04.report/base64/plot8_Cluster_depth.base64',\
    path+'/04.report/base64/plot9_Cluster_annotation.base64',\
    path+'/04.report/div/saturation.div',\
]
    plot_base64 = []
    plot_base64.append(open(path+'/04.report/div/barcode_rank.div',"r").read())
    plot_base64.append(open(path+'/04.report/div/jaccard_rank.div',"r").read())
    plot_base64.append(open(path+'/04.report/base64/plot3_DropBeadsnum.base64',"r").read())
    plot_base64.append(open(path+'/04.report/base64/plot4_QC.base64',"r").read())
    plot_base64.append(open(path+'/04.report/base64/plot5_InterSize.base64',"r").read())
    plot_base64.append(open(path+'/04.report/base64/plot6_TSS.base64',"r").read())
    plot_base64.append(open(path+'/04.report/div/cluster.div',"r").read())
    plot_base64.append(open(path+'/04.report/div/lg_uniqueFrags.div',"r").read())
    plot_base64.append(open(path+'/04.report/div/saturation.div',"r").read())


    '''
    for f in plot_file:
        if re.search('plot3_DropBeadsnum.base64',f) or re.search('plot4_QC.base64',f) or re.search('plot5_InterSize.base64',f) or re.search('plot6_TSS.base64',f):
            if os.path.exists(f):
                base64 = open(f).read()
                #img = ("<img src=%s height=500px width=100\%>" %base64)
                img = "<img src=\"data:image/png+xml;base64,"+base64+"\">"
                plot_base64.append(img)    
            else:
                plot_base64.append(
                <p style="font_family=DIN Next LT Pro;font_size=18px;font_weight=400">
                The cluster plot has not been generated because the data quality is too low.
                <p>
                )
        else:
            plot_base64.append(open(f).read())
    '''

    plot_order = ['plot1','plot2','plot3','plot4','plot5','plot6','plot7','plot8','plot9']
    plot_dict = dict(zip(plot_order, plot_base64))

    for k,v in stat.items():
        if k == 'jaccard_thres':
            pass
        elif is_number(v):
            stat[k] = format(int(v),',')
        else:
            continue
    return stat, plot_dict
    
def write_param_to_template(htmlTemplate,samplename,path,genomedir):
    stat, plot_dict = get_args_from_file(path,samplename,genomedir)
    template = open(htmlTemplate,).read()
    from string import Template

    html=Template(template)

    report=html.safe_substitute(sample_info=samplename, estimate_num_of_cell=stat['estimate_num_of_cell'],\
            median_frag_per_cell=stat['median_frag_per_cell'], median_frac_peaks=stat['median_frac_peaks'],\
            median_frac_tss=stat['median_frac_tss'],sample_id=stat['samplename'],\
            species=stat['species'], pipeversion=stat['version'],\
            ref_path=stat['ref_path'],\
            read_pairs=stat['read_pairs'],\
            frac_valid_barcode=stat['frac_valid_barcode'],\
            bead_thres=stat['bead_thres'],\
            bead_number=stat['bead_number'],\
            jaccard_thres=stat['jaccard_thres'],\
            frac_frag_overlap=stat['frac_frag_overlap'],\
            nc_free_region=stat['nc_free_region'],mono_nc_region=stat['mono_nc_region'],\
            call_peak_number=stat['call_peak_number'],overlap_call_peak=stat['overlap_call_peak'],\
            map_rate = stat['map_rate'],properly_reads = stat['properly_reads'],mit_rate = stat['mit_rate'],\
            percent_dup=stat['percent_dup'],plot1=plot_dict['plot1'],\
            plot2=plot_dict['plot2'],plot3=plot_dict['plot3'],\
            plot4=plot_dict['plot4'],plot5=plot_dict['plot5'],\
            plot6=plot_dict['plot6'],plot7=plot_dict['plot7'],\
            plot8=plot_dict['plot8'],plot10=plot_dict['plot9']
            )
    metrics_df = pd.DataFrame([stat])
    cols = ["samplename","species","estimate_num_of_cell","median_frag_per_cell","median_frac_peaks","median_frac_tss","read_pairs","frac_valid_barcode","map_rate",\
        "call_peak_number","nc_free_region","mono_nc_region","percent_dup","mit_rate"]
    metrics_summary_df = metrics_df[cols]
    metrics_summary_df.columns = ["SampleName","Species","Estimated number of cells","Median fragments per cell","Median fraction of fragments overlapping peaks",\
        "Median fraction of fragments overlapping TSSs","Total number of reads pairs","Fraction of read pairs with a valid barcode","Reads Mapped to Genome",\
        "Called peak number","Fraction of nucleosome-free regions","Fraction of fragments mono-nucleosome regions","Percent of duplicates","mito_rate"]
    return report,metrics_summary_df


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outPath', type=str, help=
	'''input the outpath''',)
    parser.add_argument('--htmlTemplate', type=str, help=
	'''input the html template''',)
    parser.add_argument('--sample', type=str, help=
        '''input the sample name''',)
    parser.add_argument('--genomedir', type=str, help=
        '''input the genome dir path''')

    args = parser.parse_args()
    return args

def main():
    args = get_args()
    outpath=get_args()[0]
    sample = get_args()[2]
    get_args_from_file()
    report,metrics_summary_df=write_param_to_template(args.htmlTemplate,args.sample.args.outPath,args.genomedir)
    fw = open(outpath+'/04.report/'+sample+'_scATAC_report.html','w')
    fw.write(report)
    file_df = outpath+'/04.report/metrics_summary.xls'
    metrics_summary_df.to_csv(file_df,sep='\t',index=None)

if __name__ == '__main__':
    main()