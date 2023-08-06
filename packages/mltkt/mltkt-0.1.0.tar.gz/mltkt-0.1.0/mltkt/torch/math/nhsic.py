import torch


# def dist_mat(x: torch.Tensor) -> torch.Tensor:
#     """ distance matrix
#     """
#     r = torch.sum(x ** 2, dim=1, keepdim=True)
#     a = x @ x.T
#     D = r - 2 * a + r.T
#     print(f"{torch.min(D)}")
#     D = torch.abs(D)
#     return D


def sq_dist_mat(x: torch.Tensor) -> torch.Tensor:
    """ distance matrix
    """
    return torch.sum((x[None, :, :] - x[:, None, :]) ** 2, dim=2)


def kernel_mat(x: torch.Tensor, sigma: float) -> torch.Tensor:
    """ kernel matrix baker
    """
    m = x.shape[0]
    H = torch.eye(m).type_as(x) - (1 / m) * torch.ones((m, m)).type_as(x)
    Dxx = sq_dist_mat(x)

    variance = 2 * sigma * sigma * x.shape[1]
    Kx = torch.exp(-Dxx / variance)  # kernel matrices

    Kxc = Kx @ H

    return Kxc


def hsic_normalized_cca(x: torch.Tensor, y: torch.Tensor, sigma: float, eps: float = 1e-5) -> torch.Tensor:
    """
    """
    m = x.shape[0]
    Kxc = kernel_mat(x, sigma=sigma)
    Kyc = kernel_mat(y, sigma=sigma)

    K_I = torch.eye(m).type_as(x)

    Kxc_i = torch.inverse(Kxc + eps * m * K_I)
    Kyc_i = torch.inverse(Kyc + eps * m * K_I)

    Rx = Kxc @ Kxc_i
    Ry = Kyc @ Kyc_i

    Pxy = torch.sum(Rx * Ry.T)

    return Pxy


