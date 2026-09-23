import logging
import math
from typing import List, Tuple

logger = logging.getLogger(__name__)

# Типы треугольника
EQUILATERAL = "равносторонний"
ISOSCELES = "равнобедренный"
SCALENE = "разносторонний"
NOT_TRIANGLE = "не треугольник"
INVALID = ""

# Заглушки координат
ERR_NUMERIC = (-1, -1)   # числовые, но невалидные данные
ERR_NON_NUMERIC = (-2, -2)  # нечисловые данные

FIELD_SIZE = 100
EPS = 1e-9


def _parse_sides(a: str, b: str, c: str) -> Tuple[float, float, float]:
    """Парсит стороны. Бросает ValueError, если данные не числа."""
    return float(a), float(b), float(c)


def _is_triangle(a: float, b: float, c: float) -> bool:
    """Проверка неравенства треугольника (строгое) + положительность."""
    if a <= 0 or b <= 0 or c <= 0:
        return False
    return (a + b > c + EPS) and (a + c > b + EPS) and (b + c > a + EPS)


def _triangle_kind(a: float, b: float, c: float) -> str:
    """Определяет вид треугольника."""
    if abs(a - b) < EPS and abs(b - c) < EPS:
        return EQUILATERAL
    if abs(a - b) < EPS or abs(b - c) < EPS or abs(a - c) < EPS:
        return ISOSCELES
    return SCALENE


def _calculate_vertices(a: float, b: float, c: float) -> List[Tuple[int, int]]:
    """
    Считает координаты вершин треугольника в поле 100x100.

    Обозначения:
      сторона a — напротив вершины A,
      сторона b — напротив вершины B,
      сторона c — напротив вершины C.

    Алгоритм:
      1. Кладём вершину A в (0, 0).
      2. Вершину B — в (c, 0).
      3. Вершину C находим через формулы:
             x = (a^2 + c^2 - b^2) / (2c)
             y = sqrt(a^2 - x^2)
      4. Масштабируем так, чтобы всё влезло в квадрат 100x100,
         и сдвигаем в положительные координаты.
    """
    # Координаты "в единицах длины"
    ax, ay = 0.0, 0.0
    bx, by = c, 0.0
    cx = (a * a + c * c - b * b) / (2 * c)
    cy = math.sqrt(max(a * a - cx * cx, 0.0))

    # Границы
    min_x = min(ax, bx, cx)
    max_x = max(ax, bx, cx)
    min_y = min(ay, by, cy)
    max_y = max(ay, by, cy)

    width = max_x - min_x
    height = max_y - min_y
    scale = min(FIELD_SIZE / width, FIELD_SIZE / height) if width and height else 1.0
    # Немного отступа, чтобы вершины не прилипали к краям
    margin = 5
    usable = FIELD_SIZE - 2 * margin
    scale = min(usable / width, usable / height) if width and height else 1.0

    def transform(x: float, y: float) -> Tuple[int, int]:
        # сдвигаем min в 0, масштабируем, добавляем margin, инвертируем Y (для экранных координат)
        nx = (x - min_x) * scale + margin
        ny = (max_y - y) * scale + margin
        return int(round(nx)), int(round(ny))

    return [transform(ax, ay), transform(bx, by), transform(cx, cy)]


def check_triangle(a_raw: str, b_raw: str, c_raw: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Главная функция.

    :param a_raw: строка со стороной A
    :param b_raw: строка со стороной B
    :param c_raw: строка со стороной C
    :return: (тип_треугольника, [координаты 3 вершин])
    """
    logger.info("Запрос: a=%r, b=%r, c=%r", a_raw, b_raw, c_raw)

    # 1) Парсинг
    try:
        a, b, c = _parse_sides(a_raw, b_raw, c_raw)
        logger.debug("Распарсенные стороны: a=%s, b=%s, c=%s", a, b, c)
    except (ValueError, TypeError) as ex:
        logger.error("Нечисловые входные данные: %s", ex)
        logger.exception("Traceback:")
        return INVALID, [ERR_NON_NUMERIC] * 3

    # 2) Проверка, что числа валидны и это треугольник
    if not _is_triangle(a, b, c):
        logger.warning(
            "Не треугольник или невалидные числовые данные: a=%s, b=%s, c=%s", a, b, c
        )
        return NOT_TRIANGLE, [ERR_NUMERIC] * 3

    # 3) Вид треугольника
    kind = _triangle_kind(a, b, c)

    # 4) Координаты
    try:
        vertices = _calculate_vertices(a, b, c)
    except Exception as ex:
        logger.exception("Ошибка при расчёте координат: %s", ex)
        return NOT_TRIANGLE, [ERR_NUMERIC] * 3

    logger.info("Успех: тип=%s, координаты=%s", kind, vertices)
    return kind, vertices