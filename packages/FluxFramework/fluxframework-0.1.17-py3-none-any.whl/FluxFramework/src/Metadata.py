################################################################################
import functools
def register(methodName):
    def wrapped(fn):
        @functools.wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapped_f.methodName = methodName
        wrapped_f.methodDescription = wrapped_f.__doc__ 
        return wrapped_f
    return wrapped

def OutputMethodMetadata(method):
    print(method.methodName)
    print(method.methodDescription)
################################################################################