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


def test_branch_update():
	"""
	Tests the Branch_Update API Call
	"""

	branch_update_test_update()


def branch_update_test_update():
	helper.delete_branch('Production Copy')

	base_branch = helper.get_branch('Production')

	branch = helper.create_branch('Production Copy', '#000000', base_branch)

	assert branch is not None

	request = merchantapi.request.BranchUpdate(helper.init_client(), branch)

	request.set_branch_color('#f1f1f1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchUpdate)

	check_branch = helper.get_branch('Production Copy')

	assert check_branch is not None
	assert check_branch.get_color() == '#f1f1f1'
