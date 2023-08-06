"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import requests
import logging
import merchantapi.request
import merchantapi.response
import merchantapi.model
import merchantapi.listquery
from . credentials import MerchantApiTestCredentials
from merchantapi.client import Client
from merchantapi.abstract import Response
from merchantapi.logging import FileLogger
from pathlib import Path
from http.client import HTTPConnection
from datetime import date

FILE_LOGGER = None


def configure_logging():
	if MerchantApiTestCredentials.DEBUG_OUTPUT is True:
		HTTPConnection.debuglevel = 1
		logging.basicConfig()
		logging.getLogger().setLevel(logging.DEBUG)
		log = logging.getLogger("requests.packages.urllib3")
		log.setLevel(logging.DEBUG)
		log.propagate = True


def configure_permissions():
	if MerchantApiTestCredentials.AUTO_PROVISION_PERMISSIONS is True:
		enable_api_function_access('Provision_Domain')
		enable_api_function_access('Provision_Store', MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
		enable_api_function_access('PrintQueueJobList_Load_Query', MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
		enable_api_function_access('PrintQueueList_Load_Query', MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
		enable_api_function_access('PrintQueueJob_Delete', MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)


def init_client():
	global FILE_LOGGER

	if MerchantApiTestCredentials.LOG_FILE is not None and isinstance(MerchantApiTestCredentials.LOG_FILE, str) and len(MerchantApiTestCredentials.LOG_FILE):
		if FILE_LOGGER is None:
			FILE_LOGGER = FileLogger(MerchantApiTestCredentials.LOG_FILE)

	client = Client(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, MerchantApiTestCredentials.MERCHANT_API_API_TOKEN, MerchantApiTestCredentials.MERCHANT_API_SIGNING_KEY, {
		'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE,
		'ssl_verify': MerchantApiTestCredentials.SSL_VERIFY
	})

	if FILE_LOGGER is not None:
		client.set_logger(FILE_LOGGER)

	return client


def validate_response_object(response, expectedtype=None):
	assert response is not None
	assert isinstance(response, Response)
	if expectedtype is not None:
		assert isinstance(response, expectedtype)


def validate_response_success(response, expectedtype=None):
	validate_response_object(response, expectedtype)

	if MerchantApiTestCredentials.VERBOSE_OUTPUT and response.is_error():
		print('%s: %s' % (response.get_error_code(), response.get_error_message()))

	assert response.is_success()


def validate_response_error(response, expectedtype=None):
	validate_response_object(response, expectedtype)
	assert response.is_error()


def read_test_file(file: str):
	filepath = MerchantApiTestCredentials.TEST_DATA_PATH + '/' + file
	fp = open(filepath, 'rb')
	ret = fp.read()
	fp.close()
	return ret


def upload_image(file: str):
	filepath = MerchantApiTestCredentials.TEST_DATA_PATH + '/' + file

	data = dict()
	data['Session_Type'] = 'admin'
	data['Function'] = 'Image_Upload'
	data['Username'] = MerchantApiTestCredentials.MERCHANT_ADMIN_USER
	data['Password'] = MerchantApiTestCredentials.MERCHANT_ADMIN_PASSWORD
	data['TemporarySession'] = 1
	data['Store_Code'] = MerchantApiTestCredentials.MERCHANT_API_STORE_CODE

	if filepath.endswith('.png'):
		type = 'image/png'
	elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
		type = 'image/jpeg'

	files = {'Image': (Path(filepath).name, open(filepath, 'rb'), type, {})}

	response = requests.post(url=MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, files=files, data=data)

	json = response.json()

	assert 'success' in json and json['success'] in (True, 1)


def enable_api_function_access(function_name: str, store_code: str = None):
	list_response = send_admin_request( 'APITokenList_Load_Query', {
		'Filter': [
			{
				'name':	'search',
				'value':
				[
					{
						'field':		'token',
						'operator':		'EQ',
						'value':		MerchantApiTestCredentials.MERCHANT_API_API_TOKEN
					}
				]
			}
		]
	}, True)

	list_result = list_response.json()

	assert list_result['success'] in (True, 1)
	assert list_result['data']['data'][0]['token'] == MerchantApiTestCredentials.MERCHANT_API_API_TOKEN

	if isinstance(store_code, str) and len(store_code):
		list_response = send_admin_request( 'StoreList_Load_Query', {
			'Filter': [
				{
					'name':	'search',
					'value':
					[
						{
							'field':		'code',
							'operator':		'EQ',
							'value':		MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
						}
					]
				}
			]
		}, False)
		
		assert list_response['success'] in (True, 1)
		assert list_response['data']['data'][0]['id'] > 0

		store_id = list_response['data']['data'][0]['id']
	else:
		store_id = 0

	response = send_admin_request( 'APITokenFunction_Insert', {
		'APIToken_ID': list_result['data']['data'][0]['id'],
		'APIToken_Store_ID': store_id,
		'APIToken_Function': function_name
	}, True)


def send_admin_request(func: str, data: dict, domain: bool = False):
	if not isinstance(data, dict):
		data = dict()

	data['Session_Type'] = 'admin'
	data['Function'] = func
	data['Username'] = MerchantApiTestCredentials.MERCHANT_ADMIN_USER
	data['Password'] = MerchantApiTestCredentials.MERCHANT_ADMIN_PASSWORD
	data['TemporarySession'] = 1

	if domain is not True and 'Store_Code' not in data:
		data['Store_Code'] = MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
	elif domain is True and 'Store_Code' in data:
		del data['Store_Code']

	return requests.post(url=MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, json=data)


def load_modules_by_feature(feature: str, include: list = None):
	response = send_admin_request('ModuleList_Load_Features', {'Module_Features': feature})

	data = response.json()

	if isinstance(include, list):
		ret = []
		for d in data['data']:
			if d['code'] in include:
				ret.append(d)
		return ret

	return data['data']


def get_product(code: str):
	request = merchantapi.request.ProductListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('code', code)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns()) \
		.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	return response.get_products()[0] if len(response.get_products()) else None


def get_products(codes: list):
	request = merchantapi.request.ProductListLoadQuery(init_client())

	filters = request.filter_expression() \
		.is_in('code', ','.join(codes))

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns()) \
		.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.ProductListLoadQuery)

	return response.get_products()


