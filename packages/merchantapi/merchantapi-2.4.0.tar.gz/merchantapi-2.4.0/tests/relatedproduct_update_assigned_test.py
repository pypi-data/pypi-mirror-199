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


def test_related_product_update_assigned():
	"""
	Tests the RelatedProduct_Update_Assigned API Call
	"""

	helper.provision_store('RelatedProduct_Update_Assigned.xml')

	related_product_update_assigned_test_assignment()
	related_product_update_assigned_test_unassignment()


def related_product_update_assigned_test_assignment():
	product = helper.get_product('RelatedProductUpdateAssignedTest_1')

	assert product is not None

	related = helper.get_related_products(product.get_code(), '', True, False)
	to_assign = helper.get_product(product.get_code() + '_1')

	assert len(related) >= 0
	assert to_assign is not None

	for r in related:
		assert r.get_id() != to_assign.get_id()

	request = merchantapi.request.RelatedProductUpdateAssigned(helper.init_client(), product)

	request.set_related_product_id(to_assign.get_id())
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductUpdateAssigned)

	check_related = helper.get_related_products(product.get_code(), to_assign.get_code(), True, False)

	assert len(check_related) == 1


def related_product_update_assigned_test_unassignment():

	product = helper.get_product('RelatedProductUpdateAssignedTest_1')

	assert product is not None

	related = helper.get_related_products(product.get_code(), product.get_code() + '_2', True, False)
	to_unassign = helper.get_product(product.get_code() + '_2')

	assert len(related) == 1
	assert to_unassign is not None

	request = merchantapi.request.RelatedProductUpdateAssigned(helper.init_client(), product)

	request.set_related_product_id(to_unassign.get_id())
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductUpdateAssigned)

	check_related = helper.get_related_products(product.get_code(), to_unassign.get_code(), False, True)

	assert len(check_related) == 1
