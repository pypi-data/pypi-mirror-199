#!/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-member, unused-variable, too-few-public-methods, invalid-name, unused-argument
# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import os
import sys
import pytest



# let's be sure we importing testing version, not system-installed (if any)
_path = os.path.split(os.path.abspath(__file__))[0]
_path = os.path.join(_path, '..', 'src')
sys.path.insert(0, _path)
del _path

from autoinit import autoinit, AutoinitWarning # pylint: disable=wrong-import-position


class BaseObj(object):  #pylint: disable=useless-object-inheritance
    pass


class Base:
    pass


def class_with_deco_builder(from_object=False):
    @autoinit
    class C(BaseObj if from_object else Base):
        def __init__(self, a, b='default value'):
            self.c = 'in init value'
    return C


def class_with_decorated_method_builder(from_object=True):
    class C(BaseObj if from_object else Base):
        @autoinit
        def __init__(self, a, b='default value'):
            self.c = 'in init value'
    return C


def test_classdecorator():
    C = class_with_deco_builder()
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 'default value'
    assert inst.c == 'in init value'


if sys.version_info.major == 2:
    def test_classdecorator_newstyle():
        C = class_with_deco_builder(from_object=True)
        inst = C(1)
        assert inst.a == 1
        assert inst.b == 'default value'
        assert inst.c == 'in init value'


def test_methoddecorator():
    C = class_with_decorated_method_builder()
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 'default value'
    assert inst.c == 'in init value'


if sys.version_info.major == 2:
    def test_methoddecorator_newstyle():
        C = class_with_decorated_method_builder(from_object=True)
        inst = C(1)
        assert inst.a == 1
        assert inst.b == 'default value'
        assert inst.c == 'in init value'


def test_warning_is_thrown():
    with pytest.warns(AutoinitWarning):
        class C(Base):
            @autoinit
            def not_init(self, a, b='default value'):
                self.c = 'in init value'  # pylint: disable=attribute-defined-outside-init


def test_warning_suppression():
    class C(Base):
        @autoinit(no_warn=True)
        def not_init(self, a, b='default value'):
            self.c = 'in init value'  # pylint: disable=attribute-defined-outside-init

def test_exception():
    with pytest.raises(ValueError):
        autoinit(reverse=False)(7)


def test_noreverse():
    class C(BaseObj):
        @autoinit
        def __init__(self, a, b=2):
            assert self.b == 2
    assert C(1).a == 1


def test_reverse():
    class C(BaseObj):
        @autoinit(reverse=True)
        def __init__(self, a, b=2):
            assert not hasattr(self, 'a')
            assert not hasattr(self, 'b')
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 2


def test_init_noargs():
    @autoinit
    class C(BaseObj):
        def __init__(self):
            self.q = 5
    assert C().q == 5


if sys.version_info.major == 2:
    def test_init_noargs_oldstyle():
        @autoinit
        class C:
            def __init__(self):
                self.q = 5
        assert C().q == 5


def test_exclude_one():
    class C(BaseObj):
        @autoinit(exclude='b')
        def __init__(self, a, b, c):
            pass
    inst = C(1, 2, 3)
    assert not hasattr(inst, 'b')


def test_exclude_many():
    @autoinit(exclude=['b', 'c'])
    class C(BaseObj):
        def __init__(self, a, b, c):
            assert not hasattr(self, 'b')

    inst = C(1, 2, 3)
    assert not hasattr(inst, 'c')

def test_slots():
    @autoinit
    class C(BaseObj):
        __slots__ = ['a', 'b']
        def __init__(self, a, b):
            pass
    inst = C(1, 2)
    assert inst.a == 1 and inst.b == 2

def test_slots_raises():
    with pytest.raises(AttributeError):
        @autoinit
        class C(BaseObj):
            __slots__ = ['a', 'b']
            def __init__(self, a, b, c=3):
                pass
        inst = C(1, 2)

def test_slots_excluded_not_raises():
    @autoinit(exclude='c')
    class C(BaseObj):
        __slots__ = ['a', 'b']
        def __init__(self, a, b, c=3):
            pass
    inst = C(1, 2)
    assert not hasattr(inst, 'c')

if sys.version_info.major == 2:
    def test_oldstyle_class_not_raises():
        @autoinit
        class C:
            __slots__ = ['a', 'b']
            def __init__(self, a, b, c=3):
                pass
        inst = C(1, 2)
        assert inst.c == 3

def test_kwargs():
    def foo_func():
        pass

    @autoinit
    class C(BaseObj):
        def __init__(self, a, some_callback):
            pass

    inst = C(1, some_callback=foo_func)
    assert inst.some_callback == foo_func  # pylint: disable=comparison-with-callable


def test_import_module_as_func():
    import autoinit as autoinit_module  # pylint: disable=import-outside-toplevel
    assert autoinit_module.autoinit is autoinit
