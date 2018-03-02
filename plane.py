from decimal import Decimal, getcontext
from vector import Vector

# 设置Decimal精度
getcontext().prec = 30

# Plane类
class Plane(object):

    # error msg
    NORMAL_VECTOR_TYPE_ERROR_MSG = 'Normal Vector must be object of Vector'
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    # 初始化函数, normval_vector为此平面的法向量
    def __init__(self, normal_vector=None, constant_term=None):
        # 获取Vector维度
        self.dimension = len(normal_vector)

        # 检查normal_vector类型
        type_normal_vector = type(normal_vector)
        if not (type_normal_vector is Vector):
            raise Exception(NORMAL_VECTOR_TYPE_ERROR_MSG)

        # 如果Vector.coordinates为空
        if not normal_vector.coordinates:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
    
        # Plan法向量赋值
        self.normal_vector = normal_vector
        self.coordinates = self.normal_vector.coordinates

        # k值检查
        if not constant_term:
            constant_term = Decimal('0')

        # k值赋值
        self.constant_term = Decimal(constant_term)

        # round精度设置
        self.num_decimal_places = 3

        # 计算, 设置基点
        self.set_basepoint()

    # 设置基点, 找坐标轴交点
    def set_basepoint(self):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        try:
            n = self.coordinates
            k = self.constant_term
            basepoint_coords = ['0'] * self.dimension
            initial_index = self.first_nonzero_index()
            initial_coefficient = n[initial_index]
            basepoint_coords[initial_index] = k / initial_coefficient
            basepoint_coords[initial_index] = round(basepoint_coords[initial_index], num_decimal_places)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None

            else:
                raise e

    # 格式化输出
    def __str__(self):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        # 空格, 符号处理
        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''
            if coefficient < 0:
                output += '-'

            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return(output)

        # 格式化输出字符串
        n = self.coordinates
        try:
            initial_index = self.first_nonzero_index()
            terms = [ write_coefficient(n[i], is_initial_term=( i==initial_index )) + 'x_{}'.format(i+1)
                        for i in range(self.dimension) if round( n[i], num_decimal_places ) != 0 ]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'

            else:
                raise e

        # 等式右边(k值)格式化处理
        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)

        output += ' = {}'.format(constant)
        return(output)

    # 查找第一个不为零的index
    def first_nonzero_index(self):
        for k, item in enumerate(self.coordinates):
            if not self.is_zero(item):
                return(k)

        raise Exception(NO_NONZERO_ELTS_FOUND_MSG)

    # 判断是否为零
    def is_zero(self, value, eps = 1e-10):
        return(abs(value) < eps)

    # 判断是否平行
    def is_parallel(self, plane):
        if (not self == plane) and (self.normal_vector.is_parallel(plane.normal_vector)):
            return(True)

        else:
            return(False)

    # 判断是否相等
    def __eq__(self, plane):
        # Check zero Vector
        if self.normal_vector.is_zero():
            if plane.normal_vector.is_zero():
                return(True)

            else:
                return(False)

        elif self.is_zero(plane.constant_term - self.constant_term):
            return(True)

        # Get Vector v from plane.basepoint - self.basepoint
        v = plane.basepoint - self.basepoint
        if v.is_orthogonal(self.normal_vector) and v.is_orthogonal(plane.normal_vector):
            return(True)

        else:
            return(False)

if __name__ == '__main__':
    A = -0.412
    B = 3.806
    C = 0.728
    k1 = -3.46
    D = 1.03
    E = -9.515
    F = -1.82
    k2 = 8.65
    v1 = Vector([A, B, C])
    v2 = Vector([D, E, F])
    plane1 = Plane(v1, k1)
    plane2 = Plane(v2, k2)
    print(plane1)
    print(plane2)
    print(plane1 == plane2)
    print(plane1.is_parallel(plane2))
    print('----------------------------')

    A = 2.611
    B = 5.528
    C = 0.283
    k1 = 4.6
    D = 7.715
    E = 8.306
    F = 5.342
    k2 = 3.76
    v1 = Vector([A, B, C])
    v2 = Vector([D, E, F])
    plane1 = Plane(v1, k1)
    plane2 = Plane(v2, k2)
    print(plane1)
    print(plane2)
    print(plane1 == plane2)
    print(plane1.is_parallel(plane2))
    print('----------------------------')

    A = -7.926
    B = 8.625
    C = -7.212
    k1 = -7.952
    D = -2.642
    E = 2.875
    F = -2.404
    k2 = -2.443
    v1 = Vector([A, B, C])
    v2 = Vector([D, E, F])
    plane1 = Plane(v1, k1)
    plane2 = Plane(v2, k2)
    print(plane1)
    print(plane2)
    print(plane1 == plane2)
    print(plane1.is_parallel(plane2))
