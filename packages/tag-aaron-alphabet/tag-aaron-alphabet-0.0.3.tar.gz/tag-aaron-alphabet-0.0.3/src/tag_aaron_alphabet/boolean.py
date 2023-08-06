

def and_operation(*operands):
    return all(operands)
def or_operation(*operands):
    return any(operands)
def xor_operation(*operands):
    return bool(sum(int(x) for x in operands) % 2)
def binary_operation(first_operand, operator, second_operand):
    return {
        '&': and_operation,
        '|': or_operation,
        '^': xor_operation,
    }[operator](first_operand, second_operand)
def not_operation(operand):
    return not operand

    