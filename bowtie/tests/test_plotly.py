#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plotly testing
"""

import os
import subprocess

from selenium.webdriver import PhantomJS
# from selenium.webdriver import ActionChains

from bowtie import Layout
from bowtie.control import Nouislider
from bowtie.visual import Plotly


def callback(*args):
    """dummy function"""
    # pylint: disable=unused-argument
    pass


# pylint: disable=unused-argument
def test_plotly(remove_build):
    """
    Tests plotly.
    """
    viz = Plotly()
    ctrl = Nouislider()

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
    layout = Layout(directory=path)
    layout.add_visual(viz)
    layout.add_controller(ctrl)
    layout.subscribe(ctrl.on_change, callback)
    layout.build()

    env = os.environ
    env['PYTHONPATH'] = '{}:{}'.format(os.getcwd(), os.environ.get('PYTHONPATH', ''))
    server = subprocess.Popen(os.path.join(path, 'src/server.py'), env=env)

    driver = PhantomJS()
    driver.get('http://localhost:9991')

    assert driver.title == 'Bowtie App'

    server.kill()
