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


def test_copyproductrules_insert():
	"""
	Tests the CopyProductRules_Insert API Call
	"""

	helper.provision_store('CopyProductRules_Insert.xml')

	copyproductrules_insert_test_insert()


def copyproductrules_insert_test_insert():
	request = merchantapi.request.CopyProductRulesInsert(helper.init_client())

	request.set_name('CopyProductRules_Insert_1')
	request.set_core_product_data(True)
	request.set_attributes(True)
	request.set_category_assignments(True)
	request.set_inventory_settings(False)
	request.set_inventory_level(True)
	request.set_images(False)
	request.set_related_products(True)
	request.set_upsale(False)
	request.set_availability_group_assignments(True)
	request.set_price_group_assignments(False)
	request.set_digital_download_settings(True)
	request.set_gift_certificate_sales(False)
	request.set_subscription_settings(True)
	request.set_payment_rules(False)
	request.set_shipping_rules(True)
	request.set_product_kits(False)
	request.set_product_variants(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesInsert)

	assert response.get_copy_product_rule() is not None
	assert response.get_copy_product_rule().get_name() == request.get_name()
	assert response.get_copy_product_rule().get_core_product_data() == request.get_core_product_data()
	assert response.get_copy_product_rule().get_attributes() == request.get_attributes()
	assert response.get_copy_product_rule().get_category_assignments() == request.get_category_assignments()
	assert response.get_copy_product_rule().get_inventory_settings() == request.get_inventory_settings()
	assert response.get_copy_product_rule().get_inventory_level() == request.get_inventory_level()
	assert response.get_copy_product_rule().get_images() == request.get_images()
	assert response.get_copy_product_rule().get_related_products() == request.get_related_products()
	assert response.get_copy_product_rule().get_upsale() == request.get_upsale()
	assert response.get_copy_product_rule().get_availability_group_assignments() == request.get_availability_group_assignments()
	assert response.get_copy_product_rule().get_price_group_assignments() == request.get_price_group_assignments()
	assert response.get_copy_product_rule().get_digital_download_settings() == request.get_digital_download_settings()
	assert response.get_copy_product_rule().get_gift_certificate_sales() == request.get_gift_certificate_sales()
	assert response.get_copy_product_rule().get_subscription_settings() == request.get_subscription_settings()
	assert response.get_copy_product_rule().get_payment_rules() == request.get_payment_rules()
	assert response.get_copy_product_rule().get_shipping_rules() == request.get_shipping_rules()
	assert response.get_copy_product_rule().get_product_kits() == request.get_product_kits()
	assert response.get_copy_product_rule().get_product_variants() == request.get_product_variants()