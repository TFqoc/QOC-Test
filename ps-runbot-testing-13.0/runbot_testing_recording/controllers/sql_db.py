# -*- coding: utf-8 -*-
import re
re_write_db = re.compile(r'\b(update|delete|insert)\b', re.I)
from odoo.sql_db import Cursor

old_execute = Cursor.execute

def new_execute(self, query, params=None, log_exceptions=None):
    result = old_execute(self, query, params, log_exceptions)

    string_query = query if isinstance(query,str) else query.as_string()

    if re_write_db.search(string_query):
        self.method_is_writing_in_db = True
    return result

Cursor.execute = new_execute
