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


def test_business_account_list_delete():
	"""
	Tests the BusinessAccountList_Delete API Call
	"""

	helper.provision_store('BusinessAccountList_Delete.xml')

	business_account_list_delete_test_deletion()


def business_account_list_delete_test_deletion():
	list_request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())
	list_request.set_filters(list_request.filter_expression().like('title', 'BusinessAccountListDeleteTest%'))
	list_response = list_request.send()

	assert len(list_response.get_business_accounts()) == 3

	request = merchantapi.request.BusinessAccountListDelete(helper.init_client())

	for a in list_response.get_business_accounts():
		request.add_business_account(a)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountListDelete)

	check_list_request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())
	check_list_request.set_filters(check_list_request.filter_expression().like('title', 'BusinessAccountListDeleteTest%'))
	check_list_response = check_list_request.send()

	assert len(check_list_response.get_business_accounts())  == 0
