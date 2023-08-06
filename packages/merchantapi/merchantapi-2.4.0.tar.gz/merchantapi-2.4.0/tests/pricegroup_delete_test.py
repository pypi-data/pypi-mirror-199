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


def test_price_group_delete():
	"""
	Tests the PriceGroup_Delete API Call
	"""

	helper.provision_store('PriceGroup_Delete.xml')

	price_group_delete_test_deletion()


def price_group_delete_test_deletion():
	pricegroup = helper.get_price_group('PriceGroupDeleteTest_1')

	assert pricegroup is not None

	request = merchantapi.request.PriceGroupDelete(helper.init_client(), pricegroup)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupDelete)

	check = helper.get_price_group(pricegroup.get_name())

	assert check is None
