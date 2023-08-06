import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scanpy as sc
import celltypist
import pandas as pd
import seaborn as sns
import math
from dnbc4tools.__init__ import __root_dir__

class CellDataAnalyzer:
    """Tsingle-cell analysis workflows
    func:
        pp_basicfilter
        pp_doubletdetect
        pp_hvgs
        pp_reduce
        pp_cluster
        pp_deg
        pp_autoanno
    """

    def __init__(self,
                adata):
        self.adata = adata
    
    
    def _pp_qc(self, 
            mtgene: list = None,):
        is_mt = self.adata.var_names.str.startswith('MT-', 'mt-')
        if mtgene:
            is_mt = is_mt | self.adata.var_names.isin(mtgene)
        self.adata.var['mt']  = is_mt  
        sc.pp.calculate_qc_metrics(
            self.adata, 
            qc_vars=['mt'], 
            percent_top=None, 
            log1p=False, 
            inplace=True
            )

    def _pp_basicfilter(self,
            min_cells: int= 3,
            pct_counts_mt: bool = True ,
            filter_maxgene : bool = True,):
        if pct_counts_mt:
            threshold = math.ceil(self.adata.obs.pct_counts_mt.quantile(0.95))
            self.adata = self.adata[self.adata.obs.pct_counts_mt <= threshold, :]
            #self.adata = self.adata[self.adata.obs.pct_counts_mt < pct_counts_mt, :]
        if filter_maxgene:
            threshold = math.ceil(self.adata.obs.n_genes_by_counts.quantile(0.95))
            #sc.pp.filter_cells(self.adata, max_genes = int(threshold))
            self.adata = self.adata[self.adata.obs.n_genes_by_counts <= threshold, :]
        if min_cells:
            sc.pp.filter_genes(self.adata, min_cells=min_cells)
        
        mediannum = int(self.adata.obs["n_genes_by_counts"].median())
        if mediannum >= 500:
            thres_gene = 200
        elif mediannum >= 200:
            thres_gene = 50
        else:
            thres_gene = 0
        sc.pp.filter_cells(self.adata, min_genes=thres_gene)
        
        
    def _pp_scanpy_doubletdetect(self,
                                doublet_thresthod: float = None,
                                doublet_rate: float = 0.05
                                ):
        scrub_doublet = sc.external.pp.scrublet_simulate_doublets(
            self.adata,
            sim_doublet_ratio = 2.0,
            synthetic_doublet_umi_subsampling = 1.0,
        )
        sc.external.pp.scrublet(
            self.adata,
            scrub_doublet,
            expected_doublet_rate=doublet_rate,
            threshold = doublet_thresthod,
            copy=False
            )
        self.adata = self.adata[self.adata.obs['predicted_doublet'] != True]

    def _pp_hvgs(self,
                min_mean: float = 0.0125,
                max_mean: float = 3,
                min_disp: float = 0.5,
                hvgs: int = 2000,
                normalization: str = 'LogNormalize',
                flavor: str = 'seurat_v3'
                ):

            if normalization == 'LogNormalize':
                sc.pp.normalize_total(self.adata, target_sum=1e4)
                sc.pp.log1p(self.adata)
            if flavor == 'seurat_v3':
                sc.pp.highly_variable_genes(self.adata,flavor='seurat_v3',n_top_genes=hvgs)
            else:
                sc.pp.highly_variable_genes(self.adata, min_mean=min_mean, max_mean=max_mean,
                                        min_disp=min_disp, flavor=flavor, n_top_genes=hvgs)
            self.adata.raw = self.adata
            sc.pp.scale(self.adata, max_value=10)

    def _pp_reduce(self,
                n_comps: int = 50,
                svd_solver: str = 'arpack',
                use_highly_variable: bool = True,):
        try:        
            sc.tl.pca(self.adata, n_comps=n_comps, svd_solver=svd_solver,
                    use_highly_variable=use_highly_variable)
        except Exception as e:
            cell_num = len(self.adata.obs.index)
            n_comps = cell_num - 1
            sc.tl.pca(self.adata, n_comps=n_comps, svd_solver=svd_solver,
                    use_highly_variable=use_highly_variable)

    def _pp_cluster(self,
                neighbors: int = 15,
                n_pcs: int = 30,
                method: str = 'umap',
                spread: float = 1.0,
                min_dist: float = 0.25,
                perplexity: int = 30,
                learning_rate: int = 1000,
                cluster_method: str = 'louvain',
                resolution: int = 0.8):
        try:
            sc.pp.neighbors(self.adata, n_neighbors=neighbors, n_pcs=n_pcs,method='umap',metric='euclidean')
        except Exception as e:
            n_comp = len( self.adata.uns['pca']['variance'])
            sc.pp.neighbors(self.adata, n_neighbors=neighbors, n_pcs=n_comp)
        if method == 'umap':
            sc.tl.umap(self.adata, min_dist=min_dist, spread=spread)
        if method == 'tsne':
            sc.tl.tsne(self.adata, perplexity=perplexity,
                        learning_rate=learning_rate)
        if cluster_method == 'leiden':
            sc.tl.leiden(self.adata, resolution=resolution)
        if cluster_method == 'louvain':
            sc.tl.louvain(self.adata, resolution=resolution)

    def _pp_deg(self,
               groupby: str = 'leiden/louvain',
               method: str = 'wilcoxon',
               n_genes: int = 200,
               ):
        
        self.adata.uns['log1p'] = {'base': None}
        if groupby == 'leiden/louvain':
            groupby = 'louvain' if 'louvain' in self.adata.obs_keys() else 'leiden'
        sc.tl.rank_genes_groups(self.adata, groupby ,pts = True,
                                method=method, n_genes=n_genes)

    def _pp_autoanno(self,
                    species: str = None
                    ):
        celltypist.models.models_path = '%s/config/cellAnno'%__root_dir__
        if species == 'Human':
            modeltype = 'Immune_All_Low.pkl'
        elif species == 'Mouse':
            modeltype = 'Adult_Mouse_Gut.pkl'
        else:
            modeltype = None
        
        predictions = celltypist.annotate(
            self.adata, model = modeltype , majority_voting=True, over_clustering = self.adata.obs['louvain'].astype(str))
        self.adata= predictions.to_adata()

