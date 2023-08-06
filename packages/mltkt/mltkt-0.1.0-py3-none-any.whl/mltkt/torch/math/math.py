import torch


def cov_mean_mat(x: torch.Tensor, bias=False) -> tuple[torch.Tensor, torch.Tensor]:
    """
    get batch co-variance matrix
    :param x: bath_size * number_of_samples * feature_dimension: batch of samples
    :param bias: if use unbiased estimation of the co-variance matrix, true for biased estimation
    :return: bath_size * feature_dimension: batch of co-variance matrix
    """
    assert len(x.shape) == 3

    avg = torch.mean(x, dim=1, keepdim=True)
    cov = x - avg
    cov = cov.transpose(1, 2) @ cov

    if bias:
        cov = cov / x.shape[1]
    else:
        cov = cov / (x.shape[1] - 1)

    return cov, avg.squeeze_(1)


def cov2cor(cov: torch.Tensor, eps=1e-9) -> torch.Tensor:
    std = torch.diagonal(cov, dim1=1, dim2=2).sqrt()
    std = torch.threshold(std, eps, eps)
    inv_std = torch.diag_embed(1 / std, dim1=1, dim2=2)
    cor = inv_std @ cov @ inv_std
    return cor