def get_category(code: str):
	request = merchantapi.request.CategoryListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('code', code)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns()) \
		.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.CategoryListLoadQuery)

	return response.get_categories()[0] if len(response.get_categories()) else None


def get_coupon(code: str):
	request = merchantapi.request.CouponListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.CouponListLoadQuery)

	return response.get_coupons()[0] if len(response.get_coupons()) else None


def get_customer(login: str):
	request = merchantapi.request.CustomerListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('login', login)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns())\
		.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.CustomerListLoadQuery)

	return response.get_customers()[0] if len(response.get_customers()) else None


def get_price_group(name: str):
	request = merchantapi.request.PriceGroupListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('name', name)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupListLoadQuery)

	return response.get_price_groups()[0] if len(response.get_price_groups()) else None


def get_branch(name: str):
	request = merchantapi.request.BranchListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('name', name)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.BranchListLoadQuery)

	return response.get_branches()[0] if len(response.get_branches()) else None


def delete_branch(name: str):
	request = merchantapi.request.BranchDelete(init_client())

	request.set_branch_name(name)

	response = request.send()

	validate_response_object(response, merchantapi.response.BranchDelete)


def get_note(field: str, value):
	request = merchantapi.request.NoteListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal(field, value)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.NoteListLoadQuery)

	return response.get_notes()[0] if len(response.get_notes()) else None


def get_order(id: int):
	request = merchantapi.request.OrderListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('id', id)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns())\
		.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.OrderListLoadQuery)

	return response.get_orders()[0] if len(response.get_orders()) else None


def provision_store(file: str):
	request = merchantapi.request.ProvisionStore(init_client())
	full_path = '%s/%s' % (MerchantApiTestCredentials.TEST_DATA_PATH, file)

	with open(full_path, 'r') as f:
		content = f.read()

	request.set_xml(content)

	response = request.send()

	validate_response_success(response, merchantapi.response.ProvisionStore)

	if MerchantApiTestCredentials.VERBOSE_OUTPUT:
		for message in response.get_provision_messages():
			print('[%s] Line %d Tag %s - %s' % (message.get_date_time_stamp(), message.get_line_number(), message.get_tag(), message.get_message()))


