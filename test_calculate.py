import random
import calculate

def testSimplifyPlusAndMinus(expression):
    functionOne = simplifyPlusAndMinus(expression)
    if eval(expression) > 0:
        evalOne = '+'
    else:
        evalOne = '-'
    try:
        assert functionOne == evalOne
        print('Expression: ' + expression + ' OK: ' + functionOne + ' ' + str(eval(expression)))
    except:
        print('Expression: ' + expression + ' FAILED'  + functionOne + ' ' + str(eval(expression)))

def testconvertUnaryOperators():
    print('This: ', calculate.convertUnaryOperators('-1'), '\nFrom: -1')
    print('This: ', calculate.convertUnaryOperators('+1'), '\nFrom: +1')
    for i in range(10):
        expression = '1'
        for section in ['-'*random.randint(0, 10) if i % 2 == 0 else '+'*random.randint(0, 10) for i in range(50)]:
            expression += section
            expression += ')'*random.randint(0, 1)
            expression += ' '*random.randint(0, 1)
        expression += '11'
        converted = calculate.convertUnaryOperators(expression)
        print('This: ', converted, converted.count('m'), '\nFrom: ', expression, expression.count('-'))
    for i in range(10):
        expression = ''
        for section in ['-'*random.randint(0, 10) if i % 2 == 0 else '+'*random.randint(0, 10) for i in range(50)]:
            expression += section
            expression += ')'*random.randint(0, 1)
            expression += ' '*random.randint(0, 1)
        expression += '11'
        converted = calculate.convertUnaryOperators(expression)
        print('This: ', converted, converted.count('m'), '\nFrom: ', expression, expression.count('-'))

def testCalculateFromString():
    for i in ['1', '1+1', '1-1', '1*1', '1/1', '12', '12+1', '12-1', '21*1', '(12/1)', '3+4*2 / ( 1 - 5 ) ** 2 ** 3',
    '!', '/', '**', '+', '-', '*', '(', ')', '3+4*2 / ( 1 - 5 ) ** 2 ** 3!', 'ur mum', '((1+1)', '(1+1)/12-123)',
    '1--1', '1+-1', '12++(12--+-+2)--2', '-1']:
        try:
            result = calculate.calculateFromString(i)
            print('Input: "' + i + '" gave result: ' + str(result))
            try:
                assert result == eval(i)
                print('OK!')
            except:
                print('NOOOO!')
        except Exception as e:
            print('Input: "' + i + '" gave error: ' + str(e))

testconvertUnaryOperators()