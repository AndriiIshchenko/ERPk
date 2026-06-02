from httpx import AsyncClient


async def test_create_customer(client: AsyncClient, auth_headers: dict):
    resp = await client.post(
        "/api/v1/customers/",
        json={"name": "Alice", "email": "alice@example.com"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Alice"


async def test_list_customers(client: AsyncClient, auth_headers: dict):
    await client.post(
        "/api/v1/customers/",
        json={"name": "Bob", "email": "bob@example.com"},
        headers=auth_headers,
    )
    resp = await client.get("/api/v1/customers/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_get_customer(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/customers/",
        json={"name": "Carol", "email": "carol@example.com"},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    resp = await client.get(f"/api/v1/customers/{cid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == cid


async def test_get_customer_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get(
        "/api/v1/customers/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


async def test_update_customer(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/customers/",
        json={"name": "Dave", "email": "dave@example.com"},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    resp = await client.put(
        f"/api/v1/customers/{cid}",
        json={"name": "David"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "David"


async def test_delete_customer(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/customers/",
        json={"name": "Eve", "email": "eve@example.com"},
        headers=auth_headers,
    )
    cid = create.json()["id"]
    resp = await client.delete(f"/api/v1/customers/{cid}", headers=auth_headers)
    assert resp.status_code == 204
