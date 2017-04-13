# -*- coding: utf-8 -*-
import re


class StringUtils:
    @classmethod
    def to_camel(cls, val, lower_flg=False):
        camel_val = None if val is None else "".join(map(
            lambda x: x.capitalize(), re.split("[\s_]", val.lower())))
        return camel_val.lower() if lower_flg else camel_val
