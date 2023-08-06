from .models import Car


async def car_init():
    cars = await Car.all()
    if not cars:
        await Car.create(transport="bus")
        await Car.create(transport="car")
        await Car.create(transport="truck")
