
import os
from classy_xml import ClassyXml

filepath = os.path.split(__file__)[0]
test_xml = os.path.join(filepath, 'test.xml')
obj = ClassyXml(test_xml)
x = 1


def test_basic_element_length():
    assert len(obj.basic_element) == 1


def test_basic_element_text():
    assert obj.basic_element.text == 'basic_element_text'


def test_multi_element_length():
    assert len(obj.multi_element) == 2


def test_multi_element_0_text():
    assert obj.multi_element[0].text == 'multi_element_text_0'


def test_multi_element_1_text():
    assert obj.multi_element[1].text == 'multi_element_text_1'


def test_empty_element_with_attributes_length():
    assert len(obj.empty_element_with_attributes) == 1


def test_empty_element_with_attributes_text():
    assert obj.empty_element_with_attributes.text is None


def test_empty_element_with_attributes_attributes():
    assert obj.empty_element_with_attributes.name == 'attr_name'
    assert obj.empty_element_with_attributes.value == 'attr_value'


def test_empty_multi_element_with_attributes_length():
    assert len(obj.empty_multi_element_with_attributes) == 2


def test_empty_multi_element_with_attributes_text():
    assert obj.empty_multi_element_with_attributes[0].text is None
    assert obj.empty_multi_element_with_attributes[1].text is None


def test_empty_multi_element_with_attributes_attributes():
    assert obj.empty_multi_element_with_attributes[0].name == 'attr_0_name'
    assert obj.empty_multi_element_with_attributes[0].value == 'attr_0_value'
    assert obj.empty_multi_element_with_attributes[1].name == 'attr_1_name'
    assert obj.empty_multi_element_with_attributes[1].value == 'attr_1_value'


def test_basic_element_with_attributes_length():
    assert len(obj.basic_element_with_attributes) == 1


def test_basic_element_with_attributes_text():
    assert obj.basic_element_with_attributes.text == 'basic_element_with_attributes_text'


def test_basic_element_with_attributes_attributes():
    assert obj.basic_element_with_attributes.name == 'attr_name'
    assert obj.basic_element_with_attributes.value == 'attr_value'


def test_multi_element_with_attributes_length():
    assert len(obj.multi_element_with_attributes) == 2


def test_multi_element_with_attributes_text():
    assert obj.multi_element_with_attributes[0].text == 'multi_element_with_attributes_text_0'
    assert obj.multi_element_with_attributes[1].text == 'multi_element_with_attributes_text_1'


def test_multi_element_with_attributes_attributes():
    assert obj.multi_element_with_attributes[0].name == 'attr_0_name'
    assert obj.multi_element_with_attributes[0].value == 'attr_0_value'
    assert obj.multi_element_with_attributes[1].name == 'attr_1_name'
    assert obj.multi_element_with_attributes[1].value == 'attr_1_value'


def test_basic_nested_element_length():
    assert len(obj.basic_nested_element) == 1


def test_basic_nested_element__basic_element_child_length():
    assert len(obj.basic_nested_element.basic_element_child) == 1


def test_basic_nested_element__basic_element_child_text():
    assert obj.basic_nested_element.basic_element_child.text == 'basic_element_child_text'


def test_basic_nested_element__multi_element_child_length():
    assert len(obj.basic_nested_element.multi_element_child) == 2


def test_basic_nested_element__multi_element_child_text():
    assert obj.basic_nested_element.multi_element_child[0].text == 'multi_element_child_text_0'
    assert obj.basic_nested_element.multi_element_child[1].text == 'multi_element_child_text_1'


def test_basic_nested_element__empty_element_with_attributes_child_length():
    assert len(
        obj.basic_nested_element.empty_element_with_attributes_child) == 1


def test_basic_nested_element__empty_element_with_attributes_child_text():
    assert obj.basic_nested_element.empty_element_with_attributes_child.text is None


