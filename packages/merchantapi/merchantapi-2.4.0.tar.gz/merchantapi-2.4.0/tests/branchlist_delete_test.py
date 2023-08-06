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


def test_branch_list_delete():
	"""
	Tests the BranchList_Delete API Call
	"""

	branch_list_delete_test()


def branch_list_delete_test():
	helper.delete_branch('Production Copy')
	helper.delete_branch('Production Copy 1')
	helper.delete_branch('Production Copy 2')

	production_branch = helper.get_branch('Production')

	branch1 = helper.create_branch('Production Copy', '#000000', production_branch)
	branch2 = helper.create_branch('Production Copy 1', '#000000', production_branch)
	branch3 = helper.create_branch('Production Copy 2', '#000000', production_branch)

	request = merchantapi.request.BranchListDelete(helper.init_client())

	request.add_branch(branch1)
	request.add_branch(branch2)
	request.add_branch(branch3)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchListDelete)

	assert response.get_processed() == 3
