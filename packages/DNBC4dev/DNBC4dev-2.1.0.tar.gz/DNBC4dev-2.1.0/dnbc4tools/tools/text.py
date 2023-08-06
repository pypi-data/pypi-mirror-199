# Single-cell analysis workflow instructions tips
# category {rna,atac,casb}
# type {dnbc4,dnbc4tools}

def help_text(category,type):
    if category == 'rna':

        help_text = '''
        DNBelab C Series Single-Cell RNA analysis workflow:
        --------------------------------
        \033[0;32;40mFunction\033[0m:
        \033[0;32;40m%s run\033[0m      Analyze sequencing data from single-cell libraries, including cDNA and oligo libraries. 
                                This process include quality control, filtering, alignment, annotation, 
                                bead-based cell merging, and obtaining matrix of gene expression for each cell.
                                Downstream analysis includes dimensionality reduction, clustering, and annotation analysis.
        \033[0;32;40m%s multi\033[0m    Generate shell scripts for running the "%s run" command on multiple samples.
        \033[0;32;40m%s mkgtf\033[0m    Filter the gene types in a GTF annotation file.
        \033[0;32;40m%s mkref\033[0m    Build reference database for aligning and annotating'''%(type,type,type,type,type)

    if category == 'atac':
        help_text = '''
        DNBelab C Series Single-Cell ATAC analysis workflow:
        --------------------------------
        \033[0;32;40mFunction\033[0m:
        \033[0;32;40m%s run\033[0m      Analyze sequencing data from single-cell libraries.
                                 This process include data filtering, alignment, cell calling, 
                                 and deconvolution, to generate unique fragment file for each cell. 
                                 Downstream analysis include peak calling, dimensionality reduction, and clustering.
        \033[0;32;40m%s multi\033[0m    Generate shell scripts for running the "%s run" command on multiple samples.
        \033[0;32;40m%s mkgtf\033[0m    Filter the gene types in a GTF annotation file.
        \033[0;32;40m%s mkref\033[0m    Build reference database.'''%(type,type,type,type,type)


    if category == 'tools':
        help_text = '''
        DNBelab C Series Single-Cell utility commands:
        --------------------------------
        \033[0;32;40mFunction\033[0m:
        \033[0;32;40m%s clean\033[0m      Remove intermediate files generated during an analysis workflow.
        \033[0;32;40m%s mergeraw\033[0m   Merge raw_matrix beads based on magnetic bead merging results.
        \033[0;32;40m%s changetag\033[0m  Exchange the tag information in bam in pairs.'''%(type,type,type)

    return help_text

    # atac


sum_help = '''
        DNBelab C Series Single-Cell analysis system:
        --------------------------------
        \033[0;32;40mdnbctools rna\033[0m      Single-Cell RNA analysis workflow
        \033[0;32;40mdnbctools atac\033[0m     Single-Cell ATAC analysis workflow
        \033[0;32;40mdnbctools tools\033[0m    Analysis utility commands'''