def test_basic_nested_element__empty_element_with_attributes_child_attributes():
    assert obj.basic_nested_element.empty_element_with_attributes_child.name == 'child_attr_name'
    assert obj.basic_nested_element.empty_element_with_attributes_child.value == 'child_attr_value'


def test_basic_nested_element__empty_multi_element_with_attributes_child_length():
    assert len(
        obj.basic_nested_element.empty_multi_element_with_attributes_child) == 2


def test_basic_nested_element__empty_multi_element_with_attributes_child_text():
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        0].text is None
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        1].text is None


def test_basic_nested_element__empty_multi_element_with_attributes_child_attributes():
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        0].name == 'child_attr_0_name'
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        0].value == 'child_attr_0_value'
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        1].name == 'child_attr_1_name'
    assert obj.basic_nested_element.empty_multi_element_with_attributes_child[
        1].value == 'child_attr_1_value'


def test_basic_nested_element__basic_element_with_attributes_child_length():
    assert len(
        obj.basic_nested_element.basic_element_with_attributes_child) == 1


def test_basic_nested_element__basic_element_with_attributes_child_text():
    assert obj.basic_nested_element.basic_element_with_attributes_child.text == 'basic_element_with_attributes_child_text'


def test_basic_nested_element__basic_element_with_attributes_child_attributes():
    assert obj.basic_nested_element.basic_element_with_attributes_child.name == 'child_attr_name'
    assert obj.basic_nested_element.basic_element_with_attributes_child.value == 'child_attr_value'


def test_basic_nested_element__multi_element_with_attributes_child_length():
    assert len(
        obj.basic_nested_element.multi_element_with_attributes_child) == 2


def test_basic_nested_element__multi_element_with_attributes_child_text():
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        0].text == 'multi_element_with_attributes_child_text_0'
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        1].text == 'multi_element_with_attributes_child_text_1'


def test_basic_nested_element__multi_element_with_attributes_child_attributes():
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        0].name == 'child_attr_0_name'
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        0].value == 'child_attr_0_value'
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        1].name == 'child_attr_1_name'
    assert obj.basic_nested_element.multi_element_with_attributes_child[
        1].value == 'child_attr_1_value'


def test_multi_nested_element_length():
    assert len(obj.multi_nested_element) == 2


def test_multi_nested_element__basic_element_child_length():
    assert len(obj.multi_nested_element[0].basic_element_child) == 1
    assert len(obj.multi_nested_element[1].basic_element_child) == 1


def test_multi_nested_element__basic_element_child_text():
    assert obj.multi_nested_element[0].basic_element_child.text == 'basic_element_child_0_text'
    assert obj.multi_nested_element[1].basic_element_child.text == 'basic_element_child_1_text'


def test_multi_nested_element__multi_element_child_length():
    assert len(obj.multi_nested_element[0].multi_element_child) == 2
    assert len(obj.multi_nested_element[1].multi_element_child) == 2


def test_multi_nested_element__multi_element_child_text():
    assert obj.multi_nested_element[0].multi_element_child[0].text == 'multi_element_child_0_text_0'
    assert obj.multi_nested_element[0].multi_element_child[1].text == 'multi_element_child_0_text_1'
    assert obj.multi_nested_element[1].multi_element_child[0].text == 'multi_element_child_1_text_0'
    assert obj.multi_nested_element[1].multi_element_child[1].text == 'multi_element_child_1_text_1'


def test_multi_nested_element__empty_element_with_attributes_child_length():
    assert len(
        obj.multi_nested_element[0].empty_element_with_attributes_child) == 1
    assert len(
        obj.multi_nested_element[1].empty_element_with_attributes_child) == 1


def test_multi_nested_element__empty_element_with_attributes_child_text():
    assert obj.multi_nested_element[0].empty_element_with_attributes_child.text is None
    assert obj.multi_nested_element[1].empty_element_with_attributes_child.text is None


