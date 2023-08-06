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


def test_price_group_insert():
	"""
	Tests the PriceGroup_Insert API Call
	"""

	helper.provision_store('PriceGroup_Insert.xml')

	price_group_insert_test_insertion()


def price_group_insert_test_insertion():
	assert helper.get_price_group('PriceGroupInsertTest_1') is None

	excluded_price_group = helper.get_price_group('PriceGroupInsertTest_Exclusion')

	assert excluded_price_group is not None

	request = merchantapi.request.PriceGroupInsert(helper.init_client())

	request.set_name("PriceGroupInsertTest_1")
	request.set_customer_scope(merchantapi.model.PriceGroup.ELIGIBILITY_ALL)
	request.set_rate(merchantapi.model.PriceGroup.DISCOUNT_TYPE_RETAIL)
	request.set_discount(1.00)
	request.set_markup(1.00)
	request.set_module_code('discount_basket')
	request.set_exclusion(True)
	request.set_description("PriceGroupInsertTest_1")
	request.set_display(False)
	request.set_date_time_start(100)
	request.set_date_time_end(120)
	request.set_qualifying_min_subtotal(2.00)
	request.set_qualifying_max_subtotal(3.00)
	request.set_qualifying_min_quantity(4)
	request.set_qualifying_max_quantity(5)
	request.set_qualifying_min_weight(6.00)
	request.set_qualifying_max_weight(7.00)
	request.set_basket_min_subtotal(8.00)
	request.set_basket_max_subtotal(9.00)
	request.set_basket_min_quantity(10)
	request.set_basket_max_quantity(11)
	request.set_basket_min_weight(12.00)
	request.set_basket_max_weight(13.00)
	request.set_priority(2)
	request.set_module_field('Basket_Discount', 1.00)
	request.set_module_field('Basket_MaxDiscount', 1.00)
	request.set_module_field('Basket_Type', 'fixed')

	exclusion = merchantapi.model.PriceGroupExclusion()
	exclusion.set_id(excluded_price_group.get_id())
	exclusion.set_scope(merchantapi.model.PriceGroupExclusion.EXCLUSION_SCOPE_GROUP)
	
	request.add_price_group_exclusion(exclusion)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupInsert)

	assert isinstance(response.get_price_group(), merchantapi.model.PriceGroup)
	assert response.get_price_group().get_discount() == 0.00
	assert response.get_price_group().get_markup() == 0.00
	assert response.get_price_group().get_exclusion() == False
	assert response.get_price_group().get_name() == 'PriceGroupInsertTest_1'
	assert response.get_price_group().get_description() == 'PriceGroupInsertTest_1'
	assert response.get_price_group().get_display() == False
	assert response.get_price_group().get_minimum_subtotal() == 2.00
	assert response.get_price_group().get_maximum_subtotal() == 3.00
	assert response.get_price_group().get_minimum_quantity() == 4.00
	assert response.get_price_group().get_maximum_quantity() == 5.00
	assert response.get_price_group().get_minimum_weight() == 6.00
	assert response.get_price_group().get_maximum_weight() == 7.00
	assert response.get_price_group().get_basket_minimum_subtotal() == 8.00
	assert response.get_price_group().get_basket_maximum_subtotal() == 9.00
	assert response.get_price_group().get_basket_minimum_quantity() == 10.00
	assert response.get_price_group().get_basket_maximum_quantity() == 11.00
	assert response.get_price_group().get_basket_minimum_weight() == 12.00
	assert response.get_price_group().get_basket_maximum_weight() == 13.00

	check = helper.get_price_group('PriceGroupInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_price_group().get_id()

	exclusion_check = helper.get_price_group_exclusion(response.get_price_group().get_name(), excluded_price_group.get_name())
	assert exclusion_check is not None
