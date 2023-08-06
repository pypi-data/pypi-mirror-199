"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import pytest
import os
from merchantapi.client import Client, SSHClient, SSHAgentClient, ClientException
from merchantapi.authenticator import TokenAuthenticator, SSHAgentAuthenticator, SSHPrivateKeyAuthenticator, SSHPrivateKeyPasswordError
from merchantapi.request import ProductListLoadQuery
from merchantapi.response import ProductListLoadQuery as ProductListLoadQueryResponse
from . import helper
from . credentials import MerchantApiTestCredentials

helper.configure_logging()


def test_client_defaults():
    client = Client('https://localhost/mm5/json.mvc', 'MYTOKEN', 'MYSIGNINGKEY')

    assert isinstance(client.get_authenticator(), TokenAuthenticator)
    assert client.get_endpoint() == 'https://localhost/mm5/json.mvc'
    assert client.get_authenticator().get_api_token() == 'MYTOKEN'
    assert client.get_authenticator().get_signing_key() == 'MYSIGNINGKEY'
    assert client.get_option('default_store_code') is None
    assert client.get_option('require_timestamps') is True
    assert client.get_option('ssl_verify') == True
    assert client.get_option('operation_timeout') == 60


def test_client_constructor_options():
    client = Client('https://localhost/mm5/json.mvc', 'MYTOKEN', 'MYSIGNINGKEY', {
        'default_store_code': 'foo',
        'require_timestamps': False,
        'ssl_verify': False,
        'operation_timeout': 20,
        'signing_key_digest': Client.SIGN_DIGEST_SHA256
    })

    assert client.get_option('default_store_code') == 'foo'
    assert client.get_option('require_timestamps') is False
    assert client.get_option('ssl_verify') == False
    assert client.get_option('operation_timeout') == 20


def test_client_signing_key_padding():
    client = Client('https://localhost/mm5/json.mvc', 'MYTOKEN', 'AA')
    assert client.get_authenticator().get_signing_key() == 'AA=='
    client.get_authenticator().set_signing_key('AAA')
    assert client.get_authenticator().get_signing_key() == 'AAA='


def test_client_exception_connectionerror():
    client = Client('http://i-do-not-exist', 'MYTOKEN', 'MYSIGNINGKEY')

    request = ProductListLoadQuery(client)

    with pytest.raises(ClientException):
        request.send()


def test_no_request_signing():
    client = Client('https://www.mystore.com/mm5/json.mvc', 'MyAPIToken', '')
    client.set_option('signing_key_digest', Client.SIGN_DIGEST_NONE)

    assert client.generate_auth_header('{foo:\'bar\'}') == 'MIVA MyAPIToken'


def test_client_ssh_authentication_sha256_openssh_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', 'test', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.openssh.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_authentication_sha512_openssh_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', 'test', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.openssh.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_authentication_sha256_pcks1_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', 'test123', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.pkcs1.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_authentication_sha512_pcks1_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', 'test123', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.pkcs1.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)



def test_client_ssh_authentication_sha256_pcks8_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs8.pem', 'test123', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.pkcs8.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)



def test_client_ssh_authentication_sha512_pcks8_pem():
    helper.provision_domain('ssh/Assign_Administrator_id_rsa_pw_test.xml')

    # Test Encrypted

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs8.pem', 'test123', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    # Test Unencrypted

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_no_password.pkcs8.pem', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_agent_sign_from_public_key_file():
    assert os.environ.get('SSH_AUTH_SOCK') is not None

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHAgentClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/public_key_no_password.openssh.pem', SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA256, None, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_agent_sign_from_public_key_file_512():
    assert os.environ.get('SSH_AUTH_SOCK') is not None

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')

    client = SSHAgentClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/public_key_no_password.openssh.pem', SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA512, None, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_agent_sign_from_public_key_string():
    assert os.environ.get('SSH_AUTH_SOCK') is not None

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')
    key = helper.read_test_file('ssh/public_key_no_password.openssh.pem')
    
    client = SSHAgentClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', '', SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA256, None, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    client.set_public_key_string(key)

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_agent_sign_from_public_key_string_512():
    assert os.environ.get('SSH_AUTH_SOCK') is not None

    helper.provision_domain('ssh/Assign_Administrator_id_rsa_no_pw.xml')
    key = helper.read_test_file('ssh/public_key_no_password.openssh.pem')

    client = SSHAgentClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', '', SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA512, None, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    client.set_public_key_string(key)

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)


def test_client_ssh_password_exception():
    # Test when thrown from constructor with an invalid password
    with pytest.raises(SSHPrivateKeyPasswordError):
        client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', 'INVALID PASSWORD', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
            'ssl_verify': False,
            'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
        })

    # Test when thrown from constructor with no password
    with pytest.raises(SSHPrivateKeyPasswordError):
        client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', None, SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
            'ssl_verify': False,
            'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
        })

    # Test when thrown from constructor with an invalid password with en encrypted pkcs#1 key file
    with pytest.raises(SSHPrivateKeyPasswordError):
        client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', 'INVALID PASSWORD', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
            'ssl_verify': False,
            'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
        })
    
    # Test when thrown from constructor with no password pkcs#1
    with pytest.raises(SSHPrivateKeyPasswordError):
        client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', None, SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
            'ssl_verify': False,
            'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
        })

    client = SSHClient(MerchantApiTestCredentials.MERCHANT_API_ENDPOINT, 'Administrator', '', '', SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, {
        'ssl_verify': False,
        'default_store_code': MerchantApiTestCredentials.MERCHANT_API_STORE_CODE
    })

    # Test when assigned after client construction with an invalid password
    with pytest.raises(SSHPrivateKeyPasswordError):
        client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', 'INVALID PASSWORD')

        # Test when assigned after client construction with  no password
    with pytest.raises(SSHPrivateKeyPasswordError):
        client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', None)
   
   # Test when assigned after client construction with an invalid password pkcs1
    with pytest.raises(SSHPrivateKeyPasswordError):
        client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', 'INVALID PASSWORD')

    # Test when assigned after client construction with  no password pkcs1
    with pytest.raises(SSHPrivateKeyPasswordError):
        client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', None)

    # Should not throw an exception
    client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test.openssh.pem', 'test')

    # Should not throw an exception
    client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs1.pem', 'test123')

    # Should not throw an exception
    client.set_private_key(MerchantApiTestCredentials.TEST_DATA_PATH + '/ssh/private_key_password_test123.pkcs8.pem', 'test123')


def test_client_global_headers():
    client = helper.init_client()

    client.set_global_header('Foo', 'Bar')
    client.set_global_header('Bin', 'Baz')
    client.set_global_header('Bar', 'Foo')

    assert client.has_global_header('Foo')
    assert client.has_global_header('Bin')
    assert client.has_global_header('Bar')

    assert client.get_global_header('Foo') == 'Bar'
    assert client.get_global_header('Bin') == 'Baz'
    assert client.get_global_header('Bar') == 'Foo'

    client.remove_global_header('Bar')

    assert client.has_global_header('Bar') is False

    request = ProductListLoadQuery(client)

    response = request.send()

    helper.validate_response_success(response, ProductListLoadQueryResponse)

    assert 'Foo' in response.get_http_response().request.headers
    assert 'Bin' in response.get_http_response().request.headers
    assert response.get_http_response().request.headers['Foo'] == 'Bar'
    assert response.get_http_response().request.headers['Bin'] == 'Baz'
