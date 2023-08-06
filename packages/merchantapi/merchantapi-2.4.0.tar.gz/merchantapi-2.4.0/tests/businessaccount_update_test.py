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


def test_business_account_update():
	"""
	Tests the BusinessAccount_Update API Call
	"""

	helper.provision_store('BusinessAccount_Update.xml')

	business_account_update_test_update()


def business_account_update_test_update():
	existing = helper.get_business_account('BusinessAccountUpdateTest_1')

	assert existing is not None

	request = merchantapi.request.BusinessAccountUpdate(helper.init_client(), existing)

	request.set_business_account_title('BusinessAccountUpdateTest_1_Modified')
	request.set_business_account_tax_exempt(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountUpdate)

	check = helper.get_business_account('BusinessAccountUpdateTest_1_Modified')

	assert check is not None
	assert check.get_title() == 'BusinessAccountUpdateTest_1_Modified'
	assert check.get_tax_exempt() == False
