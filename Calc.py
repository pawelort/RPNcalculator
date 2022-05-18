import collections

def helper():
    print('The program calculates the sum and substraction of numbers')


def input_decompose(text):
    added_extra_spaces = ''.join([char if char.isdigit() else ' ' + char + ' ' for char in text])
    pre_equation = added_extra_spaces.split()

    special_operators = []
    equation_list = []

    for i in pre_equation:
        if i in {'+', '-'}:
            special_operators.append(i)
        elif i not in {'+', '-'} and len(special_operators) > 0:
            if set(special_operators) == {'-'}:
                equation_list.append('-' if len(special_operators) % 2 else '+')
            elif set(special_operators) == {'+'}:
                equation_list.append('+')
            special_operators.clear()
            equation_list.append(i)
        else:
            equation_list.append(i)

    return equation_list

def infix_to_postfix(equation):
    stack = collections.deque()
    result = []
    for single in equation:
        if single.isalnum():
            result.append(single)
        elif single == '(':
            stack.append(single)
        elif single in {'*', '/'}:
            if len(stack) == 0 or stack[-1] in {'+', '-', '('}:
                stack.append(single)
            else:
                while len(stack) > 0 and stack[-1] not in {'*', '/'}:
                    result.append(stack.pop())
                stack.append(single)
        elif single in {'+', '-'}:
            if len(stack) == 0 or stack[-1] in {'('}:
                stack.append(single)
            else:
                while len(stack) > 0 and stack[-1] != '(':
                    result.append(stack.pop())
                stack.append(single)
        elif single == ')':
            while stack[-1] != '(':
                try:
                    result.append(stack.pop())
                except IndexError:
                    "Invalid expression"
            stack.pop()
    while len(stack) > 0:
        result.append(stack.pop())
    return result


def calculations(equation, var_memo):
    stack = collections.deque()

    if len(equation) < 3:
        eq = ''.join(equation)
        if eq.isdigit():
            return int(eq)
        elif eq.isalpha() and var_memo.get(eq) is None:
            return "Unknown variable"
        elif eq.isalpha():
            return var_memo.get(eq)

    for single in equation:
        if single.isdigit():
            stack.append(int(single))
        elif single.isalpha() and var_memo.get(single) is None:
            return "Unknown variable"
        elif single.isalpha():
            stack.append(var_memo.get(single))
        elif single == '+':
            stack.append(stack.pop() + stack.pop())
        elif single == '-':
            stack.append(-1 * stack.pop() + stack.pop())
        elif single == '*':
            stack.append(stack.pop() * stack.pop())
        elif single == '/':
            divisor = stack.pop()
            divident = stack.pop()
            stack.append(divident / divisor)

    return int(stack[0])

def assignment(equation, var_memo):
    last_element = equation[-1]
    if last_element.isalpha() and var_memo.get(last_element) is None:
        return "Unknown variable"
    elif last_element.isalpha():
        assignment_value = var_memo.get(last_element)
    else:
        assignment_value = int(last_element)
    var_memo[equation[0]] = assignment_value
    return - 1


def unknown_command_check(text):
    if text.startswith('/'):
        print('Unknown command')
        return -1


def invalid_assignment(equation_list):
    error_msg = 'Invalid assignment'

    if equation_list.count('=') > 1:
        print(error_msg)
        return -1

    for i in equation_list[2:]:
        if i in {'+', '-', '*', '/', '(', ')'}:
            continue
        if i.isascii() and not i.isdigit() and not i.isalpha():
            print(error_msg)
            return -1


def invalid_identifier(equation_list):
    symbol_to_check = equation_list[0]
    if symbol_to_check.isascii() and not symbol_to_check.isdigit() and not symbol_to_check.isalpha():
        print('Invalid identifier')


def invalid_expression(equation_list):
    if equation_list.count('(') != equation_list.count(')'):
        print("Invalid Expression")
        return -1

    mul_operators = 0
    div_operators = 0

    for single in equation_list:
        if single == '*':
            mul_operators += 1
            if mul_operators > 1:
                print("Invalid Expression")
                return -1
        elif single == '/':
            div_operators += 1
            if div_operators > 1:
                print("Invalid Expression")
                return -1
        else:
            mul_operators = 0
            div_operators = 0

user_variables = {}
while True:
    user_input = input("Type here expression to evaluate\n")
    if user_input == '/exit':
        print("Bye!")
        break
    elif user_input == '/help':
        helper()
        continue
    elif user_input == '':
        continue
    elif unknown_command_check(user_input) == -1:
        continue

    user_equation = input_decompose(user_input)
    if invalid_identifier(user_equation) == -1:
        continue
    elif invalid_assignment(user_equation) == -1:
        continue
    elif invalid_expression(user_equation) == -1:
        continue
    elif '=' in user_equation:
        assignment(user_equation, user_variables)
    else:
        postfix_equation = infix_to_postfix(user_equation)
        result = calculations(postfix_equation, user_variables)
        print(result)
