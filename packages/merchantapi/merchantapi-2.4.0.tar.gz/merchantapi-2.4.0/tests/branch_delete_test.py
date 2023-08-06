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


def test_branch_delete():
	"""
	Tests the Branch_Delete API Call
	"""

	branch_delete_test_deletion()


def branch_delete_test_deletion():
	branch = helper.get_branch('Production Copy')

	if branch is None:
		copybranch = helper.get_branch('Production')
		assert isinstance(copybranch, merchantapi.model.Branch)
		copyrequest = merchantapi.request.BranchCreate(helper.init_client(), copybranch)
		copyrequest.set_name('Production Copy')
		copyrequest.set_color('#000000')

		copyresponse = copyrequest.send()
		helper.validate_response_success(copyresponse, merchantapi.response.BranchCreate)

		branch = copyresponse.get_branch()

	request = merchantapi.request.BranchDelete(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchDelete)
