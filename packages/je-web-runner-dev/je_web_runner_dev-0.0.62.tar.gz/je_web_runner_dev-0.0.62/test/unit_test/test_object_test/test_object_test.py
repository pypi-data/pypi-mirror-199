import sys

from je_web_runner import create_test_object
from je_web_runner import get_test_object_type_list

try:
    new_test_object = create_test_object("test_object", "id")
    print(new_test_object.test_object_type)
    print(new_test_object.test_object_name)

    assert new_test_object.test_object_type == "id"
    assert new_test_object.test_object_name == "test_object"
    print(get_test_object_type_list())
    assert get_test_object_type_list() == ['id', 'css selector', 'name', 'xpath', 'tag name', 'class name', 'link text']
except Exception as error:
    print(repr(error), file=sys.stderr)
    sys.exit(1)
