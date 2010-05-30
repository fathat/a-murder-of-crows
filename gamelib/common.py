#!/usr/bin/env python
import sys

def Property(function):
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':function.__doc__}
    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict((k,locals.get(k)) for k in keys))
            sys.settrace(None)
        return probeFunc
    sys.settrace(probeFunc)
    function()
    return property(**func_locals)


def approach_value(target, current, step):
    step = abs(step)
    if target < current:
        if current - step < target:
            return target
        else:
            return current - step
    elif target > current:
        if current + step > target:
            return target
        else:
            return current + step
    return target