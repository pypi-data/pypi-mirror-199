from torchvision.transforms import functional as F

def denormalize(tensor, mean, std):
    return F.normalize(
            tensor, 
            mean=[-m/s for m, s in zip(mean, std, strict=True)], 
            std=[1/s for s in std], 
    ).clamp(0, 1)

def denormalize_(tensor, mean, std):
    return F.normalize(
            tensor, 
            mean=[-m/s for m, s in zip(mean, std, strict=True)], 
            std=[1/s for s in std], 
            inplace=True
    ).clamp_(0, 1)

class Denormalize(object):
    def __init__(self, mean, std, inplace=False):
        self.mean = mean
        self.std = std
        self.inplace = inplace

    def __call__(self, tensor):
        if self.inplace:
            return denormalize(tensor, self.mean, self.std)
        else:
            return denormalize_(tensor, self.mean, self.std)
