# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - Teknik Informatika Unhas
"""

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
