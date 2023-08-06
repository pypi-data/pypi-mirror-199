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


def test_business_account_insert():
	"""
	Tests the BusinessAccount_Insert API Call
	"""

	helper.provision_store('BusinessAccount_Insert.xml')

	business_account_insert_test_insertion()


def business_account_insert_test_insertion():
	existing = helper.get_business_account('BusinessAccountInsertTest_1')

	assert existing is None

	request = merchantapi.request.BusinessAccountInsert(helper.init_client())

	request.set_business_account_title('BusinessAccountInsertTest_1')
	request.set_business_account_tax_exempt(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountInsert)
	
	assert isinstance(response.get_business_account(), merchantapi.model.BusinessAccount)
	assert response.get_business_account().get_title() == 'BusinessAccountInsertTest_1'
	assert response.get_business_account().get_tax_exempt() == True

	check = helper.get_business_account('BusinessAccountInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_business_account().get_id()
