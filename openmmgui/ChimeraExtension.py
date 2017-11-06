#!/usr/bin/env python
# encoding: utf-8

# get used to importing this in your Py27 projects!
from __future__ import print_function, division
import chimera.extension

"""
This is the file that Chimera searches for to load new extensions
at runtime. Normally, you will only need to edit:

- the returned strings in name() and description() methods

- the name of the class in both the class statement and the
  registerExtension() call at the end of the file.

"""

# Edit the name
class OpenMMExtension(chimera.extension.EMO):

    def name(self):
        # Always prefix with 'Plume'
        return 'Plume OpenMM'

    def description(self):
        # Something short but meaningful
        return "MD simulation extension OpenMM"

    def categories(self):
        # Don't touch
        return ['InsiliChem']

    def icon(self):
        # To be implemented
        return

    def activate(self):
        # Don't edit unless you know what you're doing
        self.module('gui').showUI()

# Remember to edit the class name in this call!
chimera.extension.manager.registerExtension(OpenMMExtension(__file__))