def test_me_with_revoked_token(client, fake_redis, valid_access_token):
    # simula logout
    fake_redis.setex(
        name=f"blacklist:{valid_access_token}",
        time=3600,
        value="true"
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {valid_access_token}"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token revogado"
