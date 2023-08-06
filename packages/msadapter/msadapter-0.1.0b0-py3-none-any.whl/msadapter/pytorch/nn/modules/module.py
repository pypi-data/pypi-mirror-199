#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from mindspore.nn import Cell
from mindspore import Tensor as ms_Tensor
from mindspore.train.serialization import load_param_into_net
from msadapter.pytorch.tensor import tensor
from msadapter.pytorch.nn.parameter import Parameter
from msadapter.utils import unsupported_attr
from msadapter.pytorch.common.device import Device

__all__ = ['Module']


class Module(Cell):
    def __init__(self, auto_prefix=True, flags=None):
        super(Module, self).__init__(auto_prefix, flags)
        self.training = True

    def __del__(self):
        pass

    def __repr__(self):
        extra_str = self.extra_repr()
        info_str = self.__class__.__name__ + '('
        if self._cells:
            sub_str = '\n'
            if extra_str:
                sub_str += '{}\n'.format(self.extra_repr())
            for key, value in self._cells.items():
                sub_str += '  ({}): {}\n'.format(key, repr(value))
            sub_str = sub_str.replace('\n', '\n') + ')'
            info_str += sub_str
        else:
            info_str += extra_str + ')'
        return info_str

    def extra_repr(self):
        r"""Set the extra representation of the module"""
        return ''

    def construct(self, *inputs, **kwargs):
        return self.forward(*inputs, **kwargs)

    def _run_construct(self, cast_inputs, kwargs):
        """Run the construct function"""
        if self._enable_forward_pre_hook:
            cast_inputs = self._run_forward_pre_hook(cast_inputs)
        if self._enable_backward_hook:
            output = self._backward_hook_construct(*cast_inputs)
        elif hasattr(self, "_shard_fn"):
            output = self._shard_fn(*cast_inputs, **kwargs)
        else:
            output = self.construct(*cast_inputs, **kwargs)
        if self._enable_forward_hook:
            output = self._run_forward_hook(cast_inputs, output)

        return output

    def forward(self, *inputs, **kwargs):
        raise NotImplementedError("The forward method must be implemented by inherited class")

    def train(self, mode=True):
        self.set_train(mode)
        return self

    def eval(self):
        self.set_train(False)
        return self

    def modules(self):
        result = []
        cells_names = self.cells_and_names()
        for m in cells_names:
            result.append(m[1])
        return iter(result)

    def named_modules(self, memo=None, prefix='', remove_duplicate=None):
        if memo:
            raise NotImplementedError("For named_modules, `memo` not implemented.")
        unsupported_attr(remove_duplicate)
        output = self.cells_and_names(name_prefix=prefix)
        return output

    def _parameters_and_names(self, name_prefix='', expand=True):
        cells = []
        if expand:
            cells = self.cells_and_names(name_prefix=name_prefix)
        else:
            cells.append((name_prefix, self))

        params_set = set()
        for cell_name, cell in cells:
            params = cell._params.items()
            for par_name, par in params:
                if par.inited_param is not None:
                    par = par.inited_param
                if par is not None and id(par) not in params_set:
                    params_set.add(id(par))
                    par_new_name = par_name
                    if cell_name:
                        par_new_name = cell_name + '.' + par_new_name
                        # TODO Update parameter names to avoid duplicates
                        par.name = par_new_name
                    yield par_new_name, par

    def add_module(self, name, module):
        if not isinstance(module, Module) and module is not None:
            raise TypeError("{} is not a Module subclass".format(
                module.__name__))
        elif hasattr(self, name) and name not in self._cells:
            raise KeyError("attribute '{}' already exists".format(name))
        elif '.' in name:
            raise KeyError("module name can't contain \".\", got: {}".format(name))
        elif name == '':
            raise KeyError("module name can't be empty string \"\"")
        self._cells[name] = module

    def register_module(self, name, module):
        """Alias for :func:`add_module`."""
        self.add_module(name, module)

    def named_parameters(self, prefix='', recurse=True):
        return self._parameters_and_names(prefix, recurse)

    def parameters_and_names(self, name_prefix='', expand=True):
        return self._parameters_and_names(name_prefix=name_prefix, expand=expand)

    def named_children(self):
        r"""Returns an iterator over immediate children modules, yielding both
        the name of the module as well as the module itself.

        Yields:
            (string, Module): Tuple containing a name and child module

        Example::

            >>> for name, module in model.named_children():
            >>>     if name in ['conv4', 'conv5']:
            >>>         print(module)

        """
        memo = set()
        for name, module in self._cells.items():
            if module is not None and module not in memo:
                memo.add(module)
                yield name, module

    def children(self):
        r"""Returns an iterator over immediate children modules.

        Yields:
            Module: a child module
        """
        for _, module in self.named_children():
            yield module

    def apply(self, fn=None):
        r"""Applies ``fn`` recursively to every submodule (as returned by ``.children()``)
        as well as self. Typical use includes initializing the parameters of a model
        (see also :ref:`nn-init-doc`).

        Args:
            fn (:class:`Module` -> None): function to be applied to each submodule

        Returns:
            Module: self

        Example::

            >>> def init_weights(m):
            >>>     print(m)
            >>>     if type(m) == nn.Linear:
            >>>         m.weight.fill_(1.0)
            >>>         print(m.weight)
            >>> net = nn.Sequential(nn.Linear(2, 2), nn.Linear(2, 2))
            >>> net.apply(init_weights)
        """

        for module in self.children():
            module.apply(fn)
        fn(self)
        return self

    def parameters(self, recurse = True):
        for _, param in self.named_parameters(recurse=recurse):
            yield param

    def state_dict(self, destination=None, prefix='', keep_vars=False):
        unsupported_attr(keep_vars)
        unsupported_attr(prefix)

        if destination is None:
            destination = OrderedDict()

        for n, v in self.named_parameters():
            destination[n] = tensor(v)
        return destination

    def register_buffer(self, name, tensor, persistent=True):
        r"""Adds a buffer to the module.

               This is typically used to register a buffer that should not to be
               considered a model parameter. For example, BatchNorm's ``running_mean``
               is not a parameter, but is part of the module's state. Buffers, by
               default, are persistent and will be saved alongside parameters. This
               behavior can be changed by setting :attr:`persistent` to ``False``. The
               only difference between a persistent buffer and a non-persistent buffer
               is that the latter will not be a part of this module's
               :attr:`state_dict`.

               Buffers can be accessed as attributes using given names.

               Args:
                   name (string): name of the buffer. The buffer can be accessed
                       from this module using the given name
                   tensor (Tensor or None): buffer to be registered. If ``None``, then operations
                       that run on buffers, such as :attr:`cuda`, are ignored. If ``None``,
                       the buffer is **not** included in the module's :attr:`state_dict`.
                   persistent (bool): whether the buffer is part of this module's
                       :attr:`state_dict`.
               """
        unsupported_attr(persistent)

        if '_params' not in self.__dict__:
            raise AttributeError("cannot assign buffer before Module.__init__() call.")
        elif not isinstance(name, str):
            raise TypeError("buffer name should be a string. "
                            "Got {}".format(type(name)))
        elif '.' in name:
            raise KeyError("buffer name can't contain \".\"")
        elif name == '':
            raise KeyError("buffer name can't be empty string \"\"")
        elif hasattr(self, name) and name not in self._params:
            raise KeyError("attribute '{}' already exists".format(name))
        elif tensor is not None and not isinstance(tensor, ms_Tensor):
            raise TypeError("cannot assign '{}' object to buffer '{}' "
                            "(Tensor or None required)"
                            .format(type(tensor), name))
        else:
            self._params[name] = Parameter(tensor, name=name, requires_grad=False)


    def named_buffers(self, prefix='', recurse=True, remove_duplicate=True):
        if remove_duplicate is False:
            raise NotImplementedError("named_buffers not support `remove_duplicate` is False")

        _params = self.untrainable_params(recurse)
        if prefix:
            for param in _params:
                yield '.'.join([prefix, param.name]), param
        else:
            for param in _params:
                yield param.name, param

    def buffers(self, recurse=True):
        for _, buf in self.named_buffers(recurse=recurse):
            yield buf

    def to(self, *args, **kwargs):
        # TODO:
        # Note that this API requires the user to ensure the correctness of the input currently,
        # and only the function of modifying device is available.

        args_len = len(args)
        kwargs_len = len(kwargs)

        if args_len == 0 and kwargs_len == 0:
            raise ValueError("Module.to is missing inputs, please check.")
        elif (args_len + kwargs_len > 1) or (kwargs_len > 0 and "device" not in kwargs):
            raise ValueError("Currently only the function of modifying device is available.")
        elif (args_len > 0 and not isinstance(args[0], (str, Device))) or \
                (kwargs_len > 0 and not isinstance(kwargs.get("device"), (str, Device))):
            raise ValueError("Currently only the function of modifying device is available, "
                             "which via a string or torch.device.")
        return self

    def register_parameter(self, name, param):
        """Adds a parameter to the module.

        The parameter can be accessed as an attribute using given name.

        Args:
            name (string): name of the parameter. The parameter can be accessed
                from this module using the given name
            param (Parameter or None): parameter to be added to the module. If
                ``None``, then operations that run on parameters, such as :attr:`cuda`,
                are ignored. If ``None``, the parameter is **not** included in the
                module's :attr:`state_dict`.
        """
        if '_params' not in self.__dict__:
            raise AttributeError("cannot assign parameter before Module.__init__() call")

        elif not isinstance(name, str):
            raise TypeError("parameter name should be a string. Got {}".format(type(name)))
        elif '.' in name:
            raise KeyError("parameter name can't contain \".\"")
        elif name == '':
            raise KeyError("parameter name can't be empty string \"\"")
        elif hasattr(self, name) and name not in self._params:
            raise KeyError("attribute '{}' already exists".format(name))

        if param is None:
            self._params[name] = None
        elif not isinstance(param, Parameter):
            raise TypeError("cannot assign '{}' object to parameter '{}' "
                            "(nn.Parameter or None required)"
                            .format(type(param), name))
        else:
            self._params[name] = param

    def cuda(self, device=None):
        unsupported_attr(device)
        return self

    def load_state_dict(self, state_dict, strict=False):
        param_not_load = load_param_into_net(self, state_dict, strict_load=strict)
        return param_not_load
