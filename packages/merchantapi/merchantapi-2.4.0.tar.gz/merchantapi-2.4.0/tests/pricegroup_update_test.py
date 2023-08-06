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


def test_price_group_update():
	"""
	Tests the PriceGroup_Update API Call
	"""

	helper.provision_store('PriceGroup_Update.xml')

	price_group_update_test_update()


def price_group_update_test_update():
	pricegroup = helper.get_price_group('PriceGroupUpdateTest_1')

	assert pricegroup is not None

	excluded_price_group = helper.get_price_group('PriceGroupUpdateTest_Exclusion')

	assert excluded_price_group is not None

	request = merchantapi.request.PriceGroupUpdate(helper.init_client(), pricegroup)

	request.set_name('PriceGroupUpdateTest_1_Modified')
	request.set_description('PriceGroupUpdateTest_1_Modified')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupUpdate)

	checkA = helper.get_price_group('PriceGroupUpdateTest_1')
	checkB = helper.get_price_group('PriceGroupUpdateTest_1_Modified')

	assert checkA is None
	assert checkB is not None
	assert checkB.get_description() == 'PriceGroupUpdateTest_1_Modified'

	exclusion_check = helper.get_price_group_exclusion(checkB.get_name(), excluded_price_group.get_name())
	assert exclusion_check is not None
