#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
import numpy as np
from mindspore.ops import functional as F
from mindspore.ops import operations as P
from mindspore.common import dtype as mstype
import mindspore as ms
from mindspore import nn
from mindspore._checkparam import Validator as validator

from msadapter.pytorch.nn.parameter import Parameter
import msadapter.pytorch.nn.functional as ms_torch_nn_func
from msadapter.pytorch.tensor import Tensor, tensor, cast_to_ms_tensor, cast_to_adapter_tensor
from msadapter.utils import unsupported_attr
from msadapter.pytorch.common._inner import _inplace_assign, _inplace_limit_pynative
from .module import Module

__all__ = ['ReLU', 'Hardtanh', 'ReLU6', 'SiLU', 'Hardswish', 'LeakyReLU', 'Sigmoid', 'LogSigmoid', 'ELU', 'RReLU',
           'SELU', 'CELU', 'GELU', 'Mish', 'Softshrink', 'Tanh', 'Tanhshrink','Threshold', 'Softmax', 'LogSoftmax',
           'Softmin', 'Softsign', 'GLU', 'Hardshrink', 'MultiheadAttention', 'Hardsigmoid', 'PReLU', 'Softplus',
           'Softmax2d']


class ReLU(Module):
    r"""Applies the rectified linear unit function element-wise:

    :math:`\text{ReLU}(x) = (x)^+ = \max(0, x)`

    Args:
        inplace: can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    .. image:: ../scripts/activation_images/ReLU.png

    Examples::

        >>> import msadapter.pytorch as torch
        >>> import msadapter.pytorch.nn as nn
        >>> m = nn.ReLU()
        >>> input = torch.randn(2)
        >>> output = m(input)
    """

    def __init__(self, inplace=False):
        super(ReLU, self).__init__()
        self.relu = P.ReLU()
        self.inplace = inplace
        _inplace_limit_pynative(inplace, "ReLU")

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        output = self.relu(input_ms)
        return _inplace_assign(input, self.inplace, output)

    def extra_repr(self):
        inplace_str = 'inplace=True' if self.inplace else ''
        return inplace_str


class Hardtanh(Module):
    def __init__(
        self,
        min_val=-1.,
        max_val=1.,
        inplace=False,
        min_value=None,
        max_value=None
    ):
        super(Hardtanh, self).__init__()
        _inplace_limit_pynative(inplace, "Hardtanh")
        if min_value is not None:
            warnings.warn("keyword argument min_value is deprecated and rename to min_val")
            min_val = min_value
        if max_value is not None:
            warnings.warn("keyword argument max_value is deprecated and rename to max_val")
            max_val = max_value

        self.min_val = min_val
        self.max_val = max_val
        self.inplace = inplace
        if self.max_val <= self.min_val:
            raise ValueError('`max_val` must be larger than `min_val` in `{}`, but get `max_val`:{} and '
                             '`min_val`:{}'.format(self.__class__.__name__, self.max_val, self.min_val))
        self.hardtanh = nn.Hardtanh(min_val, max_val)


    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        output = self.hardtanh(input_ms)
        return _inplace_assign(input, self.inplace, output)

    def extra_repr(self):
        inplace_str = ', inplace=True' if self.inplace else ''
        return 'min_val={}, max_val={}{}'.format(
            self.min_val, self.max_val, inplace_str
        )


class ReLU6(Hardtanh):
    def __init__(self, inplace=False):
        _inplace_limit_pynative(inplace, "ReLU6")
        super(ReLU6, self).__init__(0., 6., inplace)

    def extra_repr(self):
        inplace_str = 'inplace=True' if self.inplace else ''
        return inplace_str


class SiLU(Module):
    def __init__(self, inplace=False):
        super(SiLU, self).__init__()
        _inplace_limit_pynative(inplace, "SiLU")
        self.inplace = inplace
        self.sigmoid = P.Sigmoid()

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        output = self.sigmoid(input_ms) * input_ms
        return _inplace_assign(input, self.inplace, output)

    def extra_repr(self) -> str:
        inplace_str = 'inplace=True' if self.inplace else ''
        return inplace_str


class Hardswish(Module):
    def __init__(self, inplace=False):
        super(Hardswish, self).__init__()
        _inplace_limit_pynative(inplace, "Hardswish")
        self.inplace = inplace
        self.hardswish = P.HSwish()

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        output = self.hardswish(input_ms)
        return _inplace_assign(input, self.inplace, output)


