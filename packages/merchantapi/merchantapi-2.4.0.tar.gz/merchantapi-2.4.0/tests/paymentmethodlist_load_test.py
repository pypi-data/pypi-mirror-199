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


def test_payment_method_list_load():
	"""
	Tests the PaymentMethodList_Load API Call
	"""

	helper.provision_store('PaymentMethodList_Load.xml')

	payment_method_list_load_test_list_load()


def payment_method_list_load_test_list_load():
	modules = helper.load_modules_by_feature('payment', ['cod', 'check'])

	assert isinstance(modules, list)
	assert len(modules) == 2

	request = merchantapi.request.PaymentMethodListLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PaymentMethodListLoad)

	assert isinstance(response.get_payment_methods(), list)
	assert len(response.get_payment_methods()) >= 2

	for pm in response.get_payment_methods():
		assert isinstance(pm, merchantapi.model.PaymentMethod)
		assert pm.get_module_api() > 0
		assert pm.get_module_id() > 0
		assert pm.get_method_code() not in (None, '')
		assert pm.get_method_name() not in (None, '')

	for module in modules:
		match = None

		for pm in response.get_payment_methods():
			if pm.get_module_id() == module['id']:
				match = pm

		assert match is not None
