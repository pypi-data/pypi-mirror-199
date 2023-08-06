import unittest
from fractions import Fraction

from momlib import Matrix, DimensionMismatchError
from tests.helpers import rand_index, rand_mat, rand_num, maybe


class TestMatrix(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Matrix([[]])
        with self.assertRaises(ValueError):
            Matrix([[1, 2, 3], [1, 2], [1, 2, 3]])
        initializer = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        mat1 = Matrix(initializer)
        for i in range(3):
            for j in range(3):
                self.assertEqual(initializer[i][j], mat1[i, j])

    def test_len(self):
        for i in range(1, 10):
            self.assertEqual(len(rand_mat(i, 10 - i)), i * (10 - i))

    def test_getitem(self):
        mat1 = Matrix([[1, 2, 3], [4, 5, 6]])
        mat2 = Matrix([[1, 2], [4, 5], [7, 8]])
        with self.assertRaises(IndexError):
            mat1[2, 0]
        with self.assertRaises(IndexError):
            mat2[0, 2]
        self.assertEqual(mat1[0, 2], 3)
        self.assertEqual(mat2[2, 1], 8)

    def test_iter_next(self):
        mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(
            [[d for d in r] for r in mat],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        )

    def test_repr(self):
        for i in range(1, 10):
            mat = rand_mat(i, 10 - i)
            self.assertEqual(mat, eval(repr(mat)))

    def test_hash(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat2 = Matrix(mat1.elements)
            self.assertEqual(hash(mat1), hash(mat2))

    def test_shape(self):
        mat1 = rand_mat(2, 3)
        self.assertEqual(mat1.shape, (2, 3))

    def test_get_slice(self):
        mat1 = rand_mat(3, 3)
        mat2 = mat1[0:2, 0:2]
        for i in range(2):
            self.assertEqual(mat1[i, i], mat2[i, i])
        with self.assertRaises(ValueError):
            mat1[2:2, 2:2]
        self.assertEqual(mat1, mat1[:, :])

    def test_matmul(self):
        mat1 = rand_mat(5, 3)
        mat2 = rand_mat(3, 5)
        mat3 = mat1 @ mat2
        mat4 = mat2 @ mat1
        self.assertEqual(mat3.shape, (5, 5))
        self.assertEqual(mat4.shape, (3, 3))
        with self.assertRaises(DimensionMismatchError):
            rand_mat(2, 3).__matmul__(rand_mat(2, 3))

    def test_multiply(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat2 = rand_mat(*size)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            mat1_mul_mat2 = mat1 * mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(
                        mat1_mul_mat2[i, j], mat1[i, j] * mat2[i, j]
                    )
            mat1_mul_n = mat1 * n
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(mat1_mul_n[i, j], mat1[i, j] * n)
            n_mul_mat2 = n * mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(n_mul_mat2[i, j], n * mat2[i, j])

    def test_division(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat2 = rand_mat(*size)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            mat1_div_mat2 = mat1 / mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(
                        mat1_div_mat2[i, j], mat1[i, j] / mat2[i, j]
                    )
            mat1_div_n = mat1 / n
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(mat1_div_n[i, j], mat1[i, j] / n)
            n_div_mat2 = n / mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(n_div_mat2[i, j], n / mat2[i, j])

    def test_addition(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat2 = rand_mat(*size)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            mat1_add_mat2 = mat1 + mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(
                        mat1_add_mat2[i, j], mat1[i, j] + mat2[i, j]
                    )
            mat1_add_n = mat1 + n
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(mat1_add_n[i, j], mat1[i, j] + n)
            n_add_mat2 = n + mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(n_add_mat2[i, j], n + mat2[i, j])

    def test_subtraction(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat2 = rand_mat(*size)
            n = rand_num()
            if n == 1 or n == 0 or n == -1:
                n += Fraction(1, 2)

            mat1_sub_mat2 = mat1 - mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(
                        mat1_sub_mat2[i, j], mat1[i, j] - mat2[i, j]
                    )
            mat1_sub_n = mat1 - n
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(mat1_sub_n[i, j], mat1[i, j] - n)
            n_sub_mat2 = n - mat2
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(n_sub_mat2[i, j], n - mat2[i, j])

    def test_neg(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)

            neg_mat1 = -mat1
            for i in range(size[0]):
                for j in range(size[1]):
                    self.assertEqual(neg_mat1[i, j], -mat1[i, j])

    def test_equality(self):
        for _ in range(10):
            size = (rand_index(), rand_index())
            mat1 = rand_mat(*size)
            mat1_els = mat1.elements
            if maybe():
                mat1_els[min(size[0] - 1, rand_index())][
                    min(size[1] - 1, rand_index())
                ] += 1
            mat2 = Matrix(mat1_els)
            if mat1 == mat2:
                for i in range(size[0]):
                    for j in range(size[1]):
                        self.assertEqual(mat1[i, j], mat2[i, j])
            else:
                for i in range(size[0]):
                    for j in range(size[1]):
                        if mat1[i, j] != mat2[i, j]:
                            return  # found the unequal point
                self.fail()


if __name__ == "__main__":
    unittest.main()