class LeakyReLU(Module):
    def __init__(self, negative_slope=1e-2, inplace=False):
        super(LeakyReLU, self).__init__()
        _inplace_limit_pynative(inplace, "LeakyReLU")
        self.negative_slope = negative_slope
        self.inplace = inplace
        self.greater_equal = P.GreaterEqual()
        self.mul = P.Mul()
        self.select_op = P.Maximum()
        if self.negative_slope > 1:
            self.select_op = P.Minimum()
        self.cast = P.Cast()

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        alpha_array = self.cast(F.scalar_to_tensor(self.negative_slope), input_ms.dtype)
        output = self.select_op(alpha_array * input_ms, input_ms)

        return _inplace_assign(input, self.inplace, output)

    def extra_repr(self) -> str:
        inplace_str = ', inplace=True' if self.inplace else ''
        return 'negative_slope={}{}'.format(self.negative_slope, inplace_str)


class Sigmoid(Module):
    def __init__(self):
        super(Sigmoid, self).__init__()
        self.sigmoid = P.Sigmoid()

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        output =  self.sigmoid(input)
        return cast_to_adapter_tensor(output)


class LogSigmoid(Module):
    def __init__(self):
        super(LogSigmoid, self).__init__()
        self.logsigmoid = ms_torch_nn_func.logsigmoid

    def forward(self, input):
        return self.logsigmoid(input)


class ELU(Module):
    def __init__(self, alpha: float=1., inplace: bool=False):
        super(ELU, self).__init__()
        _inplace_limit_pynative(inplace, "ELU")
        self.elu = ms_torch_nn_func.elu
        self.alpha = alpha
        self.inplace = inplace

    def forward(self, input):
        return self.elu(input, self.alpha, self.inplace)


class RReLU(Module):
    def __init__(
        self,
        lower=1./8,
        upper=1./3,
        inplace=False
    ):
        super(RReLU, self).__init__()
        _inplace_limit_pynative(inplace, "RReLU")
        self.lower = lower
        self.upper = upper
        self.inplace = inplace
        self.rrelu = ms.nn.RReLU(lower=self.lower, upper=self.upper)

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        out = self.rrelu(input_ms)
        return _inplace_assign(input, self.inplace, out)

    def extra_repr(self):
        inplace_str = ', inplace=True' if self.inplace else ''
        return 'lower={}, upper={}{}'.format(self.lower, self.upper, inplace_str)


class SELU(Module):
    def __init__(self, inplace=False):
        super(SELU, self).__init__()
        _inplace_limit_pynative(inplace, "SELU")
        self.inplace = inplace
        self.selu = P.SeLU()

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        out = self.selu(input_ms)
        return _inplace_assign(input, self.inplace, out)

    def extra_repr(self):
        inplace_str = 'inplace=True' if self.inplace else ''
        return inplace_str


class CELU(Module):
    def __init__(self, alpha=1., inplace=False):
        super(CELU, self).__init__()
        _inplace_limit_pynative(inplace, "CELU")
        self.alpha = alpha
        self.inplace = inplace
        self.celu = P.CeLU(alpha=self.alpha)

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        out = self.celu(input_ms)
        return _inplace_assign(input, self.inplace, out)

    def extra_repr(self):
        inplace_str = ', inplace=True' if self.inplace else ''
        return 'alpha={}{}'.format(self.alpha, inplace_str)


class GELU(Module):
    def __init__(self):
        super(GELU, self).__init__()
        self.gelu = P.GeLU()

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        out = self.gelu(input)
        return cast_to_adapter_tensor(out)


class Mish(Module):
    def __init__(self, inplace=False):
        super(Mish, self).__init__()
        _inplace_limit_pynative(inplace, "Mish")
        self.inplace = inplace
        self.mish = P.Mish()

    def forward(self, input):
        input_ms = cast_to_ms_tensor(input)
        out = self.mish(input_ms)
        return _inplace_assign(input, self.inplace, out)

    def extra_repr(self):
        inplace_str = 'inplace=True' if self.inplace else ''
        return inplace_str


class Softshrink(Module):
    def __init__(self, lambd=0.5):
        super(Softshrink, self).__init__()
        self.lambd = lambd
        self.softshrink = P.SoftShrink(lambd=self.lambd)

    def forward(self, input):
        input = cast_to_ms_tensor(input)
        out = self.softshrink(input)
        return cast_to_adapter_tensor(out)

    def extra_repr(self):
        return str(self.lambd)


class Tanh(Module):
    def forward(self,input):
        return ms_torch_nn_func.tanh(input)


class Tanhshrink(Module):
    def forward(self,input):
        return ms_torch_nn_func.tanhshrink(input)


class Threshold(Module):
    def __init__(self, threshold, value, inplace=False):
        super(Threshold, self).__init__()
        _inplace_limit_pynative(inplace, "Threshold")
        self.threshold = threshold
        self.value = value
        self.inplace = inplace

    def forward(self, input):
        return ms_torch_nn_func.threshold(input, self.threshold, self.value, self.inplace)

    def extra_repr(self):
        inplace_str = ', inplace=True' if self.inplace else ''
        return 'threshold={}, value={}{}'.format(self.threshold, self.value, inplace_str)


