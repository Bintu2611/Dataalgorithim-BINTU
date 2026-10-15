
from typing import Any, List, Union
import operator


class Stack:
    """A stack that stores items and removes the most recently added item first."""

    def __init__(self) -> None:
        # Create an empty list to hold the stack items.
        self.items: List[Any] = []

    def is_empty(self) -> bool:
        """Check whether the stack has any items."""
        return len(self.items) == 0

    def push(self, item: Any) -> None:
        """Add a new item to the top of the stack."""
        self.items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Cannot remove an item from an empty stack")

        return self.items.pop()

    def peek(self) -> Any:
        """View the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot view an empty stack")

        return self.items[-1]

    def size(self) -> int:
        """Return the number of items currently in the stack."""
        return len(self.items)


# Define the order in which mathematical operators are evaluated.
OPERATOR_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}

# Connect each operator to its corresponding Python calculation.
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def precedence(op: str) -> int:
    """Return the priority of a mathematical operator."""
    return OPERATOR_PRECEDENCE.get(op, 0)


def calculate(
    first_number: Union[int, float],
    second_number: Union[int, float],
    op: str
) -> Union[int, float]:
    """Calculate the result of an operation between two numbers."""

    if op not in OPERATORS:
        raise ValueError(f"Invalid operator: {op}")

    # Prevent division by zero.
    if op == '/' and second_number == 0:
        raise ValueError("Cannot divide by zero")

    return OPERATORS[op](first_number, second_number)


def evaluate_expression(expression: str) -> Union[int, float]:
    """Read a mathematical expression and calculate its answer."""

    number_stack = Stack()
    operator_stack = Stack()

    # Split the expression into individual numbers and operators.
    tokens = expression.split()

    for token in tokens:

        # Store numbers in the number stack.
        if token.isdigit():
            number_stack.push(int(token))

        # Save an opening bracket until its matching closing bracket.
        elif token == '(':
            operator_stack.push(token)

        # Calculate everything inside a pair of brackets first.
        elif token == ')':
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != '('
            ):
                current_operator = operator_stack.pop()
                second_number = number_stack.pop()
                first_number = number_stack.pop()

                answer = calculate(
                    first_number,
                    second_number,
                    current_operator
                )
                number_stack.push(answer)

            # Remove the opening bracket.
            if not operator_stack.is_empty():
                operator_stack.pop()

        # Handle mathematical operators according to their priority.
        elif token in OPERATORS:
            while (
                not operator_stack.is_empty()
                and operator_stack.peek() != '('
                and precedence(operator_stack.peek()) >= precedence(token)
            ):
                current_operator = operator_stack.pop()
                second_number = number_stack.pop()
                first_number = number_stack.pop()

                answer = calculate(
                    first_number,
                    second_number,
                    current_operator
                )
                number_stack.push(answer)

            operator_stack.push(token)

        else:
            raise ValueError(f"Invalid expression token: {token}")

    # Finish any calculations that remain in the operator stack.
    while not operator_stack.is_empty():
        current_operator = operator_stack.pop()
        second_number = number_stack.pop()
        first_number = number_stack.pop()

        answer = calculate(
            first_number,
            second_number,
            current_operator
        )
        number_stack.push(answer)

    # The final answer is the only number left in the stack.
    if number_stack.size() != 1:
        raise ValueError("Invalid mathematical expression")

    return number_stack.pop()


def read_expressions(filename: str) -> List[str]:
    """Read mathematical expressions from an input file."""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()

    except FileNotFoundError:
        return []

    expressions = []

    # Ignore blank lines and separator lines.
    for line in file_content.splitlines():
        expression = line.strip()

        if expression and expression != "-----":
            expressions.append(expression)

    return expressions


def write_results(
    filename: str,
    results: List[Union[int, float]]
) -> None:
    """Save the answers to a file, separating each result clearly."""

    with open(filename, 'w', encoding='utf-8') as file:
        for index, result in enumerate(results):

            # Display whole-number results without a decimal point.
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            file.write(str(result) + '\n')

            # Add a separator between results, but not after the last one.
            if index < len(results) - 1:
                file.write("-----\n")


def main() -> None:
    """Run the calculator from start to finish."""

    # Read the expressions provided in the input file.
    expressions = read_expressions('input.txt')

    if not expressions:
        print("No expressions found in 'input.txt'.")
        return

    # Calculate the answer to each expression.
    results = [
        evaluate_expression(expression)
        for expression in expressions
    ]

    # Save all answers in the output file.
    write_results('output.txt', results)

    print("All expressions have been evaluated successfully.")
    print("Please check the output.txt file for the results.")


if __name__ == "__main__":
    main()