def provision_domain(file: str):
	request = merchantapi.request.ProvisionDomain(init_client())
	full_path = '%s/%s' % (MerchantApiTestCredentials.TEST_DATA_PATH, file)

	with open(full_path, 'r') as f:
		content = f.read()

	request.set_xml(content)

	response = request.send()

	validate_response_success(response, merchantapi.response.ProvisionDomain)

	if MerchantApiTestCredentials.VERBOSE_OUTPUT:
		for message in response.get_provision_messages():
			print('[%s] Line %d Tag %s - %s' % (message.get_date_time_stamp(), message.get_line_number(), message.get_tag(), message.get_message()))


def create_print_queue(name: str):
	response = send_admin_request('PrintQueue_Insert', {'PrintQueue_Description': name})
	data = response.json()
	assert 'success' in data


def create_branch(name: str, color: str, parent: merchantapi.model.Branch):
	assert parent is not None

	request = merchantapi.request.BranchCreate(init_client(), parent)

	request.set_name(name)
	request.set_color(color)

	response = request.send()

	validate_response_success(response, merchantapi.response.BranchCreate)

	return response.get_branch()


def get_branch_template_version(filename: str, branch: merchantapi.model.Branch):
	request = merchantapi.request.BranchTemplateVersionListLoadQuery(init_client(), branch)

	request.set_filters(request.filter_expression().equal('filename', filename))
	request.set_on_demand_columns(request.get_available_on_demand_columns())

	response = request.send()

	validate_response_success(response, merchantapi.response.BranchTemplateVersionListLoadQuery)

	return response.get_branch_template_versions()[0] if len(response.get_branch_template_versions()) > 0 else None


def get_product_attribute(product_code: str, attribute_code: str):
	request = merchantapi.request.AttributeLoadCode(init_client())
	request.set_product_code(product_code)
	request.set_attribute_code(attribute_code)

	response = request.send()

	return response.get_product_attribute() if response.is_success() else None


def get_product_options(product_code: str, attribute_code: str):
	request = merchantapi.request.OptionListLoadAttribute(init_client())
	request.set_product_code(product_code)
	request.set_attribute_code(attribute_code)

	response = request.send()

	validate_response_success(response, merchantapi.response.OptionListLoadAttribute)

	return response.get_product_options()


def get_product_attribute_and_options(product_code: str):
	request = merchantapi.request.AttributeAndOptionListLoadProduct(init_client())
	request.set_product_code(product_code)

	response = request.send()

	validate_response_success(response, merchantapi.response.AttributeAndOptionListLoadProduct)

	return response.get_product_attributes()


def get_business_account(title: str):
	request = merchantapi.request.BusinessAccountListLoadQuery(init_client())

	filters = request.filter_expression() \
		.equal('title', title)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.BusinessAccountListLoadQuery)

	return response.get_business_accounts()[0] if len(response.get_business_accounts()) else None


def get_store(code: str):
	request = merchantapi.request.StoreListLoadQuery(init_client())

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.StoreListLoadQuery)

	return response.get_stores()[0] if len(response.get_stores()) else None


def get_uri(path: str):
	request = merchantapi.request.URIListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())

	filters = request.filter_expression() \
		.equal('uri', path)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.URIListLoadQuery)

	return response.get_uris()[0] if len(response.get_uris()) else None


def get_page_uris(code: str):
	request = merchantapi.request.PageURIListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_page_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.PageURIListLoadQuery)

	return response.get_uris()


def get_feed_uris(code: str):
	request = merchantapi.request.FeedURIListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_feed_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.FeedURIListLoadQuery)

	return response.get_uris()


def get_category_uris(code: str):
	request = merchantapi.request.CategoryURIListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_category_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.CategoryURIListLoadQuery)

	return response.get_uris()


def get_product_uris(code: str):
	request = merchantapi.request.ProductURIListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_product_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.ProductURIListLoadQuery)

	return response.get_uris()


def get_attribute_template(code: str):
	request = merchantapi.request.AttributeTemplateListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.AttributeTemplateListLoadQuery)

	return response.get_attribute_templates()[0] if len(response.get_attribute_templates()) else None


