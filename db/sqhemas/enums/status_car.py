import enum


class StatusCar(enum.Enum):
    free = "свободна"
    repair = "на обслуживании"
    busy = "на вызове"