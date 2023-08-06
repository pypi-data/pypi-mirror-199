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


def test_branch_list_load_query():
	"""
	Tests the BranchList_Load_Query API Call
	"""

	branch_list_load_query_test_list_load()


def branch_list_load_query_test_list_load():
	request = merchantapi.request.BranchListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchListLoadQuery)

	assert len(response.get_branches()) > 0

	for e in response.get_branches():
		assert isinstance(e, merchantapi.model.Branch)