def get_attribute_template_attribute(template_code: str, attribute_code: str):
	request = merchantapi.request.AttributeTemplateAttributeListLoadQuery(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_attribute_template_code(template_code)

	filters = request.filter_expression() \
		.equal('code', attribute_code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.AttributeTemplateAttributeListLoadQuery)

	return response.get_attribute_template_attributes()[0] if len(response.get_attribute_template_attributes()) else None


def get_attribute_template_options(template_code: str, attribute_code: str):
	request = merchantapi.request.AttributeTemplateOptionListLoadAttribute(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_attribute_template_code(template_code)
	request.set_attribute_template_attribute_code(attribute_code)

	response = request.send()

	validate_response_success(response, merchantapi.response.AttributeTemplateOptionListLoadAttribute)

	return response.get_attribute_template_options()


def get_attribute_template_option(template_code: str, attribute_code: str, option_code: str):
	request = merchantapi.request.AttributeTemplateOptionListLoadAttribute(init_client())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_attribute_template_code(template_code)
	request.set_attribute_template_attribute_code(attribute_code)

	response = request.send()

	validate_response_success(response, merchantapi.response.AttributeTemplateOptionListLoadAttribute)

	for opt in response.get_attribute_template_options():
		if opt.get_code() == option_code:
			return opt

	return None


def get_availability_group_categories(name: str, code: (str,None) = None, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.AvailabilityGroupCategoryListLoadQuery(init_client())
	request.set_availability_group_name(name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	if isinstance(code, str) and len(code):
		filters = request.filter_expression() \
			.equal('code', code)
		request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryListLoadQuery)

	return response.get_availability_group_categories()


def get_customer_business_account(title: str, customer: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.BusinessAccountCustomerListLoadQuery(init_client())
	request.set_business_account_title(title)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('login', customer)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.BusinessAccountCustomerListLoadQuery)

	return response.get_business_account_customers()


def get_coupon_customers(name: str, customer: (str,None) = None, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.CouponCustomerListLoadQuery(init_client())
	request.set_coupon_code(name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	if isinstance(customer, str) and len(customer):
		filters = request.filter_expression() \
			.equal('login', customer)
		request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.CouponCustomerListLoadQuery)

	return response.get_coupon_customers()


def get_customer_addresses(login: str):
	request = merchantapi.request.CustomerAddressListLoadQuery(init_client())
	request.set_customer_login(login)

	response = request.send()

	validate_response_success(response, merchantapi.response.CustomerAddressListLoadQuery)

	return response.get_customer_addresses()


def get_order_shipments(order_id: int):
	request = merchantapi.request.OrderShipmentListLoadQuery(init_client())

	filters = request.filter_expression() \
		.equal('order_id', order_id)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.OrderShipmentListLoadQuery)

	return response.get_order_shipments()


def get_price_group_business_accounts(pricegroup_name: str, title: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupBusinessAccountListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('title', title)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupBusinessAccountListLoadQuery)

	return response.get_price_group_business_accounts()


def get_price_group_categories(pricegroup_name: str, code: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupCategoryListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupCategoryListLoadQuery)

	return response.get_price_group_categories()


def get_price_group_excluded_categories(pricegroup_name: str, code: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupExcludedCategoryListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryListLoadQuery)

	return response.get_price_group_categories()


def get_price_group_products(pricegroup_name: str, code: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupProductListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryListLoadQuery)

	return response.get_price_group_products()


def get_price_group_excluded_products(pricegroup_name: str, code: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupExcludedProductListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupExcludedProductListLoadQuery)

	return response.get_price_group_products()


def get_price_group_qualifying_products(pricegroup_name: str, code: str, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.PriceGroupQualifyingProductListLoadQuery(init_client())
	request.set_price_group_name(pricegroup_name)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	filters = request.filter_expression() \
		.equal('code', code)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductListLoadQuery)

	return response.get_price_group_products()


def get_product_kit_variant_count(code: str):
	request = merchantapi.request.ProductKitVariantCount(init_client())
	request.set_product_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.ProductKitVariantCount)

	return response.get_variants()


def get_related_products(code: str, related_code: (str,None) = None, assigned: bool = True, unassigned: bool = False):
	request = merchantapi.request.RelatedProductListLoadQuery(init_client())
	request.set_product_code(code)
	request.set_assigned(assigned)
	request.set_unassigned(unassigned)

	if isinstance(related_code, str) and len(related_code):
		filters = request.filter_expression() \
			.equal('code', related_code)
		request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.RelatedProductListLoadQuery)

	return response.get_related_products()


def get_product_variants(code: str):
	request = merchantapi.request.ProductVariantListLoadProduct(init_client())
	request.set_product_code(code)

	response = request.send()

	validate_response_success(response, merchantapi.response.ProductVariantListLoadProduct)

	return response.get_product_variants()


def get_availability_group(name: str):
	request = merchantapi.request.AvailabilityGroupListLoadQuery(init_client())

	filters = request.filter_expression() \
		.equal('name', name)

	request.set_filters(filters)

	response = request.send()

	validate_response_success(response, merchantapi.response.AvailabilityGroupListLoadQuery)

	return response.get_availability_groups()[0] if len(response.get_availability_groups()) else None


def register_payment_card(customer: merchantapi.model.Customer, card_type : str = "Visa", card_no : str = "4111111111111111"):
	request = merchantapi.request.CustomerPaymentCardRegister(init_client())
	request.set_customer_login(customer.get_login())
	request.set_first_name(customer.get_bill_first_name())
	request.set_last_name(customer.get_bill_last_name())
	request.set_card_type(card_type)
	request.set_card_number(card_no)
	request.set_expiration_month(8)
	request.set_expiration_year(date.today().year + 2)
	request.set_address1(customer.get_bill_address1())
	request.set_address2(customer.get_bill_address2())
	request.set_city(customer.get_bill_city())
	request.set_state(customer.get_bill_state())
	request.set_zip(customer.get_bill_zip())
	request.set_country(customer.get_bill_country())

	response = request.send()

	validate_response_success(response, merchantapi.response.CustomerPaymentCardRegister)
	return response.get_customer_payment_card()


def register_payment_card_with_address(customer: merchantapi.model.Customer, address: merchantapi.model.CustomerAddress, card_type : str = "Visa", card_no : str = "4111111111111111"):
	request = merchantapi.request.CustomerPaymentCardRegister(init_client())
	request.set_customer_login(customer.get_login())
	request.set_first_name(address.get_first_name())
	request.set_last_name(address.get_last_name())
	request.set_card_type(card_type)
	request.set_card_number(card_no)
	request.set_expiration_month(8)
	request.set_expiration_year(date.today().year + 2)
	request.set_address1(address.get_address1())
	request.set_address2(address.get_address2())
	request.set_city(address.get_city())
	request.set_state(address.get_state())
	request.set_zip(address.get_zip())
	request.set_country(address.get_country())

	response = request.send()

	validate_response_success(response, merchantapi.response.CustomerPaymentCardRegister)
	return response.get_customer_payment_card()


def get_subscription(customer_id: int, subscription_id: int):
	request = merchantapi.request.CustomerSubscriptionListLoadQuery(init_client())
	request.set_customer_id(customer_id)
	request.filters.equal("id", subscription_id)

	response = request.send()

	validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)
	return response.get_customer_subscriptions()[0] if response.is_success() and response.get_total_count() > 0 else None


