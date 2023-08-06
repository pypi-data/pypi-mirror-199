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


def test_order_delete():
	"""
	Tests the Order_Delete API Call
	"""

	order_delete_test_deletion()


def order_delete_test_deletion():
	createrequest = merchantapi.request.OrderCreate(helper.init_client())

	createresponse = createrequest.send()

	helper.validate_response_success(createresponse, merchantapi.response.OrderCreate)

	assert isinstance(createresponse.get_order(), merchantapi.model.Order)
	assert createresponse.get_order().get_id() > 0

	request = merchantapi.request.OrderDelete(helper.init_client(), createresponse.get_order())

	assert request.get_order_id() == createresponse.get_order().get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderDelete)
