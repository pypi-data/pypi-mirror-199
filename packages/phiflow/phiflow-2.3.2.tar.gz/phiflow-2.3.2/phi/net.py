from dataclasses import dataclass
from typing import Tuple, Dict, List, Callable

from . import math
from .math import Tensor, Shape, random_uniform, channel, sqrt, pack_dims, non_batch, where, is_finite, finite_mean, \
    sign, vec_squared, shape, maximum, merge_shapes, to_float, ones, sigmoid, stack, rename_dims, batch, instance, \
    vec_length, spatial
from .math._fit import fit_line_2d
from .math._fit import fit_hyperplane


_CONTEXTS = []


class Context:

    def __init__(self):
        self.forward_cache = {}
        self.execution_order: List[Layer] = []

    def __enter__(self):
        _CONTEXTS.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert _CONTEXTS.pop(-1) is self


_ALL_NAMES = set()


def get_name(base: str):
    suffix = 0
    while base + str(suffix) in _ALL_NAMES:
        suffix += 1
    name = base + str(suffix)
    _ALL_NAMES.add(name)
    return name


class Layer:

    def __init__(self, inputs: Tuple['Layer', ...]):
        assert isinstance(inputs, tuple) and all(isinstance(i, Layer) for i in inputs)
        self.inputs = inputs
        self.name = get_name(self.__class__.__name__)

    @property
    def input_shapes(self) -> Tuple[Shape]:
        return tuple([i.output_shape for i in self.inputs])

    @property
    def output_shape(self) -> Shape:
        raise NotImplementedError(self.__class__)

    def __shape__(self):
        return self.output_shape

    def forward(self, *args):
        raise NotImplementedError(self.__class__)

    def forward_gradient(self, *args):
        raise NotImplementedError(self.__class__)

    def __call__(self, *args, **kwargs):
        context = _CONTEXTS[-1] if _CONTEXTS else Context()
        if self in context.forward_cache:
            return context.forward_cache[self]
        else:
            x = [i(*args, **kwargs) for i in self.inputs]
            y = self.forward(*x)
            context.execution_order.append(self)
            context.forward_cache[self] = y
            return y

    def apply_update(self, update: Dict[str, Tensor]):
        for attribute, delta in update.items():
            setattr(self, attribute, getattr(self, attribute) + delta)

    @property
    def layer_weights(self) -> Dict[str, Tensor]:
        raise NotImplementedError


class Input(Layer):

    def __init__(self, ref: str or int, *shape: Shape):
        super(Input, self).__init__(())
        self.ref = ref
        self.shape = merge_shapes(*shape)

    @property
    def output_shape(self) -> Shape:
        return self.shape

    def __call__(self, *args, **kwargs):
        context = _CONTEXTS[-1] if _CONTEXTS else Context()
        if isinstance(self.ref, int):
            value = args[self.ref]
        else:
            assert self.ref in kwargs, f"No value specified for {self}"
            value = kwargs[self.ref]
        context.forward_cache[self] = value
        context.execution_order.append(self)
        return value

    def __repr__(self):
        return f"""Input {self.ref if isinstance(self.ref, int) else f"'{self.ref}'"} {self.shape}"""

    def forward_gradient(self, *args):
        return ones(self.shape)

    @property
    def layer_weights(self) -> Dict[str, Tensor]:
        return {}


class ReLU(Layer):

    def __init__(self, x: Layer):
        super().__init__((x,))

    @property
    def output_shape(self) -> Shape:
        return self.input_shapes[0]

    def forward(self, x: Tensor):
        return maximum(0, x)

    def forward_gradient(self, x: Tensor):
        return to_float(x > 0)

    def __repr__(self):
        return "ReLU"

    @property
    def layer_weights(self) -> Dict[str, Tensor]:
        return {}


