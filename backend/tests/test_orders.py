from httpx import AsyncClient


async def _make_customer(client: AsyncClient, headers: dict, email: str) -> str:
    resp = await client.post(
        "/api/v1/customers/",
        json={"name": "Customer", "email": email},
        headers=headers,
    )
    return resp.json()["id"]


async def _make_product(
    client: AsyncClient, headers: dict, name: str, price: str
) -> str:
    resp = await client.post(
        "/api/v1/products/",
        json={"name": name, "price": price},
        headers=headers,
    )
    return resp.json()["id"]


async def test_create_order_valid(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer1@example.com")
    pid1 = await _make_product(client, auth_headers, "Item A", "10.00")
    pid2 = await _make_product(client, auth_headers, "Item B", "5.50")

    resp = await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid, "product_ids": [pid1, pid2]},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert float(data["total_amount"]) == 15.50
    assert len(data["items"]) == 2
    assert data["customer"]["id"] == cid


async def test_create_order_missing_customer(client: AsyncClient, auth_headers: dict):
    pid = await _make_product(client, auth_headers, "Item C", "1.00")
    resp = await client.post(
        "/api/v1/orders/",
        json={
            "customer_id": "00000000-0000-0000-0000-000000000000",
            "product_ids": [pid],
        },
        headers=auth_headers,
    )
    assert resp.status_code == 404


async def test_create_order_empty_products(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer2@example.com")
    resp = await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid, "product_ids": []},
        headers=auth_headers,
    )
    assert resp.status_code == 422


async def test_create_order_missing_product(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer3@example.com")
    resp = await client.post(
        "/api/v1/orders/",
        json={
            "customer_id": cid,
            "product_ids": ["00000000-0000-0000-0000-000000000000"],
        },
        headers=auth_headers,
    )
    assert resp.status_code == 404


async def test_list_orders(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/api/v1/orders/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_list_orders_by_customer(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer4@example.com")
    pid = await _make_product(client, auth_headers, "Item D", "7.00")
    await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid, "product_ids": [pid]},
        headers=auth_headers,
    )
    resp = await client.get(f"/api/v1/orders/customer/{cid}", headers=auth_headers)
    assert resp.status_code == 200
    assert all(o["customer"]["id"] == cid for o in resp.json())


async def test_get_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer5@example.com")
    pid = await _make_product(client, auth_headers, "Item E", "3.00")
    create = await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid, "product_ids": [pid]},
        headers=auth_headers,
    )
    oid = create.json()["id"]
    resp = await client.get(f"/api/v1/orders/{oid}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == oid


async def test_delete_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer6@example.com")
    pid = await _make_product(client, auth_headers, "Item F", "2.00")
    create = await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid, "product_ids": [pid]},
        headers=auth_headers,
    )
    oid = create.json()["id"]
    resp = await client.delete(f"/api/v1/orders/{oid}", headers=auth_headers)
    assert resp.status_code == 204
