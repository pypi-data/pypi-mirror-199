import unittest
from fractions import Fraction

from momlib import Vector, DimensionMismatchError
from tests.helpers import rand_index, rand_num, rand_vec, maybe


class TestVector(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Vector([])
        initializer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        vec1 = Vector(initializer)
        for i in range(10):
            self.assertEqual(vec1[i], initializer[i])

    def test_len(self):
        vec = rand_vec(5)
        self.assertEqual(len(vec), 5)

    def test_getitem(self):
        vec = rand_vec(5)
        item = None
        with self.assertRaises(IndexError):
            item = vec[5]
        item = vec[3]
        self.assertEqual(item, vec[3])

    def test_iter_next(self):
        vec = Vector([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual([i for i in vec], [i for i in range(1, 10)])

    def test_repr(self):
        for i in range(1, 10):
            vec = rand_vec(i)
            self.assertEqual(vec, eval(repr(vec)))

    def test_hash(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec2 = Vector(vec1.elements)
            self.assertEqual(hash(vec1), hash(vec2))

    def test_dot(self):
        vec1 = Vector([0, 0, 0])
        vec2 = rand_vec(3)
        self.assertEqual(vec1 @ vec2, 0)
        with self.assertRaises(DimensionMismatchError):
            vec1.__matmul__(Vector([1, 2]))

    def test_get_slice(self):
        vec1 = rand_vec(5)
        vec2 = vec1[2:4]
        for i in range(0, 2):
            self.assertEqual(vec1[i + 2], vec2[i])
        with self.assertRaises(ValueError):
            vec1[2:2]
        self.assertEqual(vec1, vec1[:])

    def test_multiply(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec2 = rand_vec(length)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            vec1_mul_vec2 = vec1 * vec2
            for i in range(length):
                self.assertEqual(vec1_mul_vec2[i], vec1[i] * vec2[i])
            vec1_mul_n = vec1 * n
            for i in range(length):
                self.assertEqual(vec1_mul_n[i], vec1[i] * n)
            n_mul_vec2 = n * vec2
            for i in range(length):
                self.assertEqual(n_mul_vec2[i], n * vec2[i])

    def test_division(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec2 = rand_vec(length)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            vec1_div_vec2 = vec1 / vec2
            for i in range(length):
                self.assertEqual(vec1_div_vec2[i], vec1[i] / vec2[i])
            vec1_div_n = vec1 / n
            for i in range(length):
                self.assertEqual(vec1_div_n[i], vec1[i] / n)
            n_div_vec2 = n / vec2
            for i in range(length):
                self.assertEqual(n_div_vec2[i], n / vec2[i])

    def test_addition(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec2 = rand_vec(length)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            vec1_add_vec2 = vec1 + vec2
            for i in range(length):
                self.assertEqual(vec1_add_vec2[i], vec1[i] + vec2[i])
            vec1_add_n = vec1 + n
            for i in range(length):
                self.assertEqual(vec1_add_n[i], vec1[i] + n)
            n_add_vec2 = n + vec2
            for i in range(length):
                self.assertEqual(n_add_vec2[i], n + vec2[i])

    def test_subtraction(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec2 = rand_vec(length)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            vec1_sub_vec2 = vec1 - vec2
            for i in range(length):
                self.assertEqual(vec1_sub_vec2[i], vec1[i] - vec2[i])
            vec1_sub_n = vec1 - n
            for i in range(length):
                self.assertEqual(vec1_sub_n[i], vec1[i] - n)
            n_sub_vec2 = n - vec2
            for i in range(length):
                self.assertEqual(n_sub_vec2[i], n - vec2[i])

    def test_neg(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)

            neg_vec1 = -vec1
            for i in range(length):
                self.assertEqual(neg_vec1[i], -vec1[i])

    def test_equality(self):
        for _ in range(10):
            length = rand_index()
            vec1 = rand_vec(length)
            vec1_els = vec1.elements
            if maybe():
                vec1_els[min(length - 1, rand_index())] += 1
            vec2 = Vector(vec1_els)
            if vec1 == vec2:
                for i in range(length):
                    self.assertEqual(vec1[i], vec2[i])
            else:
                for i in range(length):
                    if vec1[i] != vec2[i]:
                        return  # found the unequal point
                self.fail()


if __name__ == "__main__":
    unittest.main()
