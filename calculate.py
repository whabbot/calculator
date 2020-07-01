# using the shunting yard algorithm to parse simple mathematical expressions
# create tokens -> create tree

from re import sub
import sys

'''https://en.wikipedia.org/wiki/Shunting-yard_algorithm
https://stackoverflow.com/questions/1593080/how-can-i-modify-my-shunting-yard-algorithm-so-it-accepts-unary-operators
    https://en.wikipedia.org/wiki/Parsing'''

# also: http://effbot.org/zone/simple-top-down-parsing.htm

operators = { # accepted mathematical operators with their priorities and associativity
        '(': (0, None),
         ')': (0, None),
        '-' : (2, 'Left'),
        '+' : (2, 'Left'),
        '*' : (3, 'Left'),
        '/' : (3, 'Left'),
        '**' : (4, 'Right'),
        'm' : (5, 'Right')
    }

# def simplifyPlusAndMinus(unary_operators_string):
#     '''
#     Simplifies a string of unary + and - operators to the simplest form. Eg:
#     "+-+-+" -> "+"; "--+--+-++" -> "-"
#     '''
#     if list(unary_operators_string).count('m') % 2 == 1:
#         return 'm'
#     else:
#         return 'p'

def convertUnaryOperators(expression):
    '''
    Turns all unary operators "+" and "-" in an expression into "p" and "m" respectively

    Note: want \D that ignores )
    '''
    # remove spaces from expression
    expression = expression.replace(' ', '')
    # remove all unary pluses
    converted_pluses = sub(r'(?<=[^\d)])\++|^\++', r'', expression)
    # convert unary "-" into the symbol "m"
    converted_pluses_and_minuses = sub(r'(?<=[^\d)])-+?|^-+?', r'm', converted_pluses)
    return converted_pluses_and_minuses

# def processUnaryOperators(expression):
#     '''
#     Processes an expression with unary "+" and "-" operators into a form using only binary
#     operators which is usable in tokeniseExpression(). Eg:
#     "(+2 - 2)" -> "(2 - 2)"; "(-2 + +2)" -> "((0 - 2) + 2)"
#     '''
#     return sub(r'\D-', '(0-1)*', ' ' + expression) # kind of works. Example where it doesn't: 2**-3 -> 2**(0-1)*3 == (2**-1)*3. Also need it to ignore spaces

def tokeniseExpression(expression):
    '''
    Takes a mathematical expression as a string and returns a list of the corresponding tokens
    '''
    expressionString = expression
    tokens = []
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    # consecutive numbers are all one token - add each to this variable to be added all at once
    numberToTokenise = ''
    for character in expression:
        if character in operators:
            # if we arrive at an operator, we must have reached the end of the number in front
            if numberToTokenise != '':
                tokens.append(float(numberToTokenise))
                numberToTokenise = ''
            # if there are two "*" in a row, turn into a single "**" token
            # else simply add the operator
            if tokens and (character == tokens[-1] == '*'):
                tokens[-1] = '**'
            else:
                tokens.append(character)
        elif character in numbers:
            numberToTokenise += character
        # can only deal with numbers, spaces and the above operators/brackets
        else:
            raise ValueError('Invalid operator: ' + character)
    # one we reach the end of the expression, add the last number to the tokens list if not already
    # added
    if numberToTokenise != '': 
        tokens.append(float(numberToTokenise))
    return tokens

def toReversePolishNotation(tokens):
    '''
    Takes a list of tokens in infix-notation order and returns a list of tokens in reverse-Polish-
    notation order
    '''
    queue = []
    stack = []
    for token in tokens:
        # numbers get sent straight to the queue
        if type(token) == float:
            queue.append(token)
        # operators which aren't brackets get added to the stack unless there is an operator on the
        # stack which is either:
        # * higher priority than the token, or
        # * the same priority as the token and the token is left associative
        # in which cases the operator on the stack is sent to the queue
        elif token in operators and token != '(' and token != ')':
            while stack and stack[-1] in operators and stack[-1] != '(' and (operators[stack[-1]][0] > operators[token][0] or operators[stack[-1]][0] == operators[token][0] and operators[token][1] == 'Left'):
                queue.append(stack.pop())
            stack.append(token)
        # left brackets are added to the stack
        elif token == '(':
            stack.append(token)
        # if the token is a right bracket, operators on the stack are removed until a left bracket
        # is reached, at which point both brackets are deleted
        elif token == ')':
            while stack and stack[-1] != '(':
                queue.append(stack.pop())
            if not stack:
                raise ValueError('Mismatched brackets') # maybe change to print("Error:...")
            elif stack[-1] == '(':
                stack.pop()
    # once all of the tokens have been read, clear the stack
    # if there is still a "(" left, there must have been mismatched brackets in the input
    # expression
    while stack:
        if stack[-1] == '(':
            raise ValueError('Mismatched brackets')
        else:
            queue.append(stack.pop())
    return queue

def operation(left, token, right):
    '''
    Takes a string representing an operator and two numbers, left and right, and returns the
    result of the mathematical computation "left [token] right", or "[token]right" for unary
    operators
    Eg:
    token = '-', left = 1, right = 2 -> returns the result of 1 - 2 = -1
    token = '**', left = 3, right = 2 -> returns the result of 3 ** 2 = 9
    token = 'm', right = 2 -> returns -2
    '''
    if token == '+':
        return left + right
    elif token == '-':
        return left - right
    elif token == '/':
        return left / right
    elif token == '*':
        return left * right
    elif token == '**':
        return left ** right
    elif token == 'm':
        return -right

def RPNCalculate(RPNTokens):
    '''
    Takes a list of tokens in Reverse-Polish-Notation order and performs the corresponseing
    mathematical computations, returning the result
    '''
    result = []
    for token in RPNTokens:
        if type(token) == float:
            result.append(token)
        elif token in operators:
            try:
                right = result.pop()
                if token == 'm':
                    left = None
                else:
                    left = result.pop()
            except IndexError:
                print('Not enough numbers!')
            except:
                print('An error occurred with RPNCalculate with tokens %s' % RPNTokens)
                raise
            else:
                result.append(operation(left, token, right))
    # If result is a round number, display as an integer rather than a float (eg 1 not 1.0)
    if result:
        if result[0] % 1 == 0:
            return int(result[0])
        else:
            return result[0]

def calculateFromString(stringExpression):
    '''
    Takes a mathematical expression as a string and performs the corresponding calculations,
    returning the result as a number (float or integer)
    '''
    processedExpression = convertUnaryOperators(stringExpression)
    tokens = tokeniseExpression(processedExpression)
    RPNTokens = toReversePolishNotation(tokens)
    return RPNCalculate(RPNTokens)