class Linear(Layer):

    def __init__(self, x: Layer, out_features: int, *batch):
        super().__init__((x,))
        in_features = self.input_shapes[0].non_batch.volume
        k = 1 / sqrt(in_features)
        self.weight = random_uniform(channel(output=out_features, input=in_features), *batch, low=-k, high=k)
        self.bias = random_uniform(channel(output=out_features), *batch, low=-k, high=k)

    @property
    def output_shape(self) -> Shape:
        return self.input_shapes[0].batch & self.weight.shape['output']

    def __repr__(self):
        return f"{self.name} {self.output_shape}"

    def forward(self, x: Tensor):
        x = pack_dims(x, non_batch, channel('features'), pos=-1)
        y = x.features * self.weight.input + self.bias
        if channel(y).volume == 1:
            y = y[next(iter(channel(y).meshgrid()))]
        return y

    @property
    def layer_weights(self) -> Dict[str, Tensor]:
        return {'weight': self.weight, 'bias': self.bias}


def dense_net(in_channels: int,
              out_channels: int,
              layers: tuple or list,
              batch_norm=False,
              activation='ReLU') -> Layer:
    assert not batch_norm
    assert activation == 'ReLU'
    x = Input(0, channel(features=in_channels))
    for neuron_count in layers:
        x = ReLU(Linear(x, neuron_count))
    return Linear(x, out_channels)


def get_parameters(net: Layer) -> Dict[str, Tensor]:
    result = {}

    def _collect_weights_recursive(layer: Layer):
        for input_layer in layer.inputs:
            _collect_weights_recursive(input_layer)
        result.update({f"{layer.name}.{n}": v for n, v in layer.layer_weights.items()})

    _collect_weights_recursive(net)
    return result


def parameter_count(net: Layer) -> int:
    """
    Counts the number of parameters in a model.

    Args:
        net: Model

    Returns:
        `int`
    """
    total = 0
    for value in get_parameters(net).values():
        total += value.shape.volume
    return int(total)


class Optimizer:

    def __init__(self, net: Layer, learning_rate: float):
        self.net = net
        self.learning_rate = learning_rate
        self.step = 0

    def backward(self, layer: Layer, dy: Tensor, context: Context, backprop: Tuple[bool, ...]) -> Tuple[Dict[str, Tensor], tuple]:
        raise NotImplementedError(self.__class__)


class LstsqIG(Optimizer):

    def __init__(self, net: Layer, learning_rate=1., momentum=.9):
        super().__init__(net, learning_rate)
        self.momentum = momentum

    def backward(self, layer: Layer, dy: Tensor, context: Context, backprop: Tuple[bool, ...]) -> Tuple[Dict[str, Tensor], tuple]:
        if isinstance(layer, Input):
            return {}, ()
        elif isinstance(layer, ReLU):
            return {}, (dy,)
        elif isinstance(layer, Linear):
            dy = pack_dims(dy, non_batch, channel('output'))
            input_layer = layer.inputs[0]
            x = context.forward_cache[input_layer]
            x = pack_dims(x, non_batch, channel('input'), pos=-1)
            grad_x = input_layer.forward_gradient(*[context.forward_cache[i] for i in input_layer.inputs])
            grad_x = pack_dims(grad_x, non_batch, channel('input'), pos=-1)
            dw, db, _dy = self.lstsq_update(x, dy, grad_x)
            if backprop[0]:
                pre_update_fac = 1 if self.step == 0 else .5
                dx, dy_ = back_propagate_delta(layer.weight + pre_update_fac * dw, dy, grad_x)  # use 1 at start, then .5
                return {'weight': dw, 'bias': db}, (dx,)
            else:
                return {'weight': dw, 'bias': db}, (None,)

    def lstsq_update(self, x, dy, grad_x):
        """
        Update the weight matrix of the linear transformation *w · x = y*.

        Args:
            x: Forward input vector *x*, Shape (batch, input)
            dy: Desired change in *y*. Shape (batch, neurons)

        Returns:
            dw: Shape (input, neurons)
            db: Shape (neurons,)
            dy: Shape (batch, neurons)
        """
        if not channel(x):
            dw, db = fit_line_2d(x, dy, 'batch', weights=grad_x)
            dw = where(is_finite(dw), dw, 0)
        else:
            dw, db = fit_hyperplane(x, dy, 'batch')
        dw *= self.learning_rate  # / dw.input.size_or_1 division only when overlapping
        db *= self.learning_rate
        db_mean = finite_mean(db, 'input')
        db_mean = where(is_finite(db_mean), db_mean, 0)
        dy_forward = dw.input * x.input + db_mean
        return dw, db_mean, dy_forward

    def __repr__(self):
        return 'lstsq'