def test_multi_nested_element__empty_element_with_attributes_child_attributes():
    assert obj.multi_nested_element[0].empty_element_with_attributes_child.name == 'child_0_attr_name'
    assert obj.multi_nested_element[0].empty_element_with_attributes_child.value == 'child_0_attr_value'
    assert obj.multi_nested_element[1].empty_element_with_attributes_child.name == 'child_1_attr_name'
    assert obj.multi_nested_element[1].empty_element_with_attributes_child.value == 'child_1_attr_value'


def test_multi_nested_element__empty_multi_element_with_attributes_child_length():
    assert len(
        obj.multi_nested_element[0].empty_multi_element_with_attributes_child) == 2
    assert len(
        obj.multi_nested_element[1].empty_multi_element_with_attributes_child) == 2


def test_multi_nested_element__empty_multi_element_with_attributes_child_text():
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        0].text is None
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        1].text is None
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        0].text is None
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        1].text is None


def test_multi_nested_element__empty_multi_element_with_attributes_child_attributes():
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        0].name == 'child_0_attr_0_name'
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        0].value == 'child_0_attr_0_value'
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        1].name == 'child_0_attr_1_name'
    assert obj.multi_nested_element[0].empty_multi_element_with_attributes_child[
        1].value == 'child_0_attr_1_value'
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        0].name == 'child_1_attr_0_name'
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        0].value == 'child_1_attr_0_value'
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        1].name == 'child_1_attr_1_name'
    assert obj.multi_nested_element[1].empty_multi_element_with_attributes_child[
        1].value == 'child_1_attr_1_value'


def test_multi_nested_element__basic_element_with_attributes_child_length():
    assert len(
        obj.multi_nested_element[0].basic_element_with_attributes_child) == 1
    assert len(
        obj.multi_nested_element[1].basic_element_with_attributes_child) == 1


def test_multi_nested_element__basic_element_with_attributes_child_text():
    assert obj.multi_nested_element[0].basic_element_with_attributes_child.text == 'basic_element_with_attributes_child_0_text'
    assert obj.multi_nested_element[1].basic_element_with_attributes_child.text == 'basic_element_with_attributes_child_1_text'


def test_multi_nested_element__basic_element_with_attributes_child_attributes():
    assert obj.multi_nested_element[0].basic_element_with_attributes_child.name == 'child_0_attr_name'
    assert obj.multi_nested_element[0].basic_element_with_attributes_child.value == 'child_0_attr_value'
    assert obj.multi_nested_element[1].basic_element_with_attributes_child.name == 'child_1_attr_name'
    assert obj.multi_nested_element[1].basic_element_with_attributes_child.value == 'child_1_attr_value'


def test_multi_nested_element__multi_element_with_attributes_child_length():
    assert len(
        obj.multi_nested_element[0].multi_element_with_attributes_child) == 2
    assert len(
        obj.multi_nested_element[1].multi_element_with_attributes_child) == 2


def test_multi_nested_element__multi_element_with_attributes_child_text():
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        0].text == 'multi_element_with_attributes_child_0_text_0'
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        1].text == 'multi_element_with_attributes_child_0_text_1'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        0].text == 'multi_element_with_attributes_child_1_text_0'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        1].text == 'multi_element_with_attributes_child_1_text_1'


def test_multi_nested_element__multi_element_with_attributes_child_attributes():
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        0].name == 'child_0_attr_0_name'
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        0].value == 'child_0_attr_0_value'
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        1].name == 'child_0_attr_1_name'
    assert obj.multi_nested_element[0].multi_element_with_attributes_child[
        1].value == 'child_0_attr_1_value'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        0].name == 'child_1_attr_0_name'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        0].value == 'child_1_attr_0_value'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        1].name == 'child_1_attr_1_name'
    assert obj.multi_nested_element[1].multi_element_with_attributes_child[
        1].value == 'child_1_attr_1_value'


def test_multi_nested_element__unique_element_child_existence():
    assert hasattr(obj.multi_nested_element[0], 'unique_element_child')
    assert not hasattr(obj.multi_nested_element[1], 'unique_element_child')
