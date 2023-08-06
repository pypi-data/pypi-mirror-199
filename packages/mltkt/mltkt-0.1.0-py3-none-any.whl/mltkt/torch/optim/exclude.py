from pytorch_lightning import Trainer


def exclude_from_wt_decay(named_params, skip_list=None):
    params = []
    excluded_params = []

    if skip_list is None:
        skip_list = ['bias', 'bn']

    for name, param in named_params:
        if not param.requires_grad:
            continue
        elif any(layer_name in name for layer_name in skip_list):
            excluded_params.append(param)
        else:
            params.append(param)

    return [
        {
            'params': params,
        },
        {
            'params': excluded_params,
            'weight_decay': 0.
        },
    ]


def exclude_from_lr_schedule(named_params, skip_list=None):
    params = []
    excluded_params = []

    if skip_list is None:
        skip_list = ['predictor']

    for name, param in named_params:
        if not param.requires_grad:
            continue
        elif any(layer_name in name for layer_name in skip_list):
            excluded_params.append(param)
        else:
            params.append(param)

    return [
        {
            'params': params,
        },
        {
            'params': excluded_params,
        },
    ]


def get_global_batch_size(trainer: Trainer) -> int:
    assert trainer.accumulate_grad_batches == 1
    return len(trainer.accelerator_connector.parallel_devices) * trainer.num_nodes * trainer.datamodule.batch_size
