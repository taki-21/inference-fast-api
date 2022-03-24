import re

from lib.object_key import ObjectKey


def test_make_object_key():
    rtn = ObjectKey.make_object_key('pdf')
    assert re.search(r"^\d{4}\/\d{2}\/\d{2}\/\S+(\.pdf)$", rtn) is not None
