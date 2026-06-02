import pytest
from httpx import AsyncClient


async def test_register(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "password": "pass123"},
    )
    assert resp.status_code == 201
    assert "access_token" in resp.json()


async def test_register_duplicate_email(client: AsyncClient):
    payload = {"email": "dup@example.com", "password": "pass123"}
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


async def test_login(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "pass123"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "pass123"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wp@example.com", "password": "correct"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "wp@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


async def test_protected_route_without_token(client: AsyncClient):
    resp = await client.get("/api/v1/customers/")
    assert resp.status_code == 401
