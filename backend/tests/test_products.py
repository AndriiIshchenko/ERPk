from httpx import AsyncClient


async def test_create_product(client: AsyncClient, auth_headers: dict):
    resp = await client.post(
        "/api/v1/products/",
        json={"name": "Widget", "price": "10.00"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Widget"


async def test_list_products(client: AsyncClient, auth_headers: dict):
    await client.post(
        "/api/v1/products/",
        json={"name": "Gadget", "price": "5.00"},
        headers=auth_headers,
    )
    resp = await client.get("/api/v1/products/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_get_product(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/products/",
        json={"name": "Thing", "price": "3.50"},
        headers=auth_headers,
    )
    pid = create.json()["id"]
    resp = await client.get(f"/api/v1/products/{pid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == pid


async def test_get_product_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


async def test_update_product(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/products/",
        json={"name": "OldName", "price": "1.00"},
        headers=auth_headers,
    )
    pid = create.json()["id"]
    resp = await client.put(
        f"/api/v1/products/{pid}",
        json={"name": "NewName", "price": "2.00"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "NewName"


async def test_delete_product(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/api/v1/products/",
        json={"name": "ToDelete", "price": "1.00"},
        headers=auth_headers,
    )
    pid = create.json()["id"]
    resp = await client.delete(f"/api/v1/products/{pid}", headers=auth_headers)
    assert resp.status_code == 204
