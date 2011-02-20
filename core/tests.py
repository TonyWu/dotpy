"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import re

from django.test import TestCase

from dotpy.core.utils import *

__test__ = {
"UtilsTest": """
>>> generate_code(-1)
''
>>> generate_code(0)
''
>>> len(generate_code(1))
1
>>> code = generate_code(10)
>>> len(code)
10
>>> code.strip() == code
True
>>> generate_code(10) != code
True
>>> pattern = r'[a-zA-Z0-9]{7}'
>>> bool(re.match(pattern, code))
True
>>> results = []
>>> for i in range(1, 10):
...     code = generate_code(7)
...     results.append(bool(re.match(pattern, code)))
>>> results == [True for i in range(1, 10)]
True
""",
}

