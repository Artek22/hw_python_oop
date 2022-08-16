from dataclasses import asdict, dataclass
from typing import Dict, Sequence, Any

MIN_IN_HOUR: int = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    Длительность тренировки `duration` указана в часах.
    Дистанция `distance` - в километрах.
    Скорость `speed` - в км/ч.
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        try:
            return self.message.format(**asdict(self))
        except Exception:
            raise Exception('Ошибка форматирования сообщения.')


class Training:
    """Базовый класс тренировки.
    Длительность тренировки `duration` указана в часах.
    """
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action, duration, weight):
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Этот метод обязателен к переопределению!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CAL_RUN_1: int = 18
    CAL_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.CAL_RUN_1 * self.get_mean_speed() - self.CAL_RUN_2)
                * self.weight / self.M_IN_KM * self.duration * MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_WLK_1: float = 0.035
    CAL_WLK_2: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.CAL_WLK_1 * self.weight + self.get_mean_speed()**2
                // self.height * self.CAL_WLK_2 * self.weight)
                * self.duration * MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CAL_SWM_1: float = 1.1
    CAL_SWM_2: int = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CAL_SWM_1)
                * self.CAL_SWM_2 * self.weight)


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков.
    Создаём словарь, в котором сопоставляются коды тренировок и классы,
    которые нужно вызвать для каждого типа тренировки.
    """
    read_dict: Dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    try:
        return read_dict[workout_type](*data)
    except Exception:
        raise Exception('Неизвестный тип тренеровки.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
