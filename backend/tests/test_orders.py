from httpx import AsyncClient


# ── Helpers ───────────────────────────────────────────────────────────────────


async def _make_customer(client: AsyncClient, headers: dict, email: str) -> str:
    resp = await client.post(
        "/api/v1/customers/",
        json={"name": "Customer", "email": email},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _make_product(
    client: AsyncClient, headers: dict, name: str, price: str
) -> str:
    resp = await client.post(
        "/api/v1/products/",
        json={"name": name, "price": price},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_order(
    client: AsyncClient, headers: dict, customer_id: str
) -> dict:
    resp = await client.post(
        "/api/v1/orders/",
        json={"customer_id": customer_id},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


async def _add_item(
    client: AsyncClient, headers: dict, order_id: str, product_id: str
):
    return await client.post(
        f"/api/v1/orders/{order_id}/items",
        json={"product_id": product_id},
        headers=headers,
    )


# ── Create ────────────────────────────────────────────────────────────────────


async def test_create_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer1@example.com")
    resp = await client.post(
        "/api/v1/orders/",
        json={"customer_id": cid},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "draft"
    assert data["items"] == []
    assert float(data["total_amount"]) == 0.0
    assert data["customer"]["id"] == cid


async def test_create_order_invalid_customer(client: AsyncClient, auth_headers: dict):
    resp = await client.post(
        "/api/v1/orders/",
        json={"customer_id": "00000000-0000-0000-0000-000000000000"},
        headers=auth_headers,
    )
    assert resp.status_code == 404


# ── Add items ─────────────────────────────────────────────────────────────────


async def test_add_item(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer2@example.com")
    pid = await _make_product(client, auth_headers, "Widget", "9.99")
    order = await _create_order(client, auth_headers, cid)

    resp = await _add_item(client, auth_headers, order["id"], pid)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert float(data["total_amount"]) == 9.99


async def test_add_item_missing_product(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer3@example.com")
    order = await _create_order(client, auth_headers, cid)
    resp = await _add_item(
        client, auth_headers, order["id"], "00000000-0000-0000-0000-000000000000"
    )
    assert resp.status_code == 404


async def test_add_duplicate_item(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer4@example.com")
    pid = await _make_product(client, auth_headers, "Gadget", "5.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid)
    resp = await _add_item(client, auth_headers, order["id"], pid)
    assert resp.status_code == 409


async def test_add_item_to_confirmed_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer5@example.com")
    pid1 = await _make_product(client, auth_headers, "A", "1.00")
    pid2 = await _make_product(client, auth_headers, "B", "2.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid1)
    await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    resp = await _add_item(client, auth_headers, order["id"], pid2)
    assert resp.status_code == 409


# ── Remove items ──────────────────────────────────────────────────────────────


async def test_remove_item(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer6@example.com")
    pid = await _make_product(client, auth_headers, "Thing", "3.00")
    order = await _create_order(client, auth_headers, cid)
    updated = (await _add_item(client, auth_headers, order["id"], pid)).json()
    item_id = updated["items"][0]["id"]

    resp = await client.delete(
        f"/api/v1/orders/{order['id']}/items/{item_id}",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["items"] == []
    assert float(resp.json()["total_amount"]) == 0.0


# ── Status transitions ────────────────────────────────────────────────────────


async def test_confirm_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer7@example.com")
    pid = await _make_product(client, auth_headers, "Item", "20.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid)

    resp = await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"


async def test_confirm_empty_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer8@example.com")
    order = await _create_order(client, auth_headers, cid)
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    assert resp.status_code == 422


async def test_mark_paid(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer9@example.com")
    pid = await _make_product(client, auth_headers, "Item", "15.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid)
    await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/pay", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "paid"


async def test_mark_paid_non_pending(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer10@example.com")
    order = await _create_order(client, auth_headers, cid)
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/pay", headers=auth_headers
    )
    assert resp.status_code == 409


async def test_cancel_draft_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer11@example.com")
    order = await _create_order(client, auth_headers, cid)
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/cancel", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


async def test_cancel_pending_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer12@example.com")
    pid = await _make_product(client, auth_headers, "Item", "5.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid)
    await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/cancel", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


async def test_cancel_paid_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer13@example.com")
    pid = await _make_product(client, auth_headers, "Item", "5.00")
    order = await _create_order(client, auth_headers, cid)
    await _add_item(client, auth_headers, order["id"], pid)
    await client.post(
        f"/api/v1/orders/{order['id']}/confirm", headers=auth_headers
    )
    await client.post(f"/api/v1/orders/{order['id']}/pay", headers=auth_headers)
    resp = await client.post(
        f"/api/v1/orders/{order['id']}/cancel", headers=auth_headers
    )
    assert resp.status_code == 409


# ── List / Get / Delete ───────────────────────────────────────────────────────


async def test_list_orders(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/api/v1/orders/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_list_orders_by_customer(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer14@example.com")
    order = await _create_order(client, auth_headers, cid)
    pid = await _make_product(client, auth_headers, "Item", "4.00")
    await _add_item(client, auth_headers, order["id"], pid)

    resp = await client.get(
        f"/api/v1/orders/customer/{cid}", headers=auth_headers
    )
    assert resp.status_code == 200
    assert all(o["customer"]["id"] == cid for o in resp.json())


async def test_get_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer15@example.com")
    order = await _create_order(client, auth_headers, cid)

    resp = await client.get(f"/api/v1/orders/{order['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == order["id"]


async def test_get_order_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get(
        "/api/v1/orders/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


async def test_delete_order(client: AsyncClient, auth_headers: dict):
    cid = await _make_customer(client, auth_headers, "buyer16@example.com")
    order = await _create_order(client, auth_headers, cid)
    resp = await client.delete(
        f"/api/v1/orders/{order['id']}", headers=auth_headers
    )
    assert resp.status_code == 204