def mtgene_file_read(mtgenefile):
    mtgene = []
    df = pd.read_csv(mtgenefile, header=None)
    for line in list(df.iloc[:, 0]):
        line = line.strip()
        mtgene.append(line)
    return mtgene

def get_markers(adata,
        cutoff: float = 0.05,
            ):
    markertable = sc.get.rank_genes_groups_df(adata,group=None)
    markertable = markertable[~pd.isnull(markertable['logfoldchanges'])]
    markertable.columns = ['cluster','gene','score','avg_log2FC','p_val','p_val_adj','pct.1','pct.2']
    markertable = markertable.round({'avg_log2FC':3,'pct.1':3,'pct.2':3})
    markertable = markertable.loc[markertable['p_val_adj'] < cutoff, ]
    markertable = markertable.loc[markertable['avg_log2FC'] > 0].sort_values('cluster', ascending=True).groupby('cluster').head(30)
    return markertable

def get_cluster(adata,
        cluster_method: str = 'louvain',
                ):
    umap_matrix = adata.obsm.to_df()[['X_umap1','X_umap2']]
    if 'majority_voting' in adata.obs:
        obs_data = adata.obs[['n_genes_by_counts','total_counts','%s'%cluster_method,'majority_voting']]
    else:
        obs_data = adata.obs[['n_genes_by_counts','total_counts','%s'%cluster_method]]
    
    merge_data = pd.concat([obs_data,umap_matrix],axis=1)
    merge_data['Cluster_number'] =merge_data['%s'%cluster_method].map(merge_data['%s'%cluster_method].value_counts(ascending=False))
    merge_data['Cluster'] = merge_data['%s'%cluster_method].astype(str) + ' CellsNum: ' + merge_data['Cluster_number'].astype(str)
    merge_data = merge_data.drop(['Cluster_number'],axis=1)
    if 'majority_voting' in merge_data:
        merge_data['Predict_number'] =merge_data['majority_voting'].map(merge_data['majority_voting'].value_counts(ascending=False))
        merge_data['Predicted cell type'] = merge_data['majority_voting'].astype(str) + ' : ' + merge_data['Predict_number'].astype(str)
        merge_data = merge_data.drop(['majority_voting'],axis=1)
        merge_data.columns = ['nGene','nUMI','%s'%cluster_method,'UMAP_1','UMAP_2','Cluster','Predict_number','Predicted cell type']
    else:
        merge_data.columns = ['nGene','nUMI','%s'%cluster_method,'UMAP_1','UMAP_2','Cluster']
    merge_data = merge_data.sort_values(by=['%s'%cluster_method],ascending=True)
    return merge_data


