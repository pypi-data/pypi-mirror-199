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


def test_product_list_load_query():
	"""
	Tests the ProductList_Load_Query API Call
	"""

	helper.upload_image('graphics/ProductListLoadQuery1.jpg')
	helper.upload_image('graphics/ProductListLoadQuery2.jpg')
	helper.upload_image('graphics/ProductListLoadQuery3.jpg')
	helper.upload_image('graphics/ProductListLoadQuery4.jpg')
	helper.upload_image('graphics/ProductListLoadQuery5.jpg')
	helper.upload_image('graphics/ProductListLoadQuery6.jpg')
	helper.upload_image('graphics/ProductListLoadQuery7.jpg')
	helper.provision_store('ProductList_Load_Query_v10.xml')

	product_list_load_query_test_list_load()
	product_list_load_query_test_list_load_with_custom_fields()
	product_list_load_query_test_list_load_imagetypes()
	product_list_load_query_test_list_load_subscription_fields()


def product_list_load_query_test_list_load():
	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
		.like('code', 'ProductListLoadQueryTest_%')
		.and_not_like('code', 'ProductListLoadQueryTest_Rel_%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert isinstance(response.get_products(), list)
	assert len(response.get_products()) == 7

	for i, product in enumerate(response.get_products()):
		assert isinstance(product, merchantapi.model.Product)
		assert product.get_code() == 'ProductListLoadQueryTest_%d' % int(i+1)
		assert product.get_price() == 2.00
		assert product.get_cost() == 1.00
		assert product.get_weight() == 1.00
		assert product.get_active() is False
		assert product.get_taxable() is False


def product_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ProductListLoadQueryTest_%')
			.and_not_like('code', 'ProductListLoadQueryTest_Rel_%')
	)

	request.set_on_demand_columns(request.get_available_on_demand_columns()) \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_checkbox') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_imageupload') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_text') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_textarea') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_dropdown') \
		.add_on_demand_column('CustomField_Values:customfields:ProductListLoadQueryTest_multitext')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert isinstance(response.get_products(), list)
	assert len(response.get_products()) == 7

	for i, product in enumerate(response.get_products()):
		assert isinstance(product, merchantapi.model.Product)
		assert product.get_code() == 'ProductListLoadQueryTest_%d' % int(i+1)
		assert product.get_price() == 2.00
		assert product.get_cost() == 1.00
		assert product.get_weight() == 1.00
		assert product.get_active() is False
		assert product.get_taxable() is False

		if product.get_code() in ['ProductListLoadQueryTest_1', 'ProductListLoadQueryTest_2']:
			assert isinstance(product.get_attributes(), list)
			assert len(product.get_attributes()) > 0

			for attribute in product.get_attributes():
				assert isinstance(attribute, merchantapi.model.ProductAttribute)

				if attribute.get_type() == 'select':
					assert isinstance(attribute.get_options(), list)
					assert len(attribute.get_options()) > 0

					for option in attribute.get_options():
						assert isinstance(option, merchantapi.model.ProductOption)

		assert isinstance(product.get_related_products(), list)
		assert len(product.get_related_products()) > 0

		for related in product.get_related_products():
			assert isinstance(related, merchantapi.model.RelatedProduct)
			assert related.get_code() in [
				'ProductListLoadQueryTest_Rel_1',
				'ProductListLoadQueryTest_Rel_2',
				'ProductListLoadQueryTest_Rel_3',
				'ProductListLoadQueryTest_Rel_4',
				'ProductListLoadQueryTest_Rel_5',
				'ProductListLoadQueryTest_Rel_6',
				'ProductListLoadQueryTest_Rel_7'
			]

		assert isinstance(product.get_categories(), list)
		assert len(product.get_categories()) > 0

		for category in product.get_categories():
			assert isinstance(category, merchantapi.model.Category)
			assert category.get_code() in [
				'ProductListLoadQueryTest_1',
				'ProductListLoadQueryTest_2',
				'ProductListLoadQueryTest_3',
				'ProductListLoadQueryTest_4',
				'ProductListLoadQueryTest_5',
				'ProductListLoadQueryTest_6',
				'ProductListLoadQueryTest_7'
			]

		assert isinstance(product.get_product_image_data(), list)
		assert len(product.get_product_image_data()) > 0

		for imagedata in product.get_product_image_data():
			assert isinstance(imagedata, merchantapi.model.ProductImageData)
			assert imagedata.get_image() in [
				'graphics/00000001/1/ProductListLoadQuery1.jpg',
				'graphics/00000001/1/ProductListLoadQuery2.jpg',
				'graphics/00000001/1/ProductListLoadQuery3.jpg',
				'graphics/00000001/1/ProductListLoadQuery4.jpg',
				'graphics/00000001/1/ProductListLoadQuery5.jpg',
				'graphics/00000001/1/ProductListLoadQuery6.jpg',
				'graphics/00000001/1/ProductListLoadQuery7.jpg'
			]

		assert isinstance(product.get_custom_field_values(), merchantapi.model.CustomFieldValues)
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_checkbox', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_imageupload', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_text', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_textarea', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_dropdown', 'customfields') is True
		assert product.get_custom_field_values().has_value('ProductListLoadQueryTest_multitext', 'customfields') is True


def product_list_load_query_test_list_load_imagetypes():
	types = [ 'PLLQ_ImageTypes_1', 'PLLQ_ImageTypes_2', 'PLLQ_ImageTypes_3' ]

	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.filters.equal('code', 'PLLQ_ImageTypes_1')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_1')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_2')
	request.add_on_demand_column('imagetype:PLLQ_ImageTypes_3')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert len(response.get_products()) == 1
	assert len(response.get_products()[0].get_image_types()) == 3

	for (code,id) in response.get_products()[0].get_image_types().items():
		assert code in types


def product_list_load_query_test_list_load_subscription_fields():
	# See MMAPI-168
	
	request = merchantapi.request.ProductListLoadQuery(helper.init_client())

	request.filters.equal('code', 'PLLQ_SubFields_1')
	request.add_on_demand_column('subscriptionsettings')
	request.add_on_demand_column('subscriptionterms')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	assert len(response.get_products()) == 1
	
	product = response.get_products()[0]

	assert product.get_subscription_settings() is not None
	assert product.get_subscription_settings()

	assert product.get_subscription_settings().get_product_id() == product.get_id()
	assert product.get_subscription_settings().get_enabled() is True
	assert product.get_subscription_settings().get_mandatory() is True
	assert product.get_subscription_settings().get_can_cancel() is True
	assert product.get_subscription_settings().get_cancel_minimum_required_orders() == 0
	assert product.get_subscription_settings().get_can_change_quantities() is True
	assert product.get_subscription_settings().get_quantities_minimum_required_orders() == 1
	assert product.get_subscription_settings().get_can_change_term() is True
	assert product.get_subscription_settings().get_term_minimum_required_orders() == 2
	assert product.get_subscription_settings().get_can_change_next_delivery_date() is True
	assert product.get_subscription_settings().get_next_delivery_date_minimum_required_orders() == 3

	assert len(product.get_subscription_terms()) == 1

	product.get_subscription_terms()[0].get_id() > 0
	product.get_subscription_terms()[0].get_product_id() == product.get_id()

