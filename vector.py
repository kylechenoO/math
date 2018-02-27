from math import sqrt, acos, pi
from decimal import Decimal, getcontext

# 设置Decimal数值精度
getcontext().prec = 15

# 向量类
class Vector(object):

    # 初始化函数
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([ Decimal(x) for x in coordinates ])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
        
    # 格式化输出
    def __str__(self):
        return('Vector: {}'.format(self.coordinates))

    # 判断等于
    def __eq__(self, v):
        return(self.coordinates == v.coordinates)

    # 重载+
    def __add__(self, v):
        result = []
        if type(v) is not Vector:
            raise TypeError('The value must be coordinates')

        if self.dimension != v.dimension:
            raise ValueError('The value lenth must be the same')

        result = [ x + y for x, y in zip(self.coordinates, v.coordinates)]
        return(result)

    # 重载-
    def __sub__(self, v):
        result = []
        if type(v) is not Vector:
            raise TypeError('The value must be coordinates')

        if self.dimension != v.dimension:
            raise ValueError('The value lenth must be the same')

        result = [ x - y for x, y in zip(self.coordinates, v.coordinates) ]
        return(Vector(result))

    # 重载*
    def __mul__(self, v):
        result = []
        typev = type(v)
        if typev is Vector:
            if self.dimension != v.dimension:
                raise ValueError('The value lenth must be the same')

            result = sum([ x * y for x, y in zip(self.coordinates, v.coordinates) ])
            return(result)

        elif (typev is int) or (typev is float) or (typev is Decimal):
            result = [ x * Decimal(v) for x in self.coordinates ]
            return(Vector(result))

        else:
            raise TypeError('The value must be coordinates, int or float')

    # 计算维度
    def __len__(self):
        return(self.dimension)

    # 计算向量的长度
    def magnitude(self):
        result = [ pow(x, 2) for x in self.coordinates ]
        return(Decimal(sqrt(sum(result))))

    # 计算单位向量
    def normalized(self):
        try:
            magnitude = self.magnitude()
            result = self * (Decimal('1.0') / magnitude)
            return(result)

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    # 计算向量与向量间的夹角, 返回弧度/角度
    def angle(self, v, in_degress = False):
        try:
            result = []
            if type(v) is not Vector:
                raise TypeError('The value must be coordinates')

            if self.dimension != v.dimension:
                raise ValueError('The value lenth must be the same')

            normalized = self.normalized() * v.normalized()
            result = acos(normalized)
            if in_degress:
                result = Decimal(result) * Decimal('180.0') / Decimal(pi)

            return(result)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')

            else:
                raise e

    # 判断向量是否为0
    def is_zero(self):
        return(self * self == 0)

    # 判断两向量是否平行
    def is_parallel(self, v):
        try:
            if type(v) is not Vector:
                raise TypeError('The value must be coordinates')

            if self.dimension != v.dimension:
                raise ValueError('The value lenth must be the same')

            if self.is_zero() or v.is_zero():
                return(True)

            result = self.coordinates[0] / v.coordinates[0]
            i = 1
            while(i < self.dimension):
                tmp = self.coordinates[i] / v.coordinates[i]
                if result != tmp:
                    return(False)
                i += 1

            return(True)

        except Exception as e:
            raise e

    # 判断两向量是否正交
    def is_orthogonal(self, v):
        try:
            if type(v) is not Vector:
                raise TypeError('The value must be coordinates')

            if self.dimension != v.dimension:
                raise ValueError('The value lenth must be the same')

            if self.is_zero() or v.is_zero():
                return(True)

            result = self * v
            if (result == 0):
                return(True)
                
            else:
                return(False)

        except Exception as e:
            raise e

    # 求解投影向量
    def get_proj(self, v):
        return(v.normalized() * (self * v.normalized()))

    # 求解向量积
    def cross_products(self, v):
        if (self.dimension != v.dimension) or (self.dimension != 3) or (v.dimension != 3):
            raise Error('Need Vector([x, y, z])')

        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        z1 = self.coordinates[2]
        x2 = v.coordinates[0]
        y2 = v.coordinates[1]
        z2 = v.coordinates[2]

        result = [(y1 * z2 - y2 * z1), - (x1 * z2 - x2 * z1), (x1 * y2 - x2 * y1)]
        result = Vector(result)
        return(result)
