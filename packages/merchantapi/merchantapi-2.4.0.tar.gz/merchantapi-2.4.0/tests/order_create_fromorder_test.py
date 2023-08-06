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


def test_order_create_from_order():
	"""
	Tests the Order_Create_FromOrder API Call
	"""

	helper.provision_store('Order_Create_FromOrder.xml')

	order_create_from_order_test_create()
	order_create_from_order_test_invalid_order()


def order_create_from_order_test_create():
	order = helper.get_order(10520)

	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() == 10520

	request = merchantapi.request.OrderCreateFromOrder(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreateFromOrder)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_id() != 10520


def order_create_from_order_test_invalid_order():
	request = merchantapi.request.OrderCreateFromOrder(helper.init_client())

	request.set_order_id(8980999)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderCreateFromOrder)
