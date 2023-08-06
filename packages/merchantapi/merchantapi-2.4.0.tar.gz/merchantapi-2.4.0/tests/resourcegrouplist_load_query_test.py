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


def test_resource_group_list_load_query():
	"""
	Tests the ResourceGroupList_Load_Query  API Call
	"""

	resource_group_list_load_query_test_list_load()


def resource_group_list_load_query_test_list_load():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(create_response.get_branch().get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ResourceGroupListLoadQuery(helper.init_client(), create_response.get_branch())
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ResourceGroupListLoadQuery)