class Softmax(Module):
    def __init__(self, dim=None):
        super(Softmax, self).__init__()
        self.softmax = ms_torch_nn_func.softmax
        self.dim = dim

    def forward(self, input):
        return self.softmax(input, self.dim)

    def extra_repr(self):
        return 'dim={dim}'.format(dim=self.dim)

class LogSoftmax(Module):
    def __init__(self, dim=None):
        super(LogSoftmax, self).__init__()
        self.logsoftmax = ms_torch_nn_func.log_softmax
        self.dim = dim

    def forward(self, input):
        return self.logsoftmax(input, self.dim)

    def extra_repr(self):
        return 'dim={dim}'.format(dim=self.dim)

class Softmin(Module):
    def __init__(self, dim=None):
        super(Softmin, self).__init__()
        self.softmin = ms_torch_nn_func.softmin
        self.dim = dim

    def forward(self, input):
        return self.softmin(input, self.dim)

    def extra_repr(self):
        return 'dim={dim}'.format(dim=self.dim)

class Softsign(Module):
    def __init__(self):
        super(Softsign, self).__init__()
        self.softsign = ms_torch_nn_func.softsign

    def forward(self, input):
        return self.softsign(input)


class GLU(Module):
    def __init__(self, dim=-1):
        super(GLU, self).__init__()
        self.glu = ms_torch_nn_func.glu
        self.dim = dim

    def forward(self, input):
        return self.glu(input, self.dim)

    def extra_repr(self):
        return 'dim={dim}'.format(dim=self.dim)


class Hardshrink(Module):
    def __init__(self, lambd: float=0.5):
        super(Hardshrink, self).__init__()
        self.lambd = lambd

    def forward(self, input):
        return ms_torch_nn_func.hardshrink(input, self.lambd)

    def extra_repr(self) -> str:
        return '{}'.format(self.lambd)


class Hardsigmoid(Module):
    def __init__(self, inplace: bool=False):
        super(Hardsigmoid, self).__init__()
        _inplace_limit_pynative(inplace, "Hardsigmoid")
        self.inplace = inplace

    def forward(self, input):
        return ms_torch_nn_func.hardsigmoid(input, self.inplace)


class MultiheadAttention(Module):
    def __init__(self, embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, \
        add_zero_attn=False, kdim=None, vdim=None, batch_first=False, device=None, dtype=None):
        super(MultiheadAttention, self).__init__()
        if bias is not True:
            raise ValueError(f"`bias` can only be set to 'True', but got {bias}")

        if add_bias_kv:
            raise ValueError(f"`add_bias_kv` can only be set to 'False', but got {add_bias_kv}")

        if add_zero_attn:
            raise ValueError(f"`add_zero_attn` can only be set to 'False', but got {add_zero_attn}")

        unsupported_attr(kdim)
        unsupported_attr(vdim)
        unsupported_attr(device)

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.dropout = dropout
        self.add_bias_kv = add_bias_kv
        self.add_zero_attn = add_zero_attn
        self.kdim = kdim
        self.vdim = vdim
        self.batch_first = batch_first
        self.dtype = dtype

        self.reduce_mean = ms.ops.ReduceMean()

    def forward(self, query, key, value, key_padding_mask=None,
                need_weights: bool=True, attn_mask=None,
                average_attn_weights: bool=True):
        unsupported_attr(key_padding_mask)
        unsupported_attr(average_attn_weights)
        if need_weights is True:
            raise ValueError("Until now, `need_weights`='True' is not supported")

        query = self._batch_tensor(query, 'query')
        key = self._batch_tensor(key, 'key')
        value = self._batch_tensor(value, 'value')
        _batch_size = query.shape[0]
        _src_seq_length = query.shape[1]
        _tgt_seq_length = key.shape[1]

        if attn_mask:
            _attn_mask = self._process_mask(attn_mask, _batch_size)
        else:
            _attn_mask = ms.ops.ones((_batch_size, _src_seq_length, _tgt_seq_length), mstype.float32)

        self.ms_multihead_attention = ms.nn.transformer.MultiHeadAttention(
            batch_size = _batch_size,
            src_seq_length = _src_seq_length,
            tgt_seq_length = _tgt_seq_length,
            hidden_size=self.embed_dim,
            num_heads=self.num_heads,
            hidden_dropout_rate=self.dropout,
            attention_dropout_rate=self.dropout,
            compute_dtype=mstype.float32,
            softmax_compute_type=mstype.float32,
            param_init_type=mstype.float32,
            use_past=False)
        out, attn_output_weights = self.ms_multihead_attention(query, key, value, _attn_mask)

        if not self.batch_first:
            # ms default is (batch, seq, feature), batch_first
            out = ms.ops.transpose(out, (1, 0, 2))

        # if need_weights:
        #     if average_attn_weights:
        #         attn_output_weights = self.reduce_mean(attn_output_weights, 1)

        #     if _batch_size == 1:
        #         attn_output_weights = self.reduce_mean(attn_output_weights, 0)
        # else:
        #         attn_output_weights = None

        if _batch_size == 1:
            out = self.reduce_mean(out, 0)

        # TODO
        # Until Now, attn_output_weights is not the same as pytorch
        attn_output_weights = None
        return cast_to_adapter_tensor(out), cast_to_adapter_tensor(attn_output_weights)

    def _batch_tensor(self, x, x_name: str):
        x = cast_to_ms_tensor(x)
        _rank = ms.ops.rank(x)
        if _rank == 2:
            out = ms.ops.expand_dims(x, 0)
            return out

        if _rank == 3:
            if not self.batch_first:
                out = ms.ops.transpose(x, (1, 0 ,2))
            else:
                out = x
            return out

        raise ValueError(f"For MultiheadAttention, rank of {x_name} should be 2 or 3, but got {_rank}")

    def _process_mask(self, mask, batch_size):
        mask = cast_to_ms_tensor(mask)
        _rank = ms.ops.rank(mask)
        if _rank == 2:
            out = ms.ops.expand_dims(mask, 0)
            return out

        if _rank == 3:
            if mask.shape[0] != batch_size:
                warnings.warn("Until now, `attn_mask` can only support shape (N, L, S)"
                    "when `attn_mask` shape is (N * num_heads, L, S), pick the first (N, L, S) mask")

            mask = mask[:batch_size,:]
            return mask

        raise ValueError(f"For MultiheadAttention, rank of mask should be 2 or 3, but got {_rank}")


