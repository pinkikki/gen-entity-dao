# -*- coding: utf-8 -*-
import re


class StringUtils:
    @classmethod
    def to_camel(cls, val):
        return None if val is None else "".join(map(
            lambda x: x.capitalize(), re.split("[\s_]", val.lower())))