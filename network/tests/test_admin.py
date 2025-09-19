import pytest
from decimal import Decimal
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

from network.admin import NetworkNodeAdmin
from network.models import NetworkNode


def _add_session_and_messages(request):
    # Подключаем сессию
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    # Подключаем messages
    setattr(request, "_messages", FallbackStorage(request))
    return request


@pytest.mark.django_db
def test_admin_action_clear_debt():
    factory = NetworkNode.objects.create(
        name="Samsung Factory",
        email="f@samsung.com",
        country="Korea",
        city="Seoul",
        street="Techno",
        house_number="1",
    )
    node = NetworkNode.objects.create(
        name="DNS",
        email="dns@example.com",
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house_number="10",
        supplier=factory,
        debt=Decimal("12345.67"),
    )

    admin = NetworkNodeAdmin(NetworkNode, AdminSite())

    rf = RequestFactory()
    request = rf.post("/admin/network/networknode/")
    request = _add_session_and_messages(request)

    queryset = NetworkNode.objects.filter(id=node.id)
    admin.clear_debt(request, queryset)

    node.refresh_from_db()
    assert node.debt == 0