class PReLU(Module):
    def __init__(self, num_parameters=1, init=0.25, device=None, dtype=None):
        super(PReLU, self).__init__()
        unsupported_attr(device)
        validator.check_positive_int(num_parameters, 'num_parameters', self.cls_name)
        if dtype is None:
            dtype = mstype.float32
        w = init
        if isinstance(w, (float, np.float32)):
            tmp = np.empty((num_parameters,), dtype=np.float32)
            tmp.fill(w)
            w = tensor(tmp, dtype=dtype)
        elif isinstance(w, list):
            if len(w) != num_parameters:
                raise ValueError(f"For '{self.cls_name}', the length of 'init' must be equal to the 'num_parameters'"
                                 f"when the 'init' is a list, but got the length of 'num_parameters': {len(w)}, "
                                 f"the 'num_parameters': {num_parameters}.")

            for i in w:
                if not isinstance(i, (float, np.float32)):
                    raise ValueError(f"For '{self.cls_name}', all elements in 'init' must be "
                                     f"float when the 'init' is a list, but got {i}.")
            w = tensor(w, dtype=dtype)
        elif isinstance(w, Tensor):
            if w.dtype not in (mstype.float16, mstype.float32):
                raise ValueError(f"For '{self.cls_name}', the dtype of 'init' must be float16 or "
                                 f"float32 when the 'init' is a tensor, but got {w.dtype}.")
            if len(w.shape) != 1 or w.shape[0] != num_parameters:
                raise ValueError(f"For '{self.cls_name}', the dimension of 'init' must be 1, and the elements number "
                                 f"should be equal to the 'num_parameters' when the 'init' is a tensor, "
                                 f"but got 'init' shape {w.shape}, the 'num_parameters' {num_parameters}.")
        else:
            raise TypeError(f"For '{self.cls_name}', the 'init' only supported float, list and tensor, "
                            f"but got {type(w).__name__}.")

        self.weight = Parameter(w)
        self.num_parameters = num_parameters

    def forward(self, input):
        return ms_torch_nn_func.prelu(input, self.weight)

    def extra_repr(self) -> str:
        return 'num_parameters={}'.format(self.num_parameters)


class Softplus(Module):
    def __init__(self, beta=1, threshold=20):
        super(Softplus, self).__init__()
        self.beta = beta
        self.threshold = threshold

    def forward(self, input):
        return ms_torch_nn_func.softplus(input, self.beta, self.threshold)

    def extra_repr(self):
        return 'beta={}, threshold={}'.format(self.beta, self.threshold)


class Softmax2d(Module):
    def __init__(self):
        super(Softmax2d, self).__init__()
        self.softmax2d = ms.nn.Softmax2d()

    def forward(self, input):
        if input.dim() not in {3, 4}:
            raise RuntimeError("Softmax2d requires a 3D or 4D tensor as input")
        return self.softmax2d(input)
