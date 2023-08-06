import logging

import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import gammalearn.utils as utils
import ot


def cross_entropy_loss(output, target, weight):
    return F.cross_entropy(output, target.long(), weight)


def cross_entropy_loss_nn(output, target):
    return nn.CrossEntropyLoss(ignore_index=-1)(output, target.long())


def nll_nn(output, target):
    return nn.NLLLoss(ignore_index=-1)(output, target.long())


def angular_separation_loss(reduce='mean'):

    def loss_function(output, target):
        """
        Compute the mean angular separation loss between 2 directions
        Parameters
        ----------
        output (Tensor) : output of the net for direction regression
        target (Tensor) : labels for direction regression

        Returns
        -------
        Loss
        """
        logger = logging.getLogger('angular separation loss')
        logger.debug('output size : {}'.format(output.size()))
        try:
            assert output.size() == target.size()
        except AssertionError as err:
            logger.exception('Output and target shapes must be the same but are {} and {}'.format(output.size(),
                                                                                                  target.size()))
            raise err

        alt1 = output[:, 0]
        try:
            assert alt1.data.nelement() > 0
        except AssertionError as err:
            logger.exception('reconstructed alt must have at least 1 element but have {}'.format(alt1.data.nelement()))
            raise err
        try:
            assert not np.isnan(np.sum(alt1.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('alt1 has NaN value(s) : {}'.format(alt1.data))
            raise err
        logger.debug('mean on {} elements'.format(alt1.data.nelement()))

        az1 = output[:, 1]
        try:
            assert not np.isnan(np.sum(az1.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('az1 has NaN value(s) : {}'.format(az1.data))
            raise err

        alt2 = target[:, 0]
        try:
            assert not np.isnan(np.sum(alt2.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('alt2 has NaN value(s) : {}'.format(alt2.data))
            raise err

        az2 = target[:, 1]
        try:
            assert not np.isnan(np.sum(az2.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('az2 has NaN value(s) : {}'.format(az2.data))
            raise err
        loss_cos = (torch.mul(torch.mul(alt1.cos(), alt2.cos()), (az1 - az2).cos()) + torch.mul(alt1.sin(), alt2.sin()))

        try:
            assert not np.isnan(np.sum(loss_cos.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('loss_cos has NaN value(s) : {}'.format(loss_cos.data))
            raise err
        # the loss_coss needs to be < 1 for the gradient not to be inf
        loss = loss_cos.clamp(min=-0.999999, max=0.999999).acos()
        if reduce == 'mean':
            loss = loss.sum() / alt1.data.nelement()
        elif reduce == 'sum':
            loss = loss.sum()
        try:
            assert not np.isnan(np.sum(loss.data.cpu().numpy()))
        except AssertionError as err:
            logger.exception('loss has NaN value(s) : {}'.format(loss.data))
            raise err

        return loss
    return loss_function


# From https://github.com/kornia/kornia/blob/master/kornia/losses/focal.py
def one_hot(labels, num_classes, device=None, dtype=None, eps=1e-6):
    r"""Converts an integer label 2D tensor to a one-hot 3D tensor.
    Args:
        labels (torch.Tensor) : tensor with labels of shape :math:`(N, H, W)`,
                                where N is batch siz. Each value is an integer
                                representing correct classification.
        num_classes (int): number of classes in labels.
        device (Optional[torch.device]): the desired device of returned tensor.
         Default: if None, uses the current device for the default tensor type
         (see torch.set_default_tensor_type()). device will be the CPU for CPU
         tensor types and the current CUDA device for CUDA tensor types.
        dtype (Optional[torch.dtype]): the desired data type of returned
         tensor. Default: if None, infers data type from values.
        eps
    Returns:
        torch.Tensor: the labels in one hot tensor.
    """
    if not torch.is_tensor(labels):
        raise TypeError("Input labels type is not a torch.Tensor. Got {}"
                        .format(type(labels)))
    if not len(labels.shape) == 1:
        raise ValueError("Invalid depth shape, we expect B. Got: {}"
                         .format(labels.shape))
    if not labels.dtype == torch.int64:
        raise ValueError(
            "labels must be of the same dtype torch.int64. Got: {}" .format(
                labels.dtype))
    if num_classes < 1:
        raise ValueError("The number of classes must be bigger than one."
                         " Got: {}".format(num_classes))
    batch_size = labels.shape[0]
    one_h = torch.zeros(batch_size, num_classes,
                        device=device, dtype=dtype)
    return one_h.scatter_(1, labels.unsqueeze(1), 1.0) + eps


def focal_loss(x, target, gamma=2.0, reduction='none'):
    r"""Function that computes Focal loss.
    See :class:`~kornia.losses.FocalLoss` for details.
    """
    if not torch.is_tensor(x):
        raise TypeError("Input type is not a torch.Tensor. Got {}"
                        .format(type(x)))

    if not len(x.shape) == 2:
        raise ValueError("Invalid input shape, we expect BxC. Got: {}"
                         .format(x.shape))

    if not x.device == target.device:
        raise ValueError(
            "input and target must be in the same device. Got: {}" .format(
                x.device, target.device))

    # network outputs logsoftmax.

    # create the labels one hot tensor
    target_one_hot = one_hot(target, num_classes=x.shape[1], device=x.device, dtype=x.dtype)

    # compute the actual focal loss
    weight = torch.pow(-torch.exp(x) + 1., gamma)

    focal = - weight * x
    loss_tmp = torch.sum(target_one_hot * focal, dim=1)

    if reduction == 'none':
        loss = loss_tmp
    elif reduction == 'mean':
        loss = torch.mean(loss_tmp)
    elif reduction == 'sum':
        loss = torch.sum(loss_tmp)
    else:
        raise NotImplementedError("Invalid reduction mode: {}"
                                  .format(reduction))
    return loss


class FocalLoss(nn.Module):
    r"""Criterion that computes Focal loss.
    According to [1], the Focal loss is computed as follows:
    .. math::
        \text{FL}(p_t) = -\alpha_t (1 - p_t)^{\gamma} \, \text{log}(p_t)
    where:
       - :math:`p_t` is the model's estimated probability for each class.
    Arguments:
        alpha (float): Weighting factor :math:`\alpha \in [0, 1]`.
        gamma (float): Focusing parameter :math:`\gamma >= 0`.
        reduction (str, optional): Specifies the reduction to apply to the
         output: ‘none’ | ‘mean’ | ‘sum’. ‘none’: no reduction will be applied,
         ‘mean’: the sum of the output will be divided by the number of elements
         in the output, ‘sum’: the output will be summed. Default: ‘none’.
    Shape:
        - Input: :math:`(N, C, H, W)` where C = number of classes.
        - Target: :math:`(N, H, W)` where each value is
          :math:`0 ≤ targets[i] ≤ C−1`.
    Examples:
        >>> N = 5  # num_classes
        >>> args = {"alpha": 0.5, "gamma": 2.0, "reduction": 'mean'}
        >>> loss = FocalLoss(*args)
        >>> x = torch.randn(1, N, 3, 5, requires_grad=True)
        >>> target = torch.empty(1, 3, 5, dtype=torch.long).random_(N)
        >>> output = loss(x, target)
        >>> output.backward()
    References:
        [1] https://arxiv.org/abs/1708.02002
    """

    def __init__(self, alpha=0.5, gamma=2.0, reduction='mean') -> None:
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, x, target):
        return focal_loss(x, target.long(), self.gamma, self.reduction)


class LossComputing:
    def __init__(self, targets, conditional=False, gamma_class=None):
        self.targets = targets.copy()

        self.conditional = conditional
        if self.conditional:
            assert 'class' in self.targets, 'The conditional loss is defined based on particle type'
            assert gamma_class is not None, 'To mask loss, one must provide the class of gamma'

        self.gamma_class = gamma_class

    def add_grad_penalty(self, loss):
        return NotImplementedError

    def compute_loss(self, output, labels, module=None):
        loss = {}
        loss_data = {}

        if self.conditional:
            loss_mask = labels.get('class')
            loss_mask = loss_mask == self.gamma_class

        # 'targets' and 'output' must contain the same keys, but 'labels' may contain more elements, such as a domain
        # key referring to whether it belongs to the source and target datasets. Thus, we need to check if targets and
        # output keys are subset of the labels keys.
        assert (self.targets.keys() == output.keys()) and set(output.keys()).issubset(set(labels.keys())), \
            'All targets must have output and label but targets: {} \n outputs: {} ' \
            '\n labels: {}'.format(self.targets.keys(), output.keys(), labels.keys())

        for k, v in self.targets.items():
            out = output[k]
            lab = labels[k]

            # Check dimensions
            if k in ['energy', 'direction', 'impact']:
                assert out.ndim == lab.ndim, 'output and label must have same number of dimensions for correct ' \
                                             'loss computation but are {} and {}'.format(out.ndim, lab.ndim)
                out_shape = self.targets[k].get('output_shape')
                lab_shape = self.targets[k].get('label_shape', out_shape)

                assert out.shape[-1] == out_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, out.shape[-1], out_shape)
                assert lab.shape[-1] == lab_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, lab.shape[-1], lab_shape)

            # Get loss
            loss_k = v['loss'](out, lab)

            # Compute masked loss
            if k in ['energy', 'direction', 'impact']:
                if self.conditional:
                    loss_mask = loss_mask.to(out.device)
                    assert loss_k.shape[0] == loss_mask.shape[0], 'loss should not be reduced for mask on particle type' \
                                                                'but got {} and {}'.format(loss_k.shape, loss_mask.shape)
                    if loss_k.dim() > 1:
                        cond = [loss_mask.unsqueeze(1) for _ in range(loss_k.shape[1])]
                        cond = torch.cat(cond, dim=1)
                    else:
                        cond = loss_mask
                    assert loss_k.shape == cond.shape, \
                        'loss and mask must have the same shape but are {} and {}'.format(loss_k.shape, cond.shape)
                    loss_k = (loss_k * cond).sum() / cond.sum() if cond.sum() > 0 else torch.tensor(0., device=loss_k.device)

            if k in ['autoencoder']:
                loss_k = torch.mean(loss_k, dim=tuple(torch.arange(loss_k.dim())[1:]))
                loss_data[k] = loss_k.mean()
                loss[k] = loss_k.mean()
            else:
                loss_data[k] = loss_k.mean().detach().item()
                loss[k] = loss_k.mean()

            # Hand-designed loss weight. Requires to be out of the loss balancing scope.
            if v.get('loss_weight') is not None:  # If loss_weight is set in the experiment setting file
                if v.get('mt_balancing') is None or not v['mt_balancing']:  # If no loss balancing
                    if isinstance(v['loss_weight'], utils.BaseW):
                        if not v['loss_weight'].apply_on_grads:
                            loss_weight = v['loss_weight'].get_weight(module.trainer)
                            loss[k] *= loss_weight
                    else:
                        loss_weight = v['loss_weight']
                        loss[k] *= loss_weight

        return loss, loss_data


class MultilossBalancing(nn.Module):
    r"""
    Create the function to compute the loss in case of multi regression experiment with homoscedastic uncertainty
    loss balancing. See the paper https://arxiv.org/abs/1705.07115.
    In the paper the total loss is defined as:
    .. math::
        \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{2\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2

    but in https://github.com/yaringal/multi-task-learning-example/blob/master/multi-task-learning-example.ipynb as:
    .. math::
        \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -1

    should not make a big difference. However, we introduce logvar_coeff and penalty to let the user choose:
    .. math::
        \text{L} = \sum_i \frac{1}{\{logvar_coeff}\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -\text{penalty}

    Parameters
    ----------
    targets (dict): The loss dictionary defining for every objectives of the experiment the loss function and its
    initial log_var

    Returns
    -------
    The function to compute the loss
    """
    def __init__(self, targets, logvar_coeff=None, penalty=0):
        super(MultilossBalancing, self).__init__()
        self.targets = targets.copy()
        self.precisions = {}

        for k, v in self.targets.items():
            if not v['mt_balancing']:
                # Only keep targets with parameter 'mt_balancing' set to True
                self.targets.pop(k)
            else:
                # Initialize precisions
                self.precisions[k] = 1.

        self.penalty = penalty
        self.log_vars = nn.Parameter(torch.rand(len(self.targets.keys())), requires_grad=True)

        if logvar_coeff is None:
            # If the log var coeffs have not been initialized in the experiment setting file, initialize them to 1.
            self.logvar_coeff = torch.ones(self.log_vars.shape)
        else:
            self.logvar_coeff = torch.tensor(logvar_coeff)
        assert len(self.log_vars) == len(self.logvar_coeff), \
            'The number of logvar coefficients must be equal to the number of logvars'

        with torch.no_grad():
            for i, key in enumerate(self.targets.keys()):
                self.log_vars[i] = self.targets[key]['loss_weight']

    def forward(self, all_loss):
        all_loss_mt = all_loss.copy()

        for i, (k, v) in enumerate(self.targets.items()):
            self.precisions[k] = torch.exp(- self.log_vars[i]) * self.logvar_coeff[i]
            loss = self.precisions[k] * all_loss[k] + self.log_vars[i] - self.penalty
            all_loss_mt[k] = loss

        return all_loss_mt


class DeepJDOTLoss(nn.Module):
    """
    Implementation of the Wasserstein loss using the Optimal Transport theory.
    From the DeepJDOT article https://arxiv.org/abs/1803.10081.

    Parameters
    ----------
    batch_size: (int) The batch size used during training and validation. It must be constant throughout the training as
    the optimal transport matrix Gamma is of size batch_size*batch_size and thus requires the optimizer to set the
    drop_last parameter to True.
    entropic_regularization: (bool) Whether to use entropic regularization to compute gamma. Default is False.
    """

    def __init__(self, batch_size, entropic_regularization=False):
        super(DeepJDOTLoss, self).__init__()
        self.batch_size = batch_size  # The batch size indicates the size of the gamma transport plan
        self.entropic_regularization = entropic_regularization  # Makes gamma less sparse
        self.gamma = torch.zeros(batch_size, batch_size, dtype=torch.float32)  # Optimal transport plan array
        self.cost = torch.zeros(batch_size, batch_size, dtype=torch.float32)  # Cost array
        self.train = True  # In train mode, update gamma and cost, whereas in eval mode only compute cost
        self.device = None

    def set_train_context(self):
        # Gamma and cost will be updated.
        self.train = True

    def set_eval_context(self):
        # Gamma and cost will not be updated.
        self.train = False

    def update_gamma(self):
        with torch.no_grad():
            cost = self.cost.detach().cpu().numpy()

            if not self.entropic_regularization:
                gamma = ot.emd(ot.unif(self.batch_size), ot.unif(self.batch_size), cost)
            else:
                # Entropic regularization allows the gamma matrix to be less sparse.
                gamma = ot.optim.gcg(
                    ot.unif(self.batch_size),
                    ot.unif(self.batch_size),
                    cost,
                    1e-3,
                    1e-1,
                    self.f,
                    self.df
                )

        self.gamma = torch.tensor(gamma, dtype=torch.float32).to(self.device)

    def update_cost(self, latent_features_source, latent_features_target):
        latent_features_source = latent_features_source.view(self.batch_size, -1)
        latent_features_target = latent_features_target.view(self.batch_size, -1)
        self.device = latent_features_source.device
        self.cost = torch.cdist(latent_features_source, latent_features_target, p=2)**2  # ||g(x_i^s) - g(x_j^t)||²

    def compute_loss(self):
        return (self.gamma * self.cost).sum()

    def f(self, G):
        # For entropic regularization
        return 0.5 * np.sum(G ** 2)

    def df(self, G):
        # For entropic regularization
        return G

    def forward(self, latent_features_source, latent_features_target):
        # Find optimal coupling (eq. 8)
        if self.train:
            self.update_cost(latent_features_source, latent_features_target)
            self.update_gamma()

        # Compute loss (eq. 9)
        return self.compute_loss()


class DeepCORALLoss(nn.Module):
    """
    Implementation of the CORAL loss.
    From the DeepCORAL article https://arxiv.org/abs/1607.01719.

    Parameters
    ----------
    """

    def __init__(self):
        super(DeepCORALLoss, self).__init__()

    def forward(self, ds: torch.Tensor, dt: torch.Tensor) -> torch.Tensor:
        ds = ds.flatten(start_dim=1)  # Source features of size [ns, d]
        dt = dt.flatten(start_dim=1)  # Target features of size [nt, d]

        mean_s = ds.mean(0, keepdim=True)
        mean_t = dt.mean(0, keepdim=True)
        cent_s = ds - mean_s
        cent_t = dt - mean_t
        cov_s = torch.mm(cent_s.t(), cent_s) / (len(ds) - 1)
        cov_t = torch.mm(cent_t.t(), cent_t) / (len(dt) - 1)
        mean_diff = (mean_s - mean_t).pow(2).mean()
        cov_diff = (cov_s - cov_t).pow(2).mean()

        return mean_diff + cov_diff


class GradNormBalancing(nn.Module):
    """
    Compute the loss in case of multi regression experiment
    Parameters
    ----------
    criterions (dict): The loss dictionary defining for every objective of the experiment the loss function and its
    initial log_var

    Returns
    -------
    The function to compute the loss
    """
    def __init__(self, targets, conditional=False, gamma_class=None, last_common_layer=None, alpha=0):
        super(GradNormBalancing, self).__init__()

        assert last_common_layer is not None, 'The last common layer must be provided'

        self.targets = targets
        self.conditional = conditional
        if self.conditional:
            assert 'class' in self.targets, 'The conditional loss is defined based on particle type'
            assert gamma_class is not None, 'To mask loss, one must provide the class of gamma'
        self.gamma_class = gamma_class
        self.task_number = len(self.targets)
        self.last_common_layer = last_common_layer
        self.alpha = alpha
        self.weights = nn.Parameter(torch.ones(self.task_number))
        self.initial_losses = torch.zeros(self.task_number)
        self.t0 = True

    def forward(self, output, labels):
        """
        Compute the loss of the batch
        Parameters
        ----------
        output: result of the forward pass of a mini-batch in the network
        labels: mini-batch of labels

        Returns
        -------
        The Loss tensor, and the loss data of each objective
        """
        loss_data = {}
        all_loss = []
        batch_size = next(iter(output.values())).shape[0]
        device = next(iter(output.values())).device
        if self.conditional:
            loss_mask = labels.get('class')
            loss_mask = loss_mask == self.gamma_class
        else:
            loss_mask = torch.ones(batch_size, device=device)

        assert self.targets.keys() == output.keys() == labels.keys(), \
            'All targets must have output abd label but targets: {} \n outputs: {}' \
            ' \n labels: {}'.format(self.targets.keys(), output.keys(), labels.keys())

        for i, (k, v) in enumerate(self.targets.items()):
            out = output[k]
            lab = labels[k]

            if k not in ['class', 'generative']:
                assert out.ndim == lab.ndim, 'output and label must have same number of dimensions for correct ' \
                                             'loss computation but are {} and {}'.format(out.ndim, lab.ndim)
                out_shape = self.targets[k].get('output_shape')
                lab_shape = self.targets[k].get('label_shape', out_shape)

                assert out.shape[-1] == out_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, out.shape[-1], out_shape)
                assert lab.shape[-1] == lab_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, lab.shape[-1], lab_shape)

            loss = v['loss'](out, lab)
            if k != 'class':
                if self.conditional:
                    assert loss.shape[0] == loss_mask.shape[0], 'loss should not be reduced for mask on particle type' \
                                                                'but got {} and {}'.format(loss.shape, loss_mask.shape)
                    if loss.dim() > 1:
                        cond = [loss_mask.unsqueeze(1) for _ in range(loss.shape[1])]
                        cond = torch.cat(cond, dim=1)
                    else:
                        cond = loss_mask
                    assert loss.shape == cond.shape, \
                        'loss and mask must have the same shape but are {} and {}'.format(loss.shape, cond.shape)
                    loss = (loss * cond).sum() / cond.sum() if cond.sum() > 0 else torch.tensor(0., device=device)
                else:
                    loss = loss.mean()
            if self.t0:
                self.initial_losses[i] = loss.detach()
            all_loss.append(loss)
            loss_data[k] = loss.detach()
        self.t0 = False

        return all_loss, loss_data
