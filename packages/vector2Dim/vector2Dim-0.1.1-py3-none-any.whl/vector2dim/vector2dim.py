import math
import numbers
import random
from typing import Union, Type


class Vector:

    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:

        self.x = x
        self.y = y
        self._real_numbers = numbers.Real
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

class Vector2Dim(Vector):

    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:
        super().__init__(x, y)

    def __radd__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(self.x + other, self.y + other)
        else:
            return Vector2Dim(self.x + other.x, self.y + other.x)

    def __add__(self, other: Union[numbers.Real, Vector]) -> Vector:
        return self.__radd__(other)
    
    def __rsub__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(other - self.x, other - self.y)
        else:
            return Vector2Dim(other.x - self.x, other.y - self.y)

    def __sub__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(self.x - other, self.y - other)
        else:
            return Vector2Dim(self.x - other.x, self.y - other.y)

    def __rtruediv__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(other/self.x, other/self.y)
        else:
            return Vector2Dim(other.x/self.x, other.y/self.y)

    def __truediv__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(self.x/other, self.y/other)
        else:
            return Vector2Dim(self.x/other.x, self.y/other.y)
    
    def __rmul__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            return Vector2Dim(other * self.x, other * self.y)
        else:
            return Vector2Dim(other.x * self.x, other.y * self.y)
    
    def __mul__(self, other: Union[numbers.Real, Vector]) -> Vector:
        return  self.__rmul__(other)
    
    def __iadd__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            self.x += other
            self.y += other
        else:
            self.x += other.x
            self.y += other.y
        return self
    
    def __isub__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            self.x -= other
            self.y -= other
        else:
            self.x -= other.x
            self.y -= other.y
        return self
    
    def __itruediv__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            self.x /= other
            self.y /= other
        else:
            self.x /= other.x
            self.y /= other.y
        return self
    
    def __imul__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            self.x *= other
            self.y *= other
        else:
            self.x *= other.x
            self.y *= other.y
        return self
    
    def __imod__(self, other: Union[numbers.Real, Vector]) -> Vector:
        if isinstance(other, self._real_numbers):
            self.x %= other
            self.y %= other
        else:
            self.x %= other.x
            self.y %= other.y
        return self

    def __neg__(self) -> Vector:
        return Vector2Dim(-self.x, -self.y)
    
    def __pos__(self) -> Vector:
        return Vector2Dim(+self.x, +self.y)
    
    def __mod__(self, scalar) -> Vector:
        return Vector2Dim(self.x%scalar, self.y%scalar)
    
    def __abs__(self) -> float:
        return self.mag()
    
    def __eq__(self, other: Vector) -> bool:
        return (self.x == other.x and self.y == other.y)
    
    def __ne__(self, other: Vector) -> bool:
        return (self.x != other.x or self.y != other.y)
    
    def __lt__(self, other: Vector) -> bool:
        return self.mag() < other.mag()
    
    def __le__(self, other: Vector) -> bool:
        return self.mag() <= other.mag()
    
    def __gt__(self, other: Vector) -> bool:
        return self.mag() > other.mag()
    
    def __ge__(self, other: Vector) -> bool:
        return self.mag() >= other.mag()
    
    def set_values(self, x: float, y: float) -> None:
        
        """
        set x and y value
        """
        
        self.x, self.y = x, y
    
    def set_x(self, value: Union[int, float]) -> None:

        """
        set x value
        """
        
        self.x = value
    
    def set_y(self, value: Union[int, float]) -> None:
        
        """
        set y value
        """
        
        self.y = value
    
    def from_list(self, array: Union[list[float], tuple[float, float]]) -> Vector:
        
        """
        create Vector2Dim from array or tuple 
        """

        return Vector2Dim(array[0], array[1])

    def mult(self, other: Union[numbers.Real, Vector]) -> Vector:

        """
        multiply a scalar or Vector2Dim with Vector2Dim
        """

        if isinstance(other, self._real_numbers):
            self.x *= other
            self.y *= other
        else:
            self.x *= other.x
            self.y *= other.y
        return self
    
    def dot(self, other: Vector) -> float:
        
        """
        dot product
        """
        
        return (self.x * other.x) + (self.y * other.y)
    
    def cross(self, other: Vector) -> float:

        """
        cross product
        """
        
        return self.x * other.y - self.y * other.x
    
    def adds(self, other: Union[numbers.Real, Vector]) -> Vector:

        """
        adds scalar or Vector2Dim with Vector2Dim
        """
        
        if isinstance(other, self._real_numbers):
            self.x += other
            self.y += other
        else:
            self.x += other.x
            self.y += other.y
        return self

    def divide(self, other: Union[numbers.Real, Vector]) -> Vector:

        """
        divide scalar or Vector2Dim with Vector2Dim
        """

        if isinstance(other, self._real_numbers):
            self.x /= other
            self.y /= other
        else:
            self.x /= other.x
            self.y /= other.y
        return self

    def subtract(self, other: Union[numbers.Real, Vector]) -> Vector:

        """
        subtract scalar or Vector2Dim with Vector2Dim
        """

        if isinstance(other, self._real_numbers):
            self.x -= other
            self.y -= other
        else:
            self.x -= other.x
            self.y -= other.y
        return self
        
    def to_power(self, pot: int|float):

        """
        raise the Vector2Dim to a power
        """

        self.x = pow(self.x, pot)
        self.y = pow(self.y, pot)
        return self

    def copy(self) -> Vector:

        """
        make a copy of a Vector2Dim
        """
        
        return Vector2Dim(self.x, self.y)
    
    def angle(self) -> float:
        
        """
        calculate the angle in radians

        """
        
        return math.atan2(self.y, self.x)
    
    def perpendicular(self) -> Vector:
        
        """
        calculate perpendicular Vector2Dim
        """
        
        return Vector2Dim(-self.y, self.x)
    
    def mag(self) -> float:

        """
        calculate magnitude
        """

        return math.sqrt(self.x**2 + self.y**2)

    def to_polar(self) -> tuple[float, float]:

        """
        convert cartesian to polar coordinates.

        return: tuple[mag, angle in radians]
        """

        return (self.mag(), self.heading())
    
    def to_cartesian(self, polar: tuple[float, float]) -> tuple[float, float]:

        """
        convert polar to cartesian coordinates

        polar: tuple[mag, angle in radians]
        """

        return (polar[0] * math.cos(polar[1]), polar[0] * math.sin(polar[1]))


    def from_polar(self, polar: tuple[float, float]) -> Vector:

        """
        create Vector2Dim from polar coordinate
        """

        x, y = self.to_cartesian(polar=polar)
        return Vector2Dim(x, y)
    
    def normalize(self) -> Vector:

        """
        normalize Vector2Dim
        """
        
        m = self.mag()
        if m > 0:
            self.x /= m
            self.y /= m
        return self
        
    def mag_square(self) -> float:

        """
        squared mag
        """
        
        m = self.mag()
        return m**2
    
    def set_mag(self, scalar: float) -> Vector:

        """
        set magnitude
        """
        
        self.normalize()
        self.x *= scalar
        self.y *= scalar
        return self
    
    def limit(self, max_value: float) -> Vector:

        """
        limit magnitude
        """

        m = self.mag()
        if m > max_value:
            self.set_mag(max_value)
        return self
    
    def rotate(self, radians: float) -> Vector:

        """
        rotate vector by a certain amount (in radians)
        """
        
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)
        return Vector2Dim(x, y)

    def distance_to(self, other: Vector) -> float:
        
        """
        calculate distante between self and other Vector2Dim
        """
        
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def distance_squared_to(self, other: Vector) -> float:

        """
        calculate squared distante between self and other Vector2Dim
        """

        return (self.x - other.x)**2 + (self.y - other.y)**2
    
    def get_coord(self) -> tuple[float, float]:

        """
        get x and y as a tuple
        """
        
        return (self.x, self.y)


    """
    follow static method
    """

    @staticmethod
    def ones() -> Vector:
        return Vector2Dim(1, 1)
    
    @staticmethod
    def zeros() -> Vector:
        return Vector2Dim(0, 0)

    @staticmethod
    def get_distance(vec1: Vector, vec2:Vector) -> float:
        d = math.sqrt((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)
        return d

    @staticmethod
    def find_projection(point_a: Vector, point_b: Vector, point_c: Vector):
        p1 = point_b - point_a
        p2 = point_c - point_a
        p2.normalize()
        scalar_projection = p1.dot(p2)
        p2.mult(scalar_projection)
        p2.add(point_a)
        return p2
    
    @staticmethod
    def random_Vector2Dim():
        x = random.random()
        y = random.random()
        return Vector2Dim(x, y)
    
    @staticmethod
    def adds(vec1: Vector, vec2:Vector) -> Vector:
        x = vec1.x + vec2.x
        y = vec1.y + vec2.y
        return Vector2Dim(x, y)

    @staticmethod
    def subtract(vec1: Vector, vec2:Vector) -> Vector:
        x = vec1.x - vec2.x
        y = vec1.y - vec2.y
        return Vector2Dim(x, y)
    
    @staticmethod
    def divide(vec1: Vector, vec2:Vector) -> Vector:
        x = vec1.x/vec2.x
        y = vec1.y/vec2.y
        return Vector2Dim(x, y)
    
    @staticmethod
    def multiply(vec1: Vector, vec2:Vector) -> Vector:
        x = vec1.x/vec2.x
        y = vec1.y/vec2.y
        return Vector2Dim(x, y)

    @staticmethod
    def inner(vec1: Vector, vec2:Vector) -> float:
        return vec1.x * vec2.x + vec1.y * vec2.y


    


