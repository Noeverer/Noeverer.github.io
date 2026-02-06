# -*- coding: utf-8 -*-
"""
测试模块
"""

from .test_all import run_all_tests
from .test_functional import main as run_functional_tests

__all__ = ['run_all_tests', 'run_functional_tests']
