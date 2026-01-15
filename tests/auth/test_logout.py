def test_logout_blacklists_token(client, fake_redis, valid_access_token):
    response = client.post(
        "/api/v1/auth/logout",
        headers={
            "Authorization": f"Bearer {valid_access_token}"
        }
    )

    assert response.status_code == 204
    assert fake_redis.exists(f"blacklist:{valid_access_token}")
