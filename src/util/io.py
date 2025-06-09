#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Henrique Kops

# built-in
import os


class IO:

    """Wrapper class for OS filesystem interaction"""

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def create_directory_if_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def gen_path(directory, file_name, extension):
        return f'{directory}/{file_name}.{extension}'