def create_subscription(customer: merchantapi.model.Customer, product: merchantapi.model.Product, sub_term_desc: str, next_date: int, address: merchantapi.model.CustomerAddress = None, card: merchantapi.model.CustomerPaymentCard = None, ship_id: int = 0, ship_data : str = "", quantity: int = 1, attributes : list = []):
	if card is None:
		if address is None:
			card = register_payment_card(customer)
		else:
			card = register_payment_card_with_address(customer, address)

	request = merchantapi.request.SubscriptionInsert(init_client())

	request.set_product_id(product.get_id())
	request.set_customer_id(customer.get_id())

	if address is not None:
		request.set_customer_address_id(address.get_id())

	request.set_payment_card_id(card.get_id())
	request.set_product_subscription_term_description(sub_term_desc)
	request.set_ship_id(ship_id)
	request.set_ship_data(ship_data)
	request.set_next_date(next_date)
	request.set_quantity(quantity)

	if isinstance(attributes, list) and len(attributes) > 0:
		request.add_attributes(attributes)

	response = request.send()

	validate_response_success(response, merchantapi.response.SubscriptionInsert)

	return response.get_subscription()


def get_subscription_shipping_methods(customer: merchantapi.model.Customer, product: merchantapi.model.Product, sub_term_desc: str, address: merchantapi.model.CustomerAddress = None, card: merchantapi.model.CustomerPaymentCard = None, quantity: int = 1, filter_op = merchantapi.listquery.FilterExpression.OPERATOR_EQ, filter_value = ""):
	if card is None:
		if address is None:
			card = register_payment_card(customer)
		else:
			card = register_payment_card_with_address(customer, address)

	request = merchantapi.request.SubscriptionShippingMethodListLoadQuery(init_client())

	request.set_product_id(product.get_id())
	request.set_customer_id(customer.get_id())

	if address is not None:
		request.set_customer_address_id(address.get_id())

	request.set_payment_card_id(card.get_id())
	request.set_product_subscription_term_description(sub_term_desc)
	request.set_quantity(quantity)

	if filter_value is not None and len(filter_value):
		request.filters.add("method", filter_op, filter_value, "search")

	response = request.send()

	validate_response_success(response, merchantapi.response.SubscriptionShippingMethodListLoadQuery)

	return response.get_subscription_shipping_methods()


