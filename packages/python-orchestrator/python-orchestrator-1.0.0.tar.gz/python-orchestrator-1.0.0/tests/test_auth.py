def test_auth(cloud_auth, on_premise_auth):
    assert cloud_auth.base_url.startswith("https://cloud.uipath.com")
    assert cloud_auth.token_url.startswith("https://account.uipath.com")
    assert cloud_auth._token_endpoint == "/oauth/token"
    assert cloud_auth.expires
    assert not cloud_auth.authenticated
    assert not cloud_auth._access_token
    assert on_premise_auth.auth_endpoint == "/api/Account/Authenticate"
    assert on_premise_auth.expires
    assert not on_premise_auth.authenticated
    assert not on_premise_auth._access_token


def test_cloud_auth_token(cloud_auth, on_premise_auth):
    expiracy = cloud_auth.expires
    assert not cloud_auth.authenticated
    cloud_auth.auth()
    assert cloud_auth.authenticated
    assert cloud_auth.expires > expiracy
    assert cloud_auth._access_token
    assert not cloud_auth.token_expires()
    expiracy = on_premise_auth.expires
    assert not on_premise_auth.authenticated
    on_premise_auth.auth()
    assert on_premise_auth.authenticated
    assert on_premise_auth.expires > expiracy
    assert on_premise_auth._access_token
    assert not on_premise_auth.token_expires()
