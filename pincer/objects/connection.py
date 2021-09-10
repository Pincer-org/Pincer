# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from dataclasses import dataclass, MISSING
from typing import List

from pincer.objects import Integration
from pincer.objects.user import VisibilityType
from pincer.utils import APIObject, APINullable


@dataclass
class Connection(APIObject):
    """
    The connection object that the user has attached.

    :param id:
        id of the connection account

    :param name:
        the username of the connection account

    :param type:
        the service of the connection (twitch, youtube)

    :param revoked:
        whether the connection is revoked

    :param integrations:
        an array of partial server integrations

    :param verified:
        whether the connection is verified

    :param friend_sync:
        whether friend sync is enabled for this connection

    :param show_activity:
        whether activities related to this connection
        will be shown in presence updates
    """
    id: str
    name: str
    type: str
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: VisibilityType

    revoked: APINullable[bool] = MISSING
    integrations: APINullable[List[Integration]] = MISSING
