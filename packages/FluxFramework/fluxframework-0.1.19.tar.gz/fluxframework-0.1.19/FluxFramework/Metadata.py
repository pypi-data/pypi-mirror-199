################################################################################
import functools

def register():
    def wrapped(fn):
        @functools.wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapped_f.methodName = wrapped_f.__name__ 
        wrapped_f.methodDescription = wrapped_f.__doc__ 
        return wrapped_f
    return wrapped

def assignOrder(order):
  def do_assignment(to_func):
    to_func.order = order
    return to_func
  return do_assignment

@register()
def GetMethodOrder(method):
    '''Returns the value of the .order property on the provided method. -1 if no order is assigned'''
    try:
        return method.order
    except:
        return -1
    
@register()
def OutputMethodMetadata(method):
    '''Outputs the stored metadata for the given method object'''
    print(method.methodName)
    print(method.methodDescription)

################################################################################