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


def test_order_shipment_list_load_query():
	"""
	Tests the OrderShipmentList_Load_Query API Call
	"""

	helper.provision_store('OrderShipmentList_Load_Query.xml')

	order_shipment_list_load_query_test_list_load()
	order_shipment_list_load_query_test_list_load_filtered()


def order_shipment_list_load_query_test_list_load():
	request = merchantapi.request.OrderShipmentListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListLoadQuery)

	assert len(response.get_order_shipments()) > 0


def order_shipment_list_load_query_test_list_load_filtered():
	valid_ids = [855855, 855856, 855857, 855858, 855859, 855860]

	request = merchantapi.request.OrderShipmentListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().is_in('order_id', valid_ids))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListLoadQuery)

	assert len(response.get_order_shipments()) == 6

	for s in response.get_order_shipments():
		assert s.get_order_id() in valid_ids
