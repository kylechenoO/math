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
    def swap_rows(self, row1, row2):
        pass # add your code here

    # 系数乘法
    def multiply_coefficient_and_row(self, coefficient, row):
        pass # add your code here

    # 系数乘法后与等式相加
    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        pass # add your code here

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

if __name__ == '__main__':
    # main run part
    p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

    s = LinearSystem([p0,p1,p2,p3])
    print(s.indices_of_first_nonzero_terms_in_each_row())
    print('{}, {}, {}, {}'.format(s[0],s[1],s[2],s[3]))
    print(len(s))
    print(s)

    s[0] = p1
    print(s)

    print(s.is_zero(Decimal('1e-9')))
    print(s.is_zero(Decimal('1e-11')))
