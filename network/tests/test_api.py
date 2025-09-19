import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from network.models import NetworkNode


@pytest.fixture
def staff_client(client, db):
    user = User.objects.create_user(
        username="staff", password="pass", is_active=True, is_staff=True
    )
    client.login(username="staff", password="pass")
    return client


def test_permissions_active_staff_only(client, db):
    resp = client.get(reverse("suppliers-list"))
    assert resp.status_code in (401, 403)


def test_create_and_filter_by_country(staff_client, db):
    # создать завод (supplier=None)
    resp = staff_client.post(
        reverse("suppliers-list"),
        {
            "name": "Samsung Factory",
            "email": "f@samsung.com",
            "country": "South Korea",
            "city": "Seoul",
            "street": "Teheran-ro",
            "house_number": "1",
            "debt": "0.00",
        },
        content_type="application/json",
    )
    assert resp.status_code == 201

    # фильтрация по стране
    resp = staff_client.get(reverse("suppliers-list") + "?country=South Korea")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_update_cannot_change_debt(staff_client, db):
    node = NetworkNode.objects.create(
        name="BestBuy",
        email="bb@example.com",
        country="USA",
        city="NY",
        street="5th Ave",
        house_number="1",
        debt="123.45",
    )
    url = reverse("suppliers-detail", args=[node.id])
    resp = staff_client.patch(url, {"debt": "1.00"}, content_type="application/json")
    assert resp.status_code in (200, 202)
    node.refresh_from_db()
    assert str(node.debt) == "123.45"
