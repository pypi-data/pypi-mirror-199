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


def test_module():
	"""
	Tests the Module API Call
	"""

	module_test_invalid_module()


def module_test_invalid_module():
	request = merchantapi.request.Module(helper.init_client())

	request.set_module_code('InvalidModule')\
		.set_module_function('InvalidModuleFunction')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.Module)