def back_propagate_delta(w, dy, grad_x):
    """
    Back-propagate the residual `dy` through a matrix-vector multiplication.

    Args:
        w: Shape (input, output)
        dy: Shape (batch, output)
        grad_x: Shape (batch, input)

    Returns:
        dx: Shape (input, output)
        dy: Non-propagated change, Shape (batch, output)
    """
    # print(vec_length(dy, shape))
    total_dx = 0
    for i in range(1):
        unscaled_dx = sign(w).output * dy.output  # ToDo
        unscaled_dx *= abs(grad_x)  # only affect where it makes a difference, not where activation prevents change
        unscaled_forward_dy = w.input * unscaled_dx.input
        dx_scale = sqrt(vec_squared(dy, shape) / vec_squared(unscaled_forward_dy, shape))
        dx = unscaled_dx * dx_scale
        total_dx += dx
        forward_dy = unscaled_forward_dy * dx_scale
        dy = dy - forward_dy
        # print(vec_squared(dy, shape))
    # print(vec_length(dy, shape))
    from phi import vis
    # vis.show(dy.batch.retype(spatial))
    return total_dx, dy


class FAIG(Optimizer):
    """ Fast approximate inverse gradient """

    def __init__(self, net: Layer, learning_rate=1.):
        super().__init__(net, learning_rate)

    def backward(self, layer: Layer, dy: Tensor, context: Context, backprop: Tuple[bool, ...]) -> Tuple[Dict[str, Tensor], tuple]:
        if isinstance(layer, Input):
            return {}, ()
        elif isinstance(layer, ReLU):
            return {}, (dy,)
        elif isinstance(layer, Linear):
            dy = pack_dims(dy, non_batch, channel('output'))
            input_layer = layer.inputs[0]
            x = context.forward_cache[input_layer]
            x = pack_dims(x, non_batch, channel('input'), pos=-1)
            grad_x = input_layer.forward_gradient(*[context.forward_cache[i] for i in input_layer.inputs])
            grad_x = pack_dims(grad_x, non_batch, channel('input'), pos=-1)
            dw, db, dy_forward = self.line_fit_update(x, dy, grad_x)
            # dyy -= dy_forward
            if backprop[0]:
                dx, dy_ = back_propagate_delta(layer.weight + .5 * dw, dy, grad_x)
                return {'weight': dw, 'bias': db}, (dx,)
            else:
                return {'weight': dw, 'bias': db}, (None,)

    def line_fit_update(self, x, dy, grad_x):
        """
        Update the weight matrix of the linear transformation *w · x = y*.

        Args:
            x: Forward input vector *x*, Shape (batch, input)
            dy: Desired change in *y*. Shape (batch, output)

        Returns:
            dw: Shape (input, output)
            db: Shape (output,)
            dy: Shape (batch, output)
        """
        weights = grad_x
        # weights = where(x > 0, 1, 0)
        # weights = sigmoid(x / self.weight * 2)
        list_dims = batch(x).without(batch(self))
        dw, db = fit_line_2d(x, dy, list_dims, weights=weights)
        # from phi.vis import plot, show
        # from phi.field import PointCloud
        # from phi.geom import Sphere
        # for i in shape(self.weight).meshgrid(names=True):
        #     plot(PointCloud(Sphere(stack({'x': pack_dims(x[i], list_dims, instance('points')), 'dy': pack_dims(dy[i], list_dims, instance('points'))}, channel('vector')), radius=.1 * pack_dims(weights[i], list_dims, instance('points')))), title=f"{self} {i}")
        # ToDo scale dw, db according to how much they contribute, filter out NaN (no contribution)
        dw = where(is_finite(dw), dw, 0)
        # dw = where(abs(dw) > 1, dw / abs(dw), dw)
        # db = where(abs(db) > 1, db / abs(db), db)
        dw *= self.learning_rate  # / dw.input.size_or_1 division only when overlapping
        db *= self.learning_rate
        db_mean = finite_mean(db, 'input')
        db_mean = where(is_finite(db_mean), db_mean, 0)
        dy_forward = dw.input * x.input + db_mean
        return dw, db_mean, dy_forward

    def __repr__(self):
        return 'line-fit'


