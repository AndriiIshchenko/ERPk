from httpx import AsyncClient


# ── Helper ────────────────────────────────────────────────────────────────────


async def _create_product(
    client: AsyncClient, headers: dict, name: str, price: str
) -> dict:
    resp = await client.post(
        "/api/v1/products/",
        json={"name": name, "price": price},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


# ── Create ────────────────────────────────────────────────────────────────────


async def test_create_product(client: AsyncClient, auth_headers: dict):
    resp = await client.post(
        "/api/v1/products/",
        json={"name": "Widget", "price": "10.00"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Widget"
    assert data["is_active"] is True


# ── List ──────────────────────────────────────────────────────────────────────


async def test_list_products(client: AsyncClient, auth_headers: dict):
    await _create_product(client, auth_headers, "Gadget", "5.00")
    resp = await client.get("/api/v1/products/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert all(p["is_active"] for p in resp.json())


async def test_list_products_excludes_inactive_by_default(
    client: AsyncClient, auth_headers: dict
):
    p = await _create_product(client, auth_headers, "ToDeactivate", "1.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    ids = [x["id"] for x in (await client.get(
        "/api/v1/products/", headers=auth_headers
    )).json()]
    assert p["id"] not in ids


async def test_list_products_include_inactive(
    client: AsyncClient, auth_headers: dict
):
    p = await _create_product(client, auth_headers, "OldItem", "1.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    resp = await client.get(
        "/api/v1/products/?include_inactive=true", headers=auth_headers
    )
    assert resp.status_code == 200
    ids = [x["id"] for x in resp.json()]
    assert p["id"] in ids


# ── Get ───────────────────────────────────────────────────────────────────────


async def test_get_product(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "Thing", "3.50")
    resp = await client.get(f"/api/v1/products/{p['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == p["id"]


async def test_get_product_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


# ── Update ────────────────────────────────────────────────────────────────────


async def test_update_product(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "OldName", "1.00")
    resp = await client.put(
        f"/api/v1/products/{p['id']}",
        json={"name": "NewName", "price": "2.00"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "NewName"
    assert float(data["price"]) == 2.00


async def test_update_inactive_product_rejected(
    client: AsyncClient, auth_headers: dict
):
    p = await _create_product(client, auth_headers, "Inactive", "5.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    resp = await client.put(
        f"/api/v1/products/{p['id']}",
        json={"name": "ShouldFail", "price": "9.00"},
        headers=auth_headers,
    )
    assert resp.status_code == 409


# ── Deactivate / Restore ──────────────────────────────────────────────────────


async def test_deactivate_product(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "Active", "5.00")
    resp = await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False


async def test_deactivate_already_inactive(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "Active2", "5.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    resp = await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    assert resp.status_code == 409


async def test_restore_product(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "ToRestore", "5.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    resp = await client.post(
        f"/api/v1/products/{p['id']}/restore", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is True


async def test_restore_already_active(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "AlreadyActive", "5.00")
    resp = await client.post(
        f"/api/v1/products/{p['id']}/restore", headers=auth_headers
    )
    assert resp.status_code == 409


# ── History ───────────────────────────────────────────────────────────────────


async def test_history_after_update(client: AsyncClient, auth_headers: dict):
    p = await _create_product(client, auth_headers, "Original", "10.00")
    await client.put(
        f"/api/v1/products/{p['id']}",
        json={"name": "Updated", "price": "12.00"},
        headers=auth_headers,
    )
    resp = await client.get(
        f"/api/v1/products/{p['id']}/history", headers=auth_headers
    )
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) == 1
    entry = history[0]
    assert entry["change_type"] == "update"
    assert entry["name"] == "Original"
    assert float(entry["price"]) == 10.00


async def test_history_after_deactivate_and_restore(
    client: AsyncClient, auth_headers: dict
):
    p = await _create_product(client, auth_headers, "Lifecycle", "7.00")
    await client.post(
        f"/api/v1/products/{p['id']}/deactivate", headers=auth_headers
    )
    await client.post(
        f"/api/v1/products/{p['id']}/restore", headers=auth_headers
    )
    resp = await client.get(
        f"/api/v1/products/{p['id']}/history", headers=auth_headers
    )
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) == 2
    types = [h["change_type"] for h in history]
    assert "deactivate" in types
    assert "restore" in types


async def test_history_empty_for_new_product(
    client: AsyncClient, auth_headers: dict
):
    p = await _create_product(client, auth_headers, "Fresh", "3.00")
    resp = await client.get(
        f"/api/v1/products/{p['id']}/history", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json() == []
