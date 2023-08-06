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


def test_order_price_group_update_assigned():
	"""
	Tests the OrderPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('OrderPriceGroup_Update_Assigned.xml')

	order_price_group_update_assigned_test_assignment()
	order_price_group_update_assigned_test_unassignment()


def order_price_group_update_assigned_test_assignment():
	order = helper.get_order(3651499)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_price_group_name('OrderPriceGroup_Update_Assigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupUpdateAssigned)

	check_request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)
	check_request.set_filters(
		check_request.filter_expression()
		.equal('name', 'OrderPriceGroup_Update_Assigned_1')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(True)
	check_request.set_unassigned(False)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(check_response.get_order_price_groups()) == 1
	assert check_response.get_order_price_groups()[0].get_name() == 'OrderPriceGroup_Update_Assigned_1'


def order_price_group_update_assigned_test_unassignment():
	order = helper.get_order(3651499)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_price_group_name('OrderPriceGroup_Update_Assigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupUpdateAssigned)

	check_request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)

	check_request.set_filters(
		check_request.filter_expression()
		.equal('name', 'OrderPriceGroup_Update_Assigned_2')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(check_response.get_order_price_groups()) == 1
	assert check_response.get_order_price_groups()[0].get_name() == 'OrderPriceGroup_Update_Assigned_2'