def draw_qcfigure(adata,
                  ):
    params = {'figure.figsize': (5, 5),
            'axes.labelsize': 'medium',
            'figure.dpi': 150,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'xtick.labelsize':'medium',
            'ytick.labelsize':'x-small'}
    plt.rcParams.update(params)
    meta = adata.obs

    threshold1 = math.ceil(meta['pct_counts_mt'].quantile(0.995))
    threshold2 = math.ceil(meta['n_genes_by_counts'].quantile(0.995))
    threshold3 = math.ceil(meta['total_counts'].quantile(0.995))
    meta_threshold1 = meta[meta['pct_counts_mt'] <= threshold1]
    meta_threshold2 = meta[meta['n_genes_by_counts'] <= threshold2]
    meta_threshold3 = meta[meta['total_counts'] <= threshold3]

    boxprops = dict(linewidth=1, edgecolor='black',zorder=1)
    whiskerprops = dict(linewidth=1, color='black')
    medianprops = dict(linewidth=1, color='black')
    if meta['pct_counts_mt'].sum() > 0:
        fig, ax = plt.subplots(1,3)
        sns.violinplot(
            y="pct_counts_mt", 
            data=meta_threshold1, 
            color="#7570B3",
            inner=None,
            bw=.2, 
            saturation=1,
            scale="width",
            ax=ax[2],
            cut=0,
            linewidth=0.5
            )
        sns.boxplot(
            y="pct_counts_mt", 
            data=meta, 
            ax=ax[2], 
            width=0.2, 
            color="white",
            fliersize=0,
            showfliers=False,
            boxprops=boxprops, 
            whiskerprops=whiskerprops,
            medianprops=medianprops,
            showcaps=False)
        ax[2].axes.set_ylabel('')
        ax[2].axes.set_xlabel('mito.percent')
    else:
        fig, ax = plt.subplots(1,2)
    sns.violinplot(
        y="n_genes_by_counts", 
        data=meta_threshold2 , 
        color="#1B9E77",
        inner=None,
        bw=.2, 
        saturation=1,
        scale="width",
        ax=ax[0],
        cut=0,
        linewidth=0.5
        )
    sns.boxplot(
        y="n_genes_by_counts", 
        data=meta, 
        ax=ax[0], 
        width=0.2, 
        color="white",
        fliersize=0,
        showfliers=False,
        boxprops=boxprops, 
        whiskerprops=whiskerprops,
        medianprops=medianprops,
        showcaps=False
        )
    ax[0].axes.set_ylabel('')
    ax[0].axes.set_xlabel('genes')

    sns.violinplot(
        y="total_counts", 
        data=meta_threshold3, 
        color="#D95F02",
        inner=None,
        bw=.2, 
        saturation=1,
        scale="width",
        ax=ax[1],
        cut=0,
        linewidth=0.5
        )
    sns.boxplot(
        y="total_counts", 
        data=meta,
        ax=ax[1], 
        width=0.2, 
        color="white",
        fliersize=0,
        showfliers=False,
        boxprops=boxprops, 
        whiskerprops=whiskerprops,
        medianprops=medianprops,
        showcaps=False)
    ax[1].axes.set_ylabel('')
    ax[1].axes.set_xlabel('umis')

    fig.tight_layout()
    return fig
