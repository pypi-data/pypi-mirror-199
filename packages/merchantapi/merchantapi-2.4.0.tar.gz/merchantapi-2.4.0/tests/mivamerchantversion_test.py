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


def test_miva_merchant_version():
	"""
	Tests the MivaMerchantVersion API Call
	"""

	request = merchantapi.request.MivaMerchantVersion(helper.init_client())
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.MivaMerchantVersion)

	assert isinstance(response.get_merchant_version(), merchantapi.model.MerchantVersion)

	assert isinstance(response.get_merchant_version().get_version(), str) and len(response.get_merchant_version().get_version())
	assert isinstance(response.get_merchant_version().get_major(), int) and response.get_merchant_version().get_major() >= 10
	assert isinstance(response.get_merchant_version().get_minor(), int) and response.get_merchant_version().get_minor() >= 0
	assert isinstance(response.get_merchant_version().get_bugfix(), int) and response.get_merchant_version().get_bugfix() >= 0
