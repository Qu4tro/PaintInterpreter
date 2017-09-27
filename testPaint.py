import unittest
import paintInterpreter


class TestSemantics(unittest.TestCase):

    def setUp(self):
        line = 'I 5 6'
        command = paintInterpreter.makeCommand(line)
        self.board = command.apply(None)

    def test_I(self):
        self.assertEqual(self.board.width, 5)
        self.assertEqual(self.board.height, 6)

    def test_C(self):
        self.board = paintInterpreter.makeCommand('F 3 3 J').apply(self.board)
        self.assertTrue(all(self.board.colors[c] != paintInterpreter.white for c in self.board.colors))
        self.board = paintInterpreter.makeCommand('C').apply(self.board)
        self.assertTrue(all(self.board.colors[c] == paintInterpreter.white for c in self.board.colors))

    def test_L(self):
        self.board = paintInterpreter.makeCommand('L 2 3 A').apply(self.board)
        self.board = paintInterpreter.makeCommand('L 4 4 4').apply(self.board)
        self.assertEqual(self.board.colors[(2, 3)], 'A')
        self.assertEqual(self.board.colors[(4, 4)], '4')
        self.assertEqual(list(self.board.colors.values()).count('A'), 1)
        self.assertEqual(list(self.board.colors.values()).count('4'), 1)

    def test_V(self):
        self.board = paintInterpreter.makeCommand('V 2 3 4 W').apply(self.board)
        self.assertEqual(self.board.colors[(2, 3)], 'W')
        self.assertEqual(self.board.colors[(2, 4)], 'W')
        self.assertEqual(list(self.board.colors.values()).count('W'), 2)

    def test_H(self):
        self.board = paintInterpreter.makeCommand('H 3 4 2 Z').apply(self.board)
        self.assertEqual(self.board.colors[(4, 2)], 'Z')
        self.assertEqual(self.board.colors[(3, 2)], 'Z')
        self.assertEqual(list(self.board.colors.values()).count('Z'), 2)

    def test_S(self):
        self.board = paintInterpreter.makeCommand('F 3 3 J').apply(self.board)
        self.board = paintInterpreter.makeCommand('L 1 1 A').apply(self.board)
        self.assertEqual(str(self.board).count('J'), 29)
        self.assertEqual(str(self.board)[0], 'A')

    def test_hasCoordinates(self):
        self.assertTrue(self.board.hasCoordinates(3, 3))
        self.assertTrue(self.board.hasCoordinates(2, 4))
        self.assertFalse(self.board.hasCoordinates(0, 0))
        self.assertFalse(self.board.hasCoordinates(6, 6))


class TestParsing(unittest.TestCase):

    def test_I(self):
        line = 'I 5 6'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.New)
        self.assertEqual(command.width, 5)
        self.assertEqual(command.height, 6)

    def test_C(self):
        line = 'C'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.Clean)

    def test_L(self):
        line = 'L 2 3 A'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.Coloring)
        self.assertEqual(command.x, 2)
        self.assertEqual(command.y, 3)
        self.assertEqual(command.color, 'A')

    def test_V(self):
        line = 'V 2 3 4 W'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.VerticalColoring)
        self.assertEqual(command.x, 2)
        self.assertEqual(command.y1, 3)
        self.assertEqual(command.y2, 4)
        self.assertEqual(command.color, 'W')

    def test_H(self):
        line = 'H 3 4 2 Z'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.HorizontalColoring)
        self.assertEqual(command.x1, 3)
        self.assertEqual(command.x2, 4)
        self.assertEqual(command.y, 2)
        self.assertEqual(command.color, 'Z')

    def test_S(self):
        line = 'S'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.Show)

    def test_X(self):
        line = 'X'
        command = paintInterpreter.makeCommand(line)
        self.assertIsNotNone(command)
        self.assertIsInstance(command, paintInterpreter.Exit)


if __name__ == '__main__':
    unittest.main()
