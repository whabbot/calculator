import random
import prog.calculate as calculate
import pytest


class TestConvertUnaryOperators:
    def test_empty_string(self):
        assert calculate.convertUnaryOperators('') == ''

    def test_space_removal(self):
        assert calculate.convertUnaryOperators('1 + 1 - 1') == '1+1-1'

    def test_single_minus(self):
        assert calculate.convertUnaryOperators('-1') == 'm1'

    def test_double_minus(self):
        assert calculate.convertUnaryOperators('--1') == 'mm1'

    def test_triple_minus(self):
        assert calculate.convertUnaryOperators('---1') == 'mmm1'

    def test_minus_with_binary_minus(self):
        assert calculate.convertUnaryOperators('1--1') == '1-m1'

    def test_minus_after_right_bracket(self):
        assert calculate.convertUnaryOperators('(1)-1') == '(1)-1'

    def test_single_plus(self):
        assert calculate.convertUnaryOperators('+1') == '1'

    def test_double_plus(self):
        assert calculate.convertUnaryOperators('++1') == '1'

    def test_plus_with_binary_plus(self):
        assert calculate.convertUnaryOperators('1++1') == '1+1'

class TestCalculateFromString:
    valid_expressions = [
        '1', '1+1', '1-1', '1*1', '1/1', '12', '12+1', '12-1', '21*1',
        '(12/1)', '3+4*2 / ( 1 - 5 ) ** 2 ** 3', '-12**2', '3**-2'
        '1--1', '1+-1', '12++(12--+-+2)--2', '-1'
    ]
    invalid_operators = ['!', 'text']
    mismatched_brackets = ['(', '))', '(()', ')']
    not_enough_numbers = ['/', '**', '+', '-', '*', '']

    def test_valid_expressions(self):
        for expression in self.valid_expressions:
            assert calculate.calculateFromString(expression) == eval(expression)

    def test_invalid_operators(self):
        for expression in self.invalid_operators:
            with pytest.raises(ValueError, match=r'Invalid operator'):
                calculate.calculateFromString(expression)

    def test_mismatched_brackets(self):
        for expression in self.mismatched_brackets:
            with pytest.raises(ValueError, match=r'Mismatched brackets'):
                calculate.calculateFromString(expression)

    def test_not_enough_numbers(self):
        for expression in self.not_enough_numbers:
            with pytest.raises(ValueError, match=r'Not enough numbers'):
                calculate.calculateFromString(expression)

class TestTokeniseExpression:
    expressions = [
        '1', '1+1', '1-1', '1*1', '1/1', '12', '12+1', '12-1', '21*1',
        '(12/1)', '2**2', '1+m1', '', '12+(12-2)-m2', 'm1'
    ]
    known_tokenisations = [
        [1.0], [1.0, '+', 1.0], [1.0, '-', 1.0], [1.0, '*', 1.0],
        [1.0, '/', 1.0], [12.0], [12.0, '+', 1.0], [12.0, '-', 1.0],
        [21.0, '*', 1.0], ['(', 12.0, '/', 1.0, ')'], [2.0, '**', 2.0],
        [1.0, '+', 'm', 1.0], [],
        [12.0, '+', '(', 12.0, '-', 2.0, ')', '-', 'm', 2.0], ['m', 1.0]
    ]
    def test_known_tokenisations(self):
        for ex, tok in zip(self.expressions, self.known_tokenisations):
            assert calculate.tokeniseExpression(ex) == tok

class TestToReversePolishNotation:
    infix = [
        [1.0], [1.0, '+', 1.0], [1.0, '-', 1.0], [1.0, '*', 1.0],
        [1.0, '/', 1.0], [12.0], [12.0, '+', 1.0], [12.0, '-', 1.0],
        [21.0, '*', 1.0], ['(', 12.0, '/', 1.0, ')'], [2.0, '**', 2.0],
        [1.0, '+', 'm', 1.0], [],
        [12.0, '+', '(', 12.0, '-', 2.0, ')', '-', 'm', 2.0], ['m', 1.0]
    ]
    postfix = [
        [1.0], [1.0, 1.0, '+'], [1.0, 1.0, '-'], [1.0, 1.0, '*'],
        [1.0, 1.0, '/'], [12.0], [12.0, 1.0, '+'], [12.0, 1.0, '-'],
        [21.0, 1.0, '*'], [12.0, 1.0, '/'], [2.0, 2.0, '**'],
        [1.0, 1.0, 'm', '+'], [], [12.0, 12.0, 2.0, '-', '+', 2.0, 'm', '-'],
        [1.0, 'm']
    ]
    def test_reverse_polish_notation(self):
        for i, p in zip(self.infix, self.postfix):
            assert calculate.toReversePolishNotation(i) == p

class TestOperation:
    expressions = [
        (1, '+', 1), (1, '-', 1), (2, '*', 1), (2, '/', 2), (2, '**', 2), 
        (None, 'm', 2)
    ]
    results = [
        2, 0, 2, 1, 4, -2
    ]
    def test_operation(self):
        for ex, res in zip(self.expressions, self.results):
            assert calculate.operation(*ex) == res

class TestRPNCalculate:
    tokens = [
        [1.0], [1.0, 1.0, '+'], [1.0, 1.0, '-'], [1.0, 1.0, '*'],
        [1.0, 1.0, '/'], [12.0], [12.0, 1.0, '+'], [12.0, 1.0, '-'],
        [21.0, 1.0, '*'], [12.0, 1.0, '/'], [2.0, 2.0, '**'],
        [1.0, 1.0, 'm', '+'], [], [12.0, 12.0, 2.0, '-', '+', 2.0, 'm', '-'],
        [1.0, 'm']
    ]
    results = [1, 2, 0, 1, 1, 12, 13, 11, 21, 12, 4, 0, None, 24, -1]
    def test_RPN_calculate(self):
        for tok, res in zip(self.tokens, self.results):
            assert calculate.RPNCalculate(tok) == res