def get_module(code: str):
	list_response = send_admin_request( 'ModuleList_Load_Query', {
		'Filter': [
			{
				'name':	'search',
				'value':
				[
					{
						'field':		'code',
						'operator':		'EQ',
						'value':		code
					}
				]
			}
		]
	})

	list_result = list_response.json()

	assert list_result['success'] in (True, 1)
	assert 'data'in list_result
	assert 'data' in list_result['data']
	return None if len(list_result['data']['data']) == 0 else list_result['data']['data'][0]


def get_page(code: str):
	request = merchantapi.request.PageListLoadQuery(init_client())

	request.get_filters().equal('code', code)
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.add_on_demand_column('CustomField_Values:*')

	response = request.send()

	validate_response_success(response, merchantapi.response.PageListLoadQuery)

	return response.get_pages()[0] if len(response.get_pages()) else None


def reset_branch_state():
	bllqrequest = merchantapi.request.BranchListLoadQuery(init_client())
	bllqresponse = bllqrequest.send()

	if len(bllqresponse.get_branches()) == 1:
		return

	bsprequest = merchantapi.request.BranchSetPrimary(init_client())
	bsprequest.set_branch_name('Production')
	bspresponse = bsprequest.send()

	for branch in bllqresponse.get_branches():
		if branch.get_id() == 1 or branch.get_name() == 'Production':
			continue

		request = merchantapi.request.BranchDelete(init_client(), branch)
		response = request.send()


def get_css_resource(code: str):
	request = merchantapi.request.CSSResourceListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('code', code)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns())

	response = request.send()

	validate_response_success(response, merchantapi.response.CSSResourceListLoadQuery)

	return response.get_css_resources()[0] if len(response.get_css_resources()) else None


def get_javascript_resource(code: str):
	request = merchantapi.request.JavaScriptResourceListLoadQuery(init_client())

	filters = request.filter_expression()\
		.equal('code', code)

	request.set_filters(filters) \
		.set_on_demand_columns(request.get_available_on_demand_columns())

	response = request.send()

	validate_response_success(response, merchantapi.response.JavaScriptResourceListLoadQuery)

	return response.get_javascript_resources()[0] if len(response.get_javascript_resources()) else None


def get_price_group_exclusion(priceGroup: str, excudedPriceGroup: str):
	response = send_admin_request( 'PriceGroupList_Load_Exclusions', {
		'PriceGroup_Name': priceGroup
	})

	result = response.json()

	assert result['success'] in (True, 1)
	assert 'data'in result
	for pg in result['data']:
		if pg['name'] == excudedPriceGroup:
			return pg
	return None


def get_copy_product_rule(name: str):
	request = merchantapi.request.CopyProductRulesListLoadQuery(init_client())
	request.get_filters().equal('name', name)
	response = request.send()

	validate_response_success(response, merchantapi.response.CopyProductRulesListLoadQuery)

	return response.get_copy_product_rules()[0] if len(response.get_copy_product_rules()) else None


def get_copy_page_rule(name: str):
	request = merchantapi.request.CopyPageRulesListLoadQuery(init_client())
	request.get_filters().equal('name', name)

	response = request.send()

	validate_response_success(response, merchantapi.response.CopyPageRulesListLoadQuery)

	return response.get_copy_page_rules()[0] if len(response.get_copy_page_rules()) else None
