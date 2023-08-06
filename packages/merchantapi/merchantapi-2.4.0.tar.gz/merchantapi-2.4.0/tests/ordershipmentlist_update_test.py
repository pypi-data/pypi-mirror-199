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


def test_order_shipment_list_update():
	"""
	Tests the OrderShipmentList_Update API Call
	"""

	helper.provision_store('OrderShipmentList_Update.xml')

	order_shipment_list_update_test_update()


def order_shipment_list_update_test_update():
	request = merchantapi.request.OrderShipmentListUpdate(helper.init_client())
	update = merchantapi.model.OrderShipmentUpdate()

	update.set_cost(1.00) \
		.set_mark_shipped(True) \
		.set_shipment_id(100) \
		.set_tracking_number('Z12312312313') \
		.set_tracking_type('UPS')

	request.add_shipment_update(update)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderShipmentListUpdate)
