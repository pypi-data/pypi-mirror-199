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


def test_image_type_list_load_query():
	"""
	Tests the ImageTypeList_Load_Query API Call
	"""

	helper.provision_store('ImageTypeList_Load_Query.xml')

	image_type_list_load_query_test_list_load()


def image_type_list_load_query_test_list_load():
	request = merchantapi.request.ImageTypeListLoadQuery(helper.init_client())
	request.set_filters(request.filter_expression().like('code', 'ImageTypeListLoadQueryTest%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ImageTypeListLoadQuery)

	assert len(response.get_image_types()) == 5