class SGD(Optimizer):

    def __init__(self, net: Layer, learning_rate=1e-3):
        super().__init__(net, learning_rate)


def update_weights(net: Layer, optimizer: Optimizer, loss_function: Callable, *loss_args, **loss_kwargs):
    """
    Updates the weights of `net` using `optimizer`.

    This is the Φ<sub>Flow</sub> version. Analogue functions exist for other learning frameworks.

    Args:
        net: Learning model.
        optimizer: Optimizer.
        loss_function: Loss function, called as `loss_function(*loss_args, **loss_kwargs)`.
        *loss_args: Arguments given to `loss_function`.
        **loss_kwargs: Keyword arguments given to `loss_function`.

    Returns:
        Output of `loss_function`.
    """
    with Context() as context:
        loss_output = loss_function(*loss_args, **loss_kwargs)
    loss = loss_output[0] if isinstance(loss_output, tuple) else loss_output
    if isinstance(loss, L2Loss):
        updates, dy_ = back_propagate(optimizer, {net: -loss.difference}, context)
        for layer, update in updates.items():
            layer.apply_update(update)
    else:
        raise NotImplementedError  # ToDo backprop to network output
    optimizer.step += 1
    return loss_output


def back_propagate(optimizer: Optimizer, dy: Dict[Layer, Tensor], context: Context) -> Tuple[Dict[Layer, Dict[str, Tensor]], Dict[Layer, Tensor]]:
    updates = {}
    for layer in reversed(context.execution_order):
        layer_dy = dy[layer]
        backprop = tuple(bool(get_parameters(i)) for i in layer.inputs)
        layer_update, layer_dxs = optimizer.backward(layer, layer_dy, context, backprop)
        assert isinstance(layer_update, dict)
        updates[layer] = layer_update
        assert isinstance(layer_dxs, tuple), f"{type(layer).__name__}.backward() must return a tuple but got {type(layer_dxs).__name__}"
        assert len(layer_dxs) == len(layer.inputs), f"{type(layer).__name__}.backward() must return {len(layer.inputs)} values but returned {len(layer_dxs)}"
        for layer_input, layer_dx in zip(layer.inputs, layer_dxs):
            if layer_input in dy:
                dy[layer_input] += layer_dx
            else:
                dy[layer_input] = layer_dx
    return updates, dy


def l2_loss(difference):
    if _CONTEXTS:
        return L2Loss(difference)
    else:
        from phi.math import l2_loss as tensor_l2
        return tensor_l2(difference)


class L2Loss:

    def __init__(self, difference):
        self.difference = difference
        self._actual_l2 = math.l2_loss(difference)

    def __getattr__(self, item):
        return getattr(self._actual_l2, item)

    def __repr__(self):
        return repr(self._actual_l2)


def native_call(f, *args, **kwargs):
    return f(*args, **kwargs)
