from decimal import Decimal, getcontext
from copy import deepcopy
from vector import Vector
from plane import Plane

# Decimal精度设置
getcontext().prec = 30

# LinearSystem类
class LinearSystem(object):
    # 初始化函数
    def __init__(self, planes):
        # error msg
        self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
        self.NO_SOLUTIONS_MSG = 'No solutions'
        self.INF_SOLUTIONS_MSG = 'Infinitely many solutions'
        self.NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

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

            # update basepoint
            self.planes[index].set_basepoint()
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

        # update basepoint
        self.planes[index2].set_basepoint()
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
                if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
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

    # 在planes里面查找是否某个系数有值, 有值则交换到此行, 如若无值, 返回False
    def trans_row(self, p, v):
        for x in range(p + 1, len(self)):
            if not self.is_zero(self[x].normal_vector.coordinates[v]):
                self.swap_rows(p, x)
                return(True)

        return(False)

    # 清楚某行以下的等式中的v系数
    def clear(self, p, v):
        for x in range(p + 1, len(self)):
            base = - self[x].normal_vector.coordinates[v] / self[p].normal_vector.coordinates[v]
            self.add_multiple_times_row_to_row(base, p, x)

        return(True)

    # 计算三角形
    def compute_triangular_form(self):
        # 拷贝, 以防修改外部变量
        system = deepcopy(self)

        # p为plane, v为系数(vector中的一个值)
        p = 0
        v = 0
        for p in range(len(system)):
            while v < system.dimension:
                if system.is_zero(system[p].normal_vector.coordinates[v]):
                    if not system.trans_row(p, v):
                        v += 1
                        continue

                system.clear(p, v)
                p += 1
                break
            v += 1
        return(system)

# main run part
p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print('test case 1 failed')

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print('test case 2 failed')

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        t[3] == Plane()):
    print('test case 3 failed')

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print('test case 4 failed')
