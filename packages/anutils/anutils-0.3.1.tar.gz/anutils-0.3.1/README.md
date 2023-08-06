# anutils
ML and single cell analysis utils.  

## installation
```
pip install anutils
```
**NOTE**: To use `anutils.scutils.sc_cuda`, you need to install rapids first. see [rapids.ai](https://rapids.ai/start.html) for details. For example, to install rapids on a linux machine with cuda 11, you can run:  
```bash
pip install cudf-cu11 dask-cudf-cu11 --extra-index-url=https://pypi.nvidia.com
pip install cuml-cu11 --extra-index-url=https://pypi.nvidia.com
pip install cugraph-cu11 --extra-index-url=https://pypi.nvidia.com
```

## usage

### general utils: `anutils.*`

e.g., reload module
```python
import sys
sys.path.append('/path/to/some/packaege/')
import some_package

# change some_package.sub_module.func, recursive reload needed
from anutils import rreload
rreload(some_package, max_depth=2)
```


### single cell utils: `anutils.scutils.*`

#### plotting

```python
from anutils import scutils as scu

# a series of embeddings grouped by disease status
scu.pl.embeddings(adata, basis='X_umap', groupby='disease_status', **kwargs) # kwargs for sc.pl.embedding

# enhanced dotplot with groups in hierarchical order
scu.pl.dotplot(adata, var_names, groupby, **kwargs) # kwargs for sc.pl.dotplot
```
#### cuda-accelerated scanpy functions
NOTE: to use these functions, you need to install rapids first. see [installation](#installation) for details.
```python
from anutils.scutils import sc_cuda as cusc

# 10-100 times faster than `scanpy.tl.leiden`
cusc.sc.leiden(adata, resolution=0.5, key_added='leiden_0.5')

# 10-100 times faster than `scib.metrics.silhouette`
cusc.sb.silhouette(adata, group_key, embed)
```

## machine learning utils:
```python
import anutils.mlutils as ml

# to be added
```
