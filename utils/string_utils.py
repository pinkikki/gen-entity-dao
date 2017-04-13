# -*- coding: utf-8 -*-
import re


class StringUtils:
    @classmethod
    def to_camel(cls, val, lower_flg=False):
        camel_vals = None if val is None else list(map(lambda x: x.capitalize(), re.split("[\s_]", val.lower())))
        if lower_flg:
            camel_vals[0] = camel_vals[0].lower()
        return "".join(camel_vals)
