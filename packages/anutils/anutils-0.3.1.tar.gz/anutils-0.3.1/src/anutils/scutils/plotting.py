import matplotlib.pyplot as plt
import scanpy as sc
import numpy as np
import pandas as pd
import seaborn as sns


def init_fig_params():
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='Helvetica')
    plt.rcParams['pdf.fonttype'] = 42
    # sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    # sc.logging.print_header()
    sc.set_figure_params(dpi=120, facecolor='w', frameon=True, figsize=(4, 4))
    # %config InlineBackend.figure_format='retina'
    # %matplotlib inline


def embeddings(group_adata_by,
               replicate_key=None,
               groups_order=None,
               ncols=3,
               figsize=None,
               **embedding_kwargs):
    """plot embeddings of adata grouped by group_adata_by

    Parameters
    ----------
    group_adata_by : str
        a column in adata.obs
    replicate_key : str, optional
        a column in adata.obs, by default None. If not None, the number of replicates will be shown in the title
    groups_order : iterable, optional
        a ordered list of keys in `adata.obs[group_adata_by]`, by default None
    ncols : int, optional
        ncols, by default 3
    figsize : 2 length tuple, optional
        figsize, by default `(5 * ncols, 5 * nrows)`
    embedding_kwargs : dict
        kwargs for sc.pl.embedding. `adata` is required. if `basis` is not provided, `X_umap` will be used.

    Returns
    -------
    fig
        the fig object
    """
    adata = embedding_kwargs['adata']
    if 'basis' not in embedding_kwargs:
        embedding_kwargs['basis'] = 'X_umap'

    # reorder
    indices = adata.obs.groupby(group_adata_by).indices
    if groups_order is None:
        groups_order = indices.keys()
    indices = {k: indices[k] for k in groups_order}
    # plot
    N = adata.obs[group_adata_by].nunique()
    nrows = (N - 1) // ncols + 1
    if figsize is None:
        figsize = (5 * ncols, 5 * nrows)
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=figsize)

    if 'color' in embedding_kwargs:
        if isinstance(embedding_kwargs['color'], str):
            embedding_kwargs['color'] = [embedding_kwargs['color']]
        # freeze the colors for categorical variables to make sure the colors are
        # the same for different plots. (scanpy will change the colors for categorical
        # variables if the number of categories changes when subseting the adata)
        # sc.pl.embedding(**embedding_kwargs, show=False)

    for i, (k, v) in enumerate(indices.items()):
        ad = adata[v, :]
        # scanpy changes the number of categories when subseting the adata, so we need
        # to reset the categories
        if 'color' in embedding_kwargs:
            for c in embedding_kwargs['color']:
                # if it is categorical
                if adata.obs[c].dtype.name == 'category':
                    ad.obs[c].cat.set_categories(adata.obs[c].cat.categories, inplace=True)

        title = k
        if replicate_key is not None:
            title += f' (n={ad.obs[replicate_key].nunique()})'
        kwargs = embedding_kwargs.copy()
        kwargs.pop('adata')
        sc.pl.embedding(
            ad,
            **kwargs,
            ax=axes[i // ncols, i % ncols],
            show=False,
            title=title,
        )
    # remove empty axes
    while i < ncols * nrows - 1:
        i += 1
        axes[i // ncols, i % ncols].axis('off')
    # adjust axes lims to make them equal
    xlims = np.array([ax.get_xlim() for ax in axes.flat])
    ylims = np.array([ax.get_ylim() for ax in axes.flat])
    xlims = np.array([xlims[:, 0].min(), xlims[:, 1].max()])
    ylims = np.array([ylims[:, 0].min(), ylims[:, 1].max()])
    for ax in axes.flat:
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)

    # fig.tight_layout()
    return fig


def barplot(df,
            key='celltype',
            color=sns.color_palette("tab20"),
            width=0.6,
            figsize=(16, 6),
            save=False):
    fig = plt.figure(figsize=figsize)
    ax = sns.barplot(x=key, y='counts', data=df, color=color, saturation=1)
    plt.xlabel('donor', fontsize=22, labelpad=8)
    plt.ylabel('Cell Number', fontsize=22, labelpad=8)
    plt.xticks(rotation=45, fontsize=20, ha='right')
    plt.yticks([0, 5000, 10000, 15000], rotation=0, fontsize=20)
    plt.title('', fontsize=25, ha='center')

    def change_width(ax, new_value):
        for patch in ax.patches:
            current_width = patch.get_width()
            diff = current_width - new_value

            # we change the bar width
            patch.set_width(new_value)

            # we recenter the bar
            patch.set_x(patch.get_x() + diff * .5)

    change_width(ax, width)

    if save:
        plt.savefig(save, dpi=100, format='pdf', bbox_inches='tight')


def dotplot(adata, groupby, var_names, inplace=False, **dotplot_kwargs):
    if not inplace:
        adata = adata.copy()
    if 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = np.e
    adata.obs[groupby] = adata.obs[groupby].astype('category')
    sc.tl.dendrogram(adata, groupby=groupby, var_names=var_names)
    sc.pl.dotplot(adata, groupby=groupby, var_names=var_names, dendrogram=True, **dotplot_kwargs)