from typing import Sequence
import sys
import os
sys.path[0:0] = [os.path.join(sys.path[0], '../../../examples/sat')]
import sat
Sudoku = Sequence[Sequence[int]]


class SudokuSolver:
    def encode(self, x, y, n):
        return (81 * x) + (9 * y + n)

    def decode(self, n):
        d = n % 9
        if d == 0:
            d = 9
        n = (n - d) // 9
        y = n % 9
        n = (n - y) // 9
        x = n % 9
        return x, y, d

    def solve(self, sudoku: Sudoku) -> Sudoku:
        write = sat.DimacsWriter('input.txt')
        solver = sat.SatSolver()
        for i in range(9):
            x = (i // 3) * 3
            y = (i % 3) * 3
            for u in range(3):
                for v in range(3):
                    for w in range(3):
                        for z in range(3):
                            if (u != v):
                                if (w != z):
                                    for j in range(1, 10):
                                        write.writeLiteral(-(self.encode(x + u, y + w, j)))
                                        write.writeLiteral(-self.encode(x + v, y + z, j))
                                        write.finishClause()
        for row in range(9):
            for col in range(9):
                for digit in range(1, 10):
                    for digit2 in range(1, 10):
                        if digit != digit2:
                            write.writeImpl(self.encode(row, col, digit), -self.encode(row, col, digit2))
                if sudoku[row][col] != 0:
                    # ak sa v bunke už nachádza číslo, zapíšeme ho do súboru
                    write.writeLiteral(self.encode(row, col, sudoku[row][col]))
                    write.finishClause()
                # ak sa v bunke ešte nenachádza číslo, zapíšeme podmienky pre všetky čísla v bunke
                for num in range(1, 10):
                    write.writeLiteral(self.encode(row, col, num))
                write.finishClause()
                # podmienky pre riadok a stĺpec
                for num in range(1, 10):
                    # riadok
                    for c in range(9):
                        if c != col:
                            write.writeImpl(self.encode(row, c, num), -self.encode(row, col, num))
                    # stĺpec
                    for r in range(9):
                        if r != row:
                            write.writeImpl(self.encode(r, col, num), -self.encode(row, col, num))
   
        write.close()
        ok, sol = solver.solve(write, 'output.txt')
        pole = list(9 * [0] for _ in range(9))
        if ok:
            for i in sol:
                if i > 0:
                    x, y, d = self.decode(i)
                    pole[x][y] = d
        return pole