def help_sub_text(category,type,pipe):
    
    if category == 'rna':
        if pipe == 'mkgtf':
            help_text = '''
            Filter the gene types in a GTF annotation file.
            Gtf must contain at least "gene" or "transcript" types and "exon" type. 
            The attributes must have at least one of "gene_id" or "gene_name" and one of "transcript_id" or "transcript_name".
            
            '--include', choose which gene types to keep by filtering, the types to keep depends on your research,
                    which is included by default:
                     protein_coding, lncRNA, lincRNA, antisense, IG_C_gene, IG_D_gene, 
                     IG_J_gene, IG_LV_gene, IG_V_gene, IG_V_pseudogene, IG_J_pseudogene, 
                     IG_C_pseudogene,TR_C_gene, TR_D_gene, TR_J_gene, TR_V_gene 
            
            The action parameter can be set to mkgtf or stat:
            '--action stat', calculate the number of various gene types.
                Example:
                    %s mkgtf --action stat --ingtf genes.gtf --output gtfstat.txt --type gene_biotype

            '--action mkgtf', filter gene types.
                Example:
                    %s mkgtf --ingtf genes.gtf --output genes.filter.gtf --type gene_biotype 
            '''%(type,type)

        elif pipe == 'mkref':
            help_text = '''
            Build reference database for aligning and annotating

            '--species',  the species name in html are derived from this parameter in building the reference database.
                Only "Homo_sapiens","Human","Mus_musculus" and "Mouse" can perform cell annotation analysis.

            '--chrM', definition of mitochondrial chromosomes will calculate the number of reads compared to mitochondria,
                'auto' will recognize in 'chrM,MT,chrMT,mt,Mt'.
                automatically obtain the genes located on mitochondria and generate the file mtgene.list.

            '--noindex', if the database has been built using STAR, add this parameter will skip this step and only generate the ref.json file.

            Example:
                %s mkref --fasta /database/genome.fasta --ingtf /database/genes.gtf --species Homo_sapiens --chrM MT --genomeDir /database --threads 10
            '''%type

        elif pipe == 'run':
            help_text = '''
            Analyze sequencing data from single-cell libraries, including cDNA and oligo libraries. 
            This process involves quality control, filtering, alignment, annotation, 
            bead-based cell merging, and obtaining matrix of gene expression for each cell.
            Downstream analysis includes dimensionality reduction, clustering, and annotation analysis.

            '--cDNAfastq1', '--cDNAfastq2', '--oligofastq1', '--oligofastq2'
                Multiple raw FASTQ files should be separated by commas and belong to the same sequencing library.
                The order of the cDNA or oligo R1/R2 fastq files must be consistent.

            '--chemistry', '--darkreaction', '--customize'
                '--chemistry', '--darkreaction', recommend using automatic detection for settings.
                cDNA or oligo libraries should have consistent dark cycles when multiple FASTQ files are used.
                If manual configuration of reagent version and dark cycles is necessary, 
                two parameters should be set simultaneously. Reagent versions include "scRNAv1HT" and "scRNAv2HT". 
                Dark cycles for cDNA and oligo libraries should be separated by commas, for example "R1,R1R2", "R1,R1", "unset,unset", etc.
                '--customize', enable custom library structures or white-list information to be used. 
            '''
        elif pipe == 'multi':
            help_text = '''
            Generate shell scripts for running the "%s run" command on multiple samples.
            All samples should be from the same species or the same reference database.
            '''%type

        else:
            help_text = '''
        '''

    if category == 'atac':
        if pipe == 'mkgtf':
            help_text = '''
            Filter the gene types in a GTF annotation file. 
            
            '--include', choose which gene types to keep by filtering, the types to keep depends on your research,
                    which is included by default:
                     protein_coding, lncRNA, lincRNA, antisense, IG_C_gene, IG_D_gene, 
                     IG_J_gene, IG_LV_gene, IG_V_gene, IG_V_pseudogene, IG_J_pseudogene, 
                     IG_C_pseudogene,TR_C_gene, TR_D_gene, TR_J_gene, TR_V_gene 
            
            The action parameter can be set to mkgtf or stat:
            '--action stat', calculate the number of various gene types.
                Example:
                    %s mkgtf --action stat --ingtf genes.gtf --output gtfstat.txt --type gene_biotype

            '--action mkgtf', filter gene types.
                Example:
                    %s mkgtf --ingtf genes.gtf --output genes.filter.gtf --type gene_biotype 
            '''%(type,type)

        elif pipe == 'mkref':
            help_text = '''
            Build reference database.

            '--chrM', definition of mitochondrial chromosomes, 'auto' will recognize in 'chrM,MT,chrMT,mt,Mt'.

            '--noindex', if the database has been built using chromap, add this parameter will skip this step and only generate the ref.json file.

            Example:
                %s mkref --fasta /database/genome.fasta --ingtf /database/genes.gtf --species Homo_sapiens --chrM MT --genomeDir /database --blacklist blacklist.bed 

            '''
        elif pipe == 'run':
            help_text = '''
            Analyze sequencing data from single-cell libraries.
            This process include data filtering, alignment, cell calling,
            and deconvolution, to generate unique fragment file for each cell.
            Downstream analysis include peak calling, dimensionality reduction, and clustering.

            '--fastq1', '--fastq2',
                Multiple raw FASTQ files should be separated by commas and belong to the same sequencing library.
                The order of the R1/R2 fastq files must be consistent.

            '--darkreaction', '--customize'
                '--darkreaction', recommend using automatic detection for settings.
                Multiple FASTQ data for sequencing need to have consistent sequencing lengths and dark cycles. 
                The dark cycles mode can be "R1R2", "R1", "R2", "unset", etc.
                '--customize', enable custom library structures to be used. 
            '''
        elif pipe == 'multi':
            help_text = '''
            Generate shell scripts for running the "%s run" command on multiple samples.
            All samples should be from the same species or the same reference database.
            '''%type
        
        else:
            help_text = '''
            '''

    if category == 'tools':
        if pipe == 'clean':
            help_text = '''
            Clean up intermediate files produced after analysis to reduce storage.

            Example:
                %s clean --name sample1,sample2
            '''%type

        elif pipe == 'mergeraw':
            help_text = '''
            Merge raw_matrix beads based on magnetic bead merging results.

            Example:
                %s mergeraw --rawmatrix raw_matrix --filtermatrix filter_matrix --barcodecell barcodeTranslate_hex.txt
            '''%type
        elif pipe == 'changetag':
            help_text = '''
            Exchange the tag information in bam in pairs.

            Example:
                %s changetag --inbam anno_decon_sorted.bam --outbam out.velocyto.bam
            '''%type

        else:
            help_text = '''
        '''
    return help_text
