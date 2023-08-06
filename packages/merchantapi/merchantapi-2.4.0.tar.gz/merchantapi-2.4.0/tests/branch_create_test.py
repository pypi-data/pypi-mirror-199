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


def test_branch_create():
	"""
	Tests the Branch_Create API Call
	"""

	branch_create_test_create()


def branch_create_test_create():
	helper.delete_branch('Production Copy')

	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.BranchCreate(helper.init_client(), branch)

	request.set_name('Production Copy')
	request.set_color('#000000')

	assert branch.get_id() == request.get_parent_branch_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchCreate)

	assert isinstance(response.get_branch(), merchantapi.model.Branch)
