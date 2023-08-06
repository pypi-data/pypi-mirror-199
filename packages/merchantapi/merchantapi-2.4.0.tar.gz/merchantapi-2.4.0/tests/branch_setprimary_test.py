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


def test_branch_set_primary():
	"""
	Tests the Branch_SetPrimary API Call
	"""

	branch_set_primary_test_set_primary()


def branch_set_primary_test_set_primary():
	helper.delete_branch('Production Copy')

	base_branch = helper.get_branch('Production')

	branch = helper.create_branch('Production Copy', '#000000', base_branch)

	assert branch is not None

	request = merchantapi.request.BranchSetPrimary(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchSetPrimary)

	# Reset back to default primary or other tests might fail
	request.set_branch_id(base_branch.get_id())
	request.send()
