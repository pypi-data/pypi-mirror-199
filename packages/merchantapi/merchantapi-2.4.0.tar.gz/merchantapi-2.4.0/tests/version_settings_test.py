"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
from . import helper


def test_version_settings():
	"""
	Tests the VersionSettings model within various API Calls
	"""

	version_settings_test_serialization()
	version_settings_test_deserialization()


def version_settings_test_serialization():
	data = {
		"foo": {
			"bar": "bin",
			"baz": 1,
			"bin": 1.99
		},
		"bar": {
			"array": [
				"foo",
				"bar"
			]
		},
		"baz": "bar"
	}

	model = merchantapi.model.VersionSettings(data)

	serialized = model.to_dict()

	assert isinstance(serialized, dict)

	assert 'foo' in serialized
	assert 'bar' in serialized
	assert 'baz' in serialized

	assert serialized['foo']['bar'] == 'bin'
	assert serialized['foo']['baz'] == 1
	assert serialized['foo']['bin'] == 1.99
	assert serialized['bar']['array'][0] == 'foo'
	assert serialized['bar']['array'][1] == 'bar'
	assert serialized['baz'] == 'bar'


def version_settings_test_deserialization():
	data = {
		"foo": {
			"bar": "bin",
			"baz": 1,
			"bin": 1.99
		},
		"bar": {
			"array": [
				"foo",
				"bar"
			]
		},
		"baz": "bar"
	}

	model = merchantapi.model.VersionSettings(data)

	assert model.is_dict() is True
	assert model.is_scalar() is False
	assert model.is_list() is False

	assert model.has_item('foo') is True
	assert model.item_has_property('foo', 'bar') is True
	assert model.item_has_property('foo', 'baz') is True
	assert model.item_has_property('foo', 'bin') is True
	assert model.get_item_property('foo', 'bar') == "bin"
	assert model.get_item_property('foo', 'baz') == 1
	assert model.get_item_property('foo', 'bin') == 1.99

	assert model.has_item('bar') is True
	assert model.item_has_property('bar', 'array') is True
	assert isinstance(model.get_item_property('bar', 'array'), list)

	assert model.has_item('baz') is True
	assert model.item_has_property('baz', 'NONE') is False
	assert model.get_item('baz') == 'bar'
