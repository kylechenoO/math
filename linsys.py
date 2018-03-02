from decimal import Decimal, getcontext
from copy import deepcopy
from vector import Vector
from plane import Plane

# Decimal精度设置
getcontext().prec = 30

# LinearSystem类
class LinearSystem(object):

    # error msg
    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    # 初始化函数
    def __init__(self, planes):
        try:
            # 判断是否在同一维度进行计算
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            # 平面列表赋值
            self.planes = planes

            # 维度赋值
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    # 交换等式
    def swap_rows(self, index1, index2):
        self.planes[index1], self.planes[index2] = self.planes[index2], self.planes[index1]
        return(self.planes)

    # 系数乘法
    def multiply_coefficient_and_row(self, coefficient, index, inplace = True):
        if coefficient == 0:
            return(False)

        if inplace :
            # mul normal_vector
            self.planes[index].normal_vector = self.planes[index].normal_vector * Decimal(coefficient)

            # mul constant_term
            self.planes[index].constant_term = self.planes[index].constant_term * Decimal(coefficient)

            # flush coordinates
            self.planes[index].coordinates = self.planes[index].normal_vector.coordinates
            return(self.planes[index])

        else:
            normal_vector = self.planes[index].normal_vector * Decimal(coefficient)
            constant_term = self.planes[index].constant_term * Decimal(coefficient)
            return(Plane(normal_vector, constant_term))

    # 系数乘法后与等式相加, 不修改原planes[index1]
    # planes[index2] = planes[index1] * coefficient + planes[index2]
    def add_multiple_times_row_to_row(self, coefficient, index1, index2):
        # get mul index1
        plane = self.multiply_coefficient_and_row(coefficient, index1, inplace = False)
        if not plane:
            return(self.planes[index2])

        # add it to index2
        self.planes[index2].normal_vector = self.planes[index2].normal_vector + plane.normal_vector
        self.planes[index2].constant_term = self.planes[index2].constant_term + plane.constant_term

        # flush coordinates
        self.planes[index2].coordinates = self.planes[index2].normal_vector.coordinates
        return(self.planes[index2])

    # 查找第一个非零的系数
    def indices_of_first_nonzero_terms_in_each_row(self):
        # 获取等式个数
        num_equations = len(self)

        # 获取维度
        num_variables = self.dimension

        indices = [-1] * num_equations
        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index()

            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue

                else:
                    raise e

        return(indices)

    # 计算平面个数
    def __len__(self):
        return(len(self.planes))

    # 获取index的plane值
    def __getitem__(self, i):
        return(self.planes[i])

    # 为相应index的plane赋值
    def __setitem__(self, i, plane):
        try:
            assert plane.dimension == self.dimension
            self.planes[i] = plane

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    # 设置输出格式
    def __str__(self):
        ret = 'Linear System:\n'
        temp = [ 'Equation {}: {}'.format( i+1, p ) for i, p in enumerate( self.planes ) ]
        ret += '\n'.join(temp)
        return(ret)

    # 判断零
    def is_zero(self, value, eps=1e-10):
        return(abs(value) < eps)

# main run part
p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])
s.swap_rows(0,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print('test case 1 failed')

s.swap_rows(1,3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print('test case 2 failed')

s.swap_rows(3,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print('test case 3 failed')

s.multiply_coefficient_and_row(1,0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print('test case 4 failed')

s.multiply_coefficient_and_row(-1,2)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print('test case 5 failed')

s.multiply_coefficient_and_row(10,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print('test case 6 failed')

s.add_multiple_times_row_to_row(0,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print('test case 7 failed')

s.add_multiple_times_row_to_row(1,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print('test case 8 failed')

s.add_multiple_times_row_to_row(-1,1,0)
if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print('test case 9 failed')
