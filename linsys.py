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

            # round精度设置
            self.num_decimal_places = 3

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

    # Trangle在planes里面查找第v个系数的有效值(不等于0), 有值则交换到此行, 并返回True, 如若无值, 返回False
    def trans_row(self, p, v):
        for x in range(p + 1, len(self)):
            if not self.is_zero(self[x].normal_vector.coordinates[v]):
                self.swap_rows(p, x)
                return(True)

        return(False)

    # Trangle清除p行以下的plane中的第v个系数
    def clear(self, p, v):
        for x in range(p + 1, len(self)):
            base = - self[x].normal_vector.coordinates[v] / self[p].normal_vector.coordinates[v]
            self.add_multiple_times_row_to_row(base, p, x)

        return(True)

    # Trangle function
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

    # RREF使self[p].normal_vector.coordinates[v]为1
    def equal_one(self, p, v):
        base = Decimal('1') / self[p].normal_vector.coordinates[v]
        self.multiply_coefficient_and_row(base, p)
        return(True)

    # RREF向上消除self[p].normal_vector.coodinates[v]
    def clear_above(self, p, v):
        x = p - 1
        while x >= 0:
            base = - self[x].normal_vector.coordinates[v]
            self.add_multiple_times_row_to_row(base, p, x)
            x -= 1

        return(True)

    # RREF function
    def compute_rref(self):
        tf = self.compute_triangular_form()
        indices_list = tf.indices_of_first_nonzero_terms_in_each_row()
        p = len(tf) - 1
        while p >= 0:
            v = indices_list[p]
            if indices_list[p] < 0:
                p -= 1
                continue

            tf.equal_one(p, v)
            tf.clear_above(p, v)
            p -= 1
        return(tf)

    # RREF无解异常抛出
    def raise_nosolution(self):
        for plane in self.planes:
            try:
                plane.first_nonzero_index()

            except Exception as e:
                if (str(e) == 'No nonzero elements found'):
                    constant_term = plane.constant_term
                    if not plane.is_zero(constant_term):
                        raise Exception(self.NO_SOLUTIONS_MSG)

    # RREF无数解异常抛出(解的个数与维度比较, 如果有唯一解, 则解的个数与维度应该相等)
    def raise_infsolution(self):
        indicies_list = self.indices_of_first_nonzero_terms_in_each_row()
        vcount = sum([ 1 if index >= 0 else 0 for index in indicies_list ])
        dimension = self.dimension
        if vcount < dimension:
            raise Exception(self.INF_SOLUTIONS_MSG)

    # 高斯消元求解调度函数
    def do_gaussion(self):
        rref = self.compute_rref()
        rref.raise_nosolution()
        rref.raise_infsolution()
        dimension = rref.dimension
        result = [ round(rref.planes[i].constant_term, self.num_decimal_places) for i in range(dimension) ]
        return(Vector(result))

    # 高斯消元求解入口函数
    def compute_solution(self):
        try:
            return self.do_gaussion()

        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG) or \
                    (str(e) == self.INF_SOLUTIONS_MSG):
                return(str(e))

            else:
                raise e


# main run part
p1 = Plane(normal_vector = Vector([5.862, 1.178, -10.366]), constant_term = -8.15)
p2 = Plane(normal_vector = Vector([-2.931, -0.589, 5.183]), constant_term = -4.075)
s = LinearSystem([p1, p2])
t = s.compute_solution()
print(t)

p1 = Plane(normal_vector = Vector([8.631, 5.112, -1.816]), constant_term = -5.113)
p2 = Plane(normal_vector = Vector([4.315, 11.132, -5.27]), constant_term = -6.775)
p3 = Plane(normal_vector = Vector([-2.158, 3.01, -1.727]), constant_term = -0.831)
s = LinearSystem([p1, p2, p3])
t = s.compute_solution()
print(t)

p1 = Plane(normal_vector = Vector([5.262, 2.739, -9.878]), constant_term = -3.441)
p2 = Plane(normal_vector = Vector([5.111, 6.358, 7.638]), constant_term = -2.152)
p3 = Plane(normal_vector = Vector([2.016, -9.924, -1.367]), constant_term = -9.278)
p4 = Plane(normal_vector = Vector([2.167, -13.543, -18.883]), constant_term = -10.567)
s = LinearSystem([p1, p2, p3, p4])
t = s.compute_solution()
print(t)
