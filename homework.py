from dataclasses import dataclass, asdict
from typing import Dict, Sequence, Any

MIN_IN_HOUR = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    Длительность тренировки `duration` указана в часах.
    Дистанция `distance` - в километрах.
    Скорость `speed` - в км/ч."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            'Тип тренировки: {training_type}; '
            'Длительность: {duration:.3f} ч.; '
            'Дистанция: {distance:.3f} км; '
            'Ср. скорость: {speed:.3f} км/ч; '
            'Потрачено ккал: {calories:.3f}.'.format(**asdict(self))
        )


@dataclass
class Training:
    """Базовый класс тренировки.
    Длительность тренировки `duration` указана в часах.
    """
    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Этот метод обязателен к переопределению!
        """
        raise NotImplementedError

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
    CAL_RUN_1 = 18
    CAL_RUN_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.CAL_RUN_1 * self.get_mean_speed() - self.CAL_RUN_2)
                * self.weight / self.M_IN_KM * self.duration * MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_WLK_1 = 0.035
    CAL_WLK_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return ((self.CAL_WLK_1 * self.weight + self.get_mean_speed()**2
                // self.height * self.CAL_WLK_2 * self.weight)
                * self.duration * MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CAL_SWM_1 = 1.1
    CAL_SWM_2 = 2

    length_pool: float
    count_pool: int

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


def read_package(workout_type: Any, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков.
    Создаём словарь, в котором сопоставляются коды тренировок и классы,
    которые нужно вызвать для каждого типа тренировки.
    """
    read_dict: Dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return read_dict[workout_type](*data)


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
