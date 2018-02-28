from decimal import Decimal, getcontext
from vector import Vector

# 设置Decimal数值精度
getcontext().prec = 30

# Line类
class Line(object):

    # ERROR MSG
    NORMAL_VECTOR_TYPE_ERROR_MSG = 'Normal Vector must be object of Vector'
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    # 构建函数, normal_vector =  Vector([a, b])为此Line的法向量
    def __init__(self, normal_vector=None, constant_term=None):
        # 获取Vector维度
        self.dimension = len(normal_vector)

        # 如果Vector.coordinates为空
        if not normal_vector.coordinates:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)

        # 检查normal_vector类型
        type_normal_vector = type(normal_vector)
        if not (type_normal_vector is Vector):
            raise Exception(NORMAL_VECTOR_TYPE_ERROR_MSG)

        # Line法向量赋值
        self.normal_vector = normal_vector
        self.coordinates = self.normal_vector.coordinates

        # k值检查
        if not constant_term:
            constant_term = Decimal('0')

        # Line k值赋值
        self.constant_term = Decimal(constant_term)

        # 设置round四舍五入精度
        self.num_decimal_places = 3

        # 计算, 设置基点
        self.set_basepoint()

    # 设置basepoint(基点), 找坐标轴交点
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
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None

            else:
                raise e

    # 格式化输出
    def __str__(self):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        # 空格, 符号变量输出格式化函数
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
            terms = [ write_coefficient( n[i], is_initial_term = ( i == initial_index ) ) + 'x_{}'.format(i+1)
                        for i in range(self.dimension) if round( n[i], num_decimal_places ) != 0 ]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'

            else:
                raise e

        # 等式右边(k值)格式化处理
        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)

        output += ' = {}'.format(constant)
        return(output)

    # 返回第一个非零值, 如若Vector.coordinates = [0, 0](原点), 则报错
    def first_nonzero_index(self):
        for k, item in enumerate(self.coordinates):
            if not self.is_zero(item):
                return(k)

        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    # 检测是否为0
    def is_zero(self, value, eps = 1e-10):
        return(abs(value) < eps)

    # 计算指定x值的y值
    def get_y(self, x):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        A = self.coordinates[0]
        B = self.coordinates[0]
        k = self.constant_term
        if B == 0:
            return(False)

        result = (k - A * x) / B
        result = round(result, num_decimal_places)
        return(Decimal(result))

    # 计算指定y值的x值
    def get_x(self, y):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        A = self.coordinates[0]
        B = self.coordinates[0]
        k = self.constant_term
        if A == 0:
            return(False)

        result = (k - B * y) / A
        result = round(result, num_decimal_places)
        return(Decimal(result))

    # 检查是否平行
    def is_parallel(self, line):
        if (not self == line) and (self.normal_vector.is_parallel(line.normal_vector)):
            return(True)

        else:
            return(False)

    # 检查是否相等
    def __eq__(self, line):
        # Check zero vector
        if self.normal_vector.is_zero():
            if line.normal_vector.is_zero():
                return(True)

            else:
                return(False)

        elif self.is_zero(line.constant_term - self.constant_term):
            return(True)

        # Get Vector v from line.basepoint - self.basepoint
        v = line.basepoint - self.basepoint
        #if (v.coordinates[0] == 0) and (v.coordinates[1] == 0):
            #x = line.basepoint.coordinates[0] + Decimal('0')
            #y = line.get_y(x)
            #v = Vector([x, y])
            #v = v - self.basepoint

        # v同时与两直线法线正交时相等
        if v.is_orthogonal(self.normal_vector) and v.is_orthogonal(line.normal_vector):
            return(True)

        else:
            return(False)

    # 计算交点
    def intersection(self, line):
        # round四舍五入精度配置读取
        num_decimal_places = self.num_decimal_places

        # 判断是否平行
        if self.is_parallel(line):
            print('is parallel')
            return(False)

        # 判断是否相等
        if self == line:
            print('is equal')
            return(False)

        # 变量取值
        # Ax + By = k1
        # Cx + By = k2
        l1 = self
        l2 = line
        v1 = self.normal_vector
        v2 = line.normal_vector
        vc1 = v1.coordinates
        vc2 = v2.coordinates

        # 如若等式一中A为0, 则与等式二交换位置
        A = vc1[0]
        if A == 0:
            l1, l2 = l2, l1
            v1, v2 = v2, v1
            vc1, vc2 = vc2, vc1
            A = vc1[0]

        B = vc1[1]
        k1 = l1.constant_term
        C = vc2[0]
        D = vc2[1]
        k2 = l2.constant_term

        # 计算交点值
        x = Decimal((D * k1 - B * k2) / (A * D - B * C))
        y = Decimal((A * k2 - C * k1) / (A * D - B * C))
        x = round(x, num_decimal_places)
        y = round(y, num_decimal_places)

        # 返回Vector
        result = Vector([x, y])
        return(result)

# main run part
if __name__ == '__main__':
    A = 4.046
    B = 2.836
    k1 = 1.21
    C = 10.115
    D = 7.09
    k2 = 3.025
    v1 = Vector([A, B])
    v2 = Vector([C, D])
    line1 = Line(v1, k1)
    line2 = Line(v2, k2)
    print(line1)
    print(line2)
    print(line1.is_parallel(line2))
    print(line1 == line2)
    print(line1.intersection(line2))
    print('---------------------------------')

    A = 7.204
    B = 3.182
    k1 = 8.68
    C = 8.172
    D = 4.114
    k2 = 9.883
    v1 = Vector([A, B])
    v2 = Vector([C, D])
    line1 = Line(v1, k1)
    line2 = Line(v2, k2)
    print(line1)
    print(line2)
    print(line1.is_parallel(line2))
    print(line1 == line2)
    print(line1.intersection(line2))
    print('---------------------------------')

    A = 1.182
    B = 5.562
    k1 = 6.744
    C = 1.773
    D = 8.343
    k2 = 9.525
    v1 = Vector([A, B])
    v2 = Vector([C, D])
    line1 = Line(v1, k1)
    line2 = Line(v2, k2)
    print(line1)
    print(line2)
    print(line1.is_parallel(line2))
    print(line1 == line2)
    print(line1.intersection(line2))
    print('---------------------------------')

    A = 0
    B = 0
    k1 = 1.000000000001
    C = 0
    D = 0
    k2 = 1.000000000002
    v1 = Vector([A, B])
    v2 = Vector([C, D])
    line1 = Line(v1, k1)
    line2 = Line(v2, k2)
    print(line1)
    print(line2)
    print(line1.is_parallel(line2))
    print(line1 == line2)
    print(line1.intersection(line2))
    print('---------------------------------')
