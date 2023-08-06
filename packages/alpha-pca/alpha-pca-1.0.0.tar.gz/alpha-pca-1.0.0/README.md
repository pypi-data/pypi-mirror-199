# Alpha-PCA

Alpha-PCA is more robust to outliers than standard PCA. \
Standard PCA is a special case of alpha PCA (when alpha=1).

* [Usage](#usage)

## Usage

The model is inherited from a sklearn module and works the same way as the [standard PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html). \
It also supports [PyTorch](https://pytorch.org/) tensors (on cpu and GPU).

```python
from alpha_pca import AlphaPCA
import torch 

X = torch.randn(16, 10) # also works with numpy
pca = AlphaPCA(n_components=5, alpha=0.7, random_state=123) # alpha=1 -> standard PCA
pca.fit(X)

# to project X in the latent space
X_transformed = pca.transform(X) # (16, 10) -> (16, 5)

# fit inverse
X_ = pca.inverse_transform(X_transformed) # (16, 5) -> (16, 10)

# directly approximate X_ == inverse_transform(transform(X))
X_ = pca.approximate(X) # (16, 10) -> (16, 10)

# Find the optimal alpha via a reconstruction loss
best_alpha = pca.compute_optimal_alpha(X, n_components=5)
```
