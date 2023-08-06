from typing import Union

import numpy as np
import torch


def nn_entropy(x: torch.Tensor) -> torch.Tensor:
    assert len(x.shape) == 2

    # dist_mat = torch.norm(x[None, :, :] - x[:, None, :], dim=2, p=2)
    dist_mat = torch.cdist(x, x, p=2)
    nn_dist_mat = torch.topk(dist_mat, k=2, largest=False, dim=1).values[:, 1]

    # print(dist_mat)

    # filter out zero dist
    nn_dist_mat = nn_dist_mat[nn_dist_mat > 0]

    n = nn_dist_mat.shape[0]
    # d = x.shape[1]

    h = 1 / n * torch.sum(torch.log(n * nn_dist_mat)) + np.log(2) + np.euler_gamma
    # h = digamma(n) - digamma(1) \
    #     + np.log((np.pi ** (d / 2)) / gamma(1 + (d / 2))) \
    #     + d / n * torch.sum(torch.log(nn_dist))

    return h


def nn_dist(x: torch.Tensor, eps=1e-9) -> Union[torch.Tensor, float]:
    assert len(x.shape) == 2

    dist_mat = torch.cdist(x, x, p=2)
    nn_dist_mat = torch.topk(dist_mat, k=2, largest=False, dim=1).values[:, 1]

    nn_dist_mat = nn_dist_mat[nn_dist_mat > 0]

    # filter out zero dist
    if nn_dist_mat.shape[0] == 0:
        return 0

    return torch.mean(torch.log(nn_dist_mat))
