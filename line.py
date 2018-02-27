from decimal import Decimal, getcontext
from vector import Vector

# 设置Decimal数值精度
getcontext().prec = 30

# Line类
class Line(object):

    # error msg
    NORMAL_VECTOR_TYPE_ERROR_MSG = 'Normal Vector must be object of Vector'
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    # 构建函数
    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = len(normal_vector)
        if not normal_vector.coordinates:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)

        type_normal_vector = type(normal_vector)
        if not (type_normal_vector is Vector):
            raise Exception(NORMAL_VECTOR_TYPE_ERROR_MSG)

        self.normal_vector = normal_vector
        self.coordinates = self.normal_vector.coordinates
        if not constant_term:
            constant_term = Decimal('0')

        self.constant_term = Decimal(constant_term)
        self.set_basepoint()
        self.num_decimal_places = 3

    # 设置基点
    def set_basepoint(self):
        try:
            n = self.coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension
            initial_index = self.first_nonzero_index()
            initial_coefficient = n[initial_index]
            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None

            else:
                raise e

    # 格式化输出
    def __str__(self):
        num_decimal_places = self.num_decimal_places
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

        n = self.coordinates
        try:
            initial_index = self.first_nonzero_index()
            terms = [ write_coefficient( n[i], is_initial_term = ( i == initial_index ) ) + 'x_{}'.format(i+1)
                        for i in range(self.dimension) if round( n[i], num_decimal_places ) != 0 ]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'

            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)

        output += ' = {}'.format(constant)
        return(output)

    # 获取第一个非零值
    def first_nonzero_index(self):
        print(self.coordinates)
        for k, item in enumerate(self.coordinates):
            if not self.is_zero(item):
                return(k)

        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    # 检测是否为0
    def is_zero(self, value, eps=1e-10):
        return abs(value) < eps

# main run part
if __name__ == '__main__':
    v1 = Vector([1, 2])
    k1 = 1
    lineObj = Line(normal_vector = v1, constant_term = k1)
    print(lineObj)
    print(lineObj.basepoint)
