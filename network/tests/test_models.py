import pytest
from django.core.exceptions import ValidationError
from network.models import NetworkNode


@pytest.mark.django_db
def test_hierarchy_levels():
    factory = NetworkNode.objects.create(
        name="LG Factory",
        email="f@lg.com",
        country="Korea",
        city="Seoul",
        street="Tech",
        house_number="1",
    )
    network = NetworkNode.objects.create(
        name="DNS",
        email="dns@example.com",
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house_number="10",
        supplier=factory,
    )
    ip = NetworkNode.objects.create(
        name="ИП Иванов",
        email="ivanov@example.com",
        country="Russia",
        city="Tver",
        street="Lenina",
        house_number="5",
        supplier=network,
    )

    assert factory.level == 0
    assert network.level == 1
    assert ip.level == 2

    # Проверим, что глубже нельзя
    with pytest.raises(ValidationError):
        NetworkNode.objects.create(
            name="ИП Сидоров",
            email="sidorov@example.com",
            country="Russia",
            city="Ryazan",
            street="Sovetskaya",
            house_number="7",
            supplier=ip,
        )
