from tortoise import Model, fields


class User(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.CharField(max_length=15, unique=True)
    username = fields.CharField(max_length=25, null=True)
    first_name = fields.CharField(max_length=25, null=True)
    language_code = fields.CharField(max_length=5, null=True)
    is_staff = fields.BooleanField(default=False)
    last_active = fields.DatetimeField(auto_now_add=True)
    number = fields.OneToOneField(
        "models.Numbers", related_name="user", null=True, on_delete=fields.SET_NULL
    )
    monitoring = fields.OneToOneField(
        "models.Tracking", related_name="user", null=True, on_delete=fields.SET_NULL
    )

    class Meta:
        table = "users"


class Numbers(Model):
    id = fields.BigIntField(pk=True)
    bus = fields.CharField(max_length=12, null=True)
    car = fields.CharField(max_length=12, null=True)
    truck = fields.CharField(max_length=12, null=True)

    class Meta:
        table = "numbers"


class Car(Model):
    id = fields.BigIntField(pk=True)
    transport = fields.CharField(max_length=9)

    class Meta:
        table = "cars"


class Tracking(Model):
    id = fields.BigIntField(pk=True)
    number = fields.CharField(max_length=12)
    checkpoint = fields.CharField(max_length=15)
    car = fields.ForeignKeyField("models.Car")
    intensity = fields.IntField()
    place = fields.IntField(null=True)

    class Meta:
        table = "monitoring"
