"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import pytest
from merchantapi.listquery import ListQueryRequest, FilterExpression
from . import helper

helper.configure_logging()


def test_custom_filters():
	"""
	Tests the custom filter functionality of the list query class

	:return:
	"""

	class TestListQuery(ListQueryRequest):
		available_custom_filters = {
			'int_test': 'int',
			'float_test': 'float',
			'string_test': 'str',
			'bool_test': 'bool',
			'choice_test': [
				'foo',
				'bar',
				9
			]
		}

	lq = TestListQuery()

	with pytest.raises(Exception):
		lq.set_custom_filter('invalid', 'foo')

	lq.set_custom_filter('int_test', 100)

	with pytest.raises(Exception):
		lq.set_custom_filter('int_test', 'foo')

	lq.set_custom_filter('float_test', 15.25)

	with pytest.raises(Exception):
		lq.set_custom_filter('float_test', 'foo')

	lq.set_custom_filter('string_test', 'foo')

	with pytest.raises(Exception):
		lq.set_custom_filter('string_test', 10)

	lq.set_custom_filter('bool_test', False)

	with pytest.raises(Exception):
		lq.set_custom_filter('bool_test', 10)

	lq.set_custom_filter('choice_test', 'foo')

	with pytest.raises(Exception):
		lq.set_custom_filter('choice_test', 'invalid')

	for filter in lq.get_custom_filters():
		assert filter['name'] in ['int_test','float_test','string_test','bool_test','choice_test']

		if filter['name'] is 'int_test':			assert filter['value'] is 100
		elif filter['name'] is 'float_test':		assert filter['value'] is 15.25
		elif filter['name'] is 'string_test':		assert filter['value'] is 'foo'
		elif filter['name'] is 'bool_test':			assert filter['value'] is False
		elif filter['name'] is 'choice_test':		assert filter['value'] is 'foo'
		else:
			pytest.fail('Unexpected value')

	lq.remove_custom_filter('int_test')

	for filter in lq.get_custom_filters():
		assert filter['name'] is not 'int_test'


def test_filter_expression():
	"""
	Tests the FilterExpression class

	:return:
	"""

	filter_expression_test_simple()
	filter_expression_test_complex()


def filter_expression_test_simple():
	expr = FilterExpression()

	expr.equal('foo', 'bar').and_equal('bar', 'baz')

	data = expr.to_list()

	assert len(data) == 2
	assert isinstance(data[0], dict)
	assert isinstance(data[1], dict)


def filter_expression_test_complex():
	expr = FilterExpression()
	sub = expr.expr()

	sub.equal('bin', 'bar').and_greater_than('baz', 5)
	expr.equal('foo', 'bar').and_equal('bar', 'baz').and_x(sub)

	data = expr.to_list()

	assert len(data) == 3
	assert isinstance(data[0], dict)

	assert data[0]['name'] == 'search'
	assert isinstance(data[0]['value'], list)
	assert len(data[0]['value']) == 1

	assert isinstance(data[1], dict)
	assert data[1]['name'] == 'search_AND'
	assert isinstance(data[1]['value'], list)
	assert len(data[1]['value']) == 1

	assert isinstance(data[2], dict)
	assert data[2]['name'] == 'search_AND'
	assert isinstance(data[2]['value'], list)
	assert len(data[2]['value']) == 2
