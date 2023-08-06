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


def test_changeset_change_list_load_query():
	"""
	Tests the ChangesetChangeList_Load_Query API Call
	"""

	changeset_change_list_load_query_test_list_load()


def changeset_change_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create 3 Changes in one changeset

	create_changeset_request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	template1 = helper.get_branch_template_version('sfnt.mvc', branch)
	template2 = helper.get_branch_template_version('prod.mvc', branch)
	template3 = helper.get_branch_template_version('ctgy.mvc', branch)

	change1 = merchantapi.model.TemplateChange()
	change2 = merchantapi.model.TemplateChange()
	change3 = merchantapi.model.TemplateChange()

	change1.set_template_filename('sfnt.mvc').set_source(template1.get_source().replace('<body class="SFNT">', '<body class="SFNT">HELLO_WORLD'))
	change2.set_template_filename('prod.mvc').set_source(template2.get_source().replace('<body class="PROD">', '<body class="PROD">HELLO_WORLD'))
	change3.set_template_filename('ctgy.mvc').set_source(template3.get_source().replace('<body class="CTGY">', '<body class="CTGY">HELLO_WORLD'))

	create_changeset_request.add_template_change(change1)
	create_changeset_request.add_template_change(change2)
	create_changeset_request.add_template_change(change3)

	create_changeset_response = create_changeset_request.send()

	helper.validate_response_success(create_changeset_response, merchantapi.response.ChangesetCreate)

	changeset = create_changeset_response.get_changeset()

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetChangeListLoadQuery(helper.init_client(), changeset)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetChangeListLoadQuery)

	assert len(response.get_changeset_changes()) == 3

	for change in response.get_changeset_changes():
		assert isinstance(change, merchantapi.model.ChangesetChange)
