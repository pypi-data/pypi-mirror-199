# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


class FieldAlias:

    def __init__(self, attr):
        self.name = attr

    def __get__(self, instance, owner):
        return getattr(instance or owner, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)
