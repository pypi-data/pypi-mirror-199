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


def test_allorderpaymentlist_load_query():
	"""
	Tests the AllOrderPaymentList_Load_Query API Call
	"""

	helper.provision_store('AllOrderPaymentList_Load_Query.xml')

	allorderpaymentlist_load_query_test_list_load()


def allorderpaymentlist_load_query_test_list_load():
	order_ids = [ 979571, 979572, 979573, 979574, 979575, 979576, 979577 ]
	cod = helper.get_module('cod')

	for order_id in order_ids:
		helper.send_admin_request('Order_Authorize', {
			'Order_ID': order_id,
			'Module_ID': cod['id'],
			'Amount': 66.09,
			'Module_Data': order_id
		})

	request = merchantapi.request.AllOrderPaymentListLoadQuery(helper.init_client())

	request.filters.equal('cust_login', 'AllOrderPaymentListLoadQueryTest_Cust1')
	request.add_on_demand_column('cust_login')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AllOrderPaymentListLoadQuery)

	assert len(response.get_all_order_payments()) == 7
	for aop in response.get_all_order_payments():
		assert isinstance(aop, merchantapi.model.AllOrderPayment)
		assert isinstance(aop.get_order_payment(), merchantapi.model.OrderPayment)
		assert aop.get_id() in order_ids
		assert aop.get_id() == aop.get_order_payment().get_order_id()