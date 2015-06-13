#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading
import subprocess
import sys
import sublime
import sublime_plugin
import LiveReload

class MakeThread(threading.Thread):

    def __init__(self, dirname, on_compile, filename):

        self.filename = filename
        self.dirname = dirname.replace('\\', '/')
        self.command = 'make'
        self.stdout = None
        self.stderr = None
        self.on_compile = on_compile
        threading.Thread.__init__(self)

    def run(self):
        cmd = self.command

        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        test = p.stdout.read()
        if test:
            print(test)
            self.on_compile()

class Make(LiveReload.Plugin, sublime_plugin.EventListener):

    title = 'Make'
    description = 'Make'
    file_types = '*'
    this_session_only = True
    file_name = ''

    def on_post_save(self, view):
        self.original_filename = os.path.basename(view.file_name())

        if self.should_run(self.original_filename):
            self.file_name_to_refresh = \
                self.original_filename.replace('.less', '.css')
            dirname = os.path.dirname(view.file_name())
            MakeThread(dirname, self.on_compile, self.original_filename).start()

    def on_compile(self):
        print(self.file_name_to_refresh)
        settings = {
            'path': self.file_name_to_refresh,
            'apply_js_live': False,
            'apply_css_live': True,
            'apply_images_live': True,
            }
        self.sendCommand('refresh', settings, self.original_filename)