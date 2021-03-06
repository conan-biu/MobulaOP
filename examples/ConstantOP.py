'''
Notice:
    ConstantOP only supports CPU.
    For supporting cross-device, please use ConstantOP2
'''
import sys
sys.path.append('../')  # Add MobulaOP path
import mobula
import numpy as np

# ConstantOP only supports CPU.


@mobula.op.register(need_top_grad=False)
class ConstantOP:
    def __init__(self, constant):
        self.constant = self.F.array(constant)

    def forward(self):
        return self.constant

    def backward(self, dy):
        return []

    def infer_shape(self, in_shape):
        return [], [self.constant.shape]


@mobula.op.register(need_top_grad=False)
class ConstantOP2:
    def __init__(self, constant):
        self.constant = self.F.array(constant)
        self.constant_buffer = dict()

    def forward(self, x):
        ctx = x.context
        return self.constant_buffer.get(ctx, self.constant.as_in_context(ctx))

    def backward(self, dy):
        return [0]

    def infer_shape(self, in_shape):
        return in_shape, [self.constant.shape]


if __name__ == '__main__':
    import mxnet as mx
    import numpy as np

    # ConstantOP only supports CPU.
    if mx.current_context() == mx.cpu():
        # NDArray
        a = mx.nd.array([1, 2, 3])
        b = mx.nd.array([4, 5, 6])
        c = a + ConstantOP[mx.nd.NDArray](b)
        print(c)  # [5,7,9]

        # Symbol
        a_sym = mx.sym.Variable('a')
        output_sym = a_sym + ConstantOP[mx.sym.Symbol](b)
        exe = output_sym.simple_bind(
            ctx=mx.context.current_context(), a=a.shape)
        exe.forward(a=np.array([1, 2, 3]))

        print(exe.outputs[0].asnumpy())  # [5,7,9]

    '''
    ConstantOP2: accept a variable for getting the context information
    '''

    # NDArray
    a = mx.nd.array([1, 2, 3])
    b = mx.nd.array([4, 5, 6])
    c = a + ConstantOP2(a, constant=b)
    print(c)  # [5,7,9]

    # Symbol
    a_sym = mx.sym.Variable('a')
    # declare input_type explicitly because the inputs includes mx.sym.Symbol and mx.nd.NDArray
    output_sym = a_sym + ConstantOP2[mx.sym.Symbol](a_sym, constant=b)
    exe = output_sym.simple_bind(ctx=mx.context.current_context(), a=a.shape)
    exe.forward(a=np.array([1, 2, 3]))

    print(exe.outputs[0].asnumpy())  # [5,7,9]
