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


def test_changeset_create():
	"""
	Tests the Changeset_Create API Call
	"""

	changeset_create_test_creation()


def changeset_create_test_creation():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	assert request.get_branch_id() == branch.get_id()

	# Load a Changeset
	load_changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	load_changeset_response = load_changeset_request.send()

	helper.validate_response_success(load_changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert isinstance(load_changeset_response.get_changesets(), list)
	assert len(load_changeset_response.get_changesets()) > 0

	changeset = load_changeset_response.get_changesets()[0]

	assert isinstance(changeset, merchantapi.model.Changeset)

	# Load a Template
	load_template_request = merchantapi.request.BranchTemplateVersionListLoadQuery(helper.init_client(), branch)

	load_template_request.set_filters(load_template_request.filter_expression().equal('filename', 'sfnt.mvc'))
	load_template_request.set_on_demand_columns(load_template_request.get_available_on_demand_columns())
	load_template_request.set_changeset_id(changeset.get_id())

	load_template_response = load_template_request.send()

	helper.validate_response_success(load_template_response, merchantapi.response.BranchTemplateVersionListLoadQuery)

	assert isinstance(load_template_response.get_branch_template_versions(), list)
	assert len(load_template_response.get_branch_template_versions()) > 0

	version = load_template_response.get_branch_template_versions()[0]

	assert isinstance(version, merchantapi.model.BranchTemplateVersion)

	# Add a Change
	change1 = merchantapi.model.TemplateChange()

	source = version.get_source()

	assert isinstance(source, str)
	assert len(source) > 0

	if '<body class="SFNT">HELLO_WORLD' in source:
		change1.set_template_filename('sfnt.mvc').set_source(source.replace('<body class="SFNT">HELLO_WORLD', '<body class="SFNT">'))
	else:
		change1.set_template_filename('sfnt.mvc').set_source(source.replace('<body class="SFNT">', '<body class="SFNT">HELLO_WORLD'))

	request.add_template_change(change1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCreate)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)
