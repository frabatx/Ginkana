#!/usr/bin/python3.5
'''
PORT = port sent to the previouse step
Etapa 2: Aritmetic
------------------

- Connect to server atclab.esi.uclm.es:PORT
- You will receive a text string with a mathematical operation in ASCII format.
- The expression contains parentheses and brackets, and are well balanced (there
  are so many opening and closure).
- Calculate the result of the operation and reply through the same socket, placing
  the result within parentheses.
- The process is repeated for an undetermined number of operations.

If everything is right, the server will instruct you to continue.
You have 20 seconds.

Tracks:
- The parentheses are vital, the spaces trivial.
- The symbol '/' represents an entire division.
- Example:
   - server: (2 * [3+ 5] * {1 -0})
   - client: (16)

Restrictions:
- It is not allowed to use the function eval(), exec() or any other that evaluates
  python statements.

You have 20 seconds.

'''

import socket as s


# Main function, create a client to send and receive messages with
# host: atclab.esi.uclm.es
# port: is passed in the function
# @input: port(string)
# @output: port(string)
def init(port):
    print("\n------------------STEP 2------------------\n")
    host = "atclab.esi.uclm.es"

    print("Creating socket...")
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    print("done.")

    print("Connecting to remote host on port {}...".format(int(port)))
    sock.connect((host, int(port)))
    print("done. \n")
    print("Operation step : \n")

    # Dictionary with all brackets
    bracket = "()}{[]"

    while True:
        msg, server = sock.recvfrom(1024)
        message = msg.decode()

        # Control if is not a matemathical expression
        # return next port
        if message[0] not in bracket:
            print("the message {} is not an operation".format(message.partition("\n")[0]))
            # creating a file to store the instructions
            f = open("inst_step3.txt", "w")
            f.write(message)
            f.close()
            sock.close
            return message.partition("\n")[0]

        # Control if matemathical expression from the server is valid (all brackets are balanced)
        elif trasform(message).count("(") != trasform(message).count(")"):
            # print("Message from server is {}".format(message))
            sock.close
            raise SyntaxError(
                "Parentheses are not balanced, invalid message.Connection is aborted...")

        operation = message.partition("\n")[0]

        # Elaborate the information
        num = "({})".format(Infix(operation))
        print(str(operation)+"="+str(num))

        # print("Sending result...")
        sock.sendto(num.encode(), (host, int(port)))
        # print("Result is sent")

    print("Connection is closed")


# Site of code "http://code.activestate.com/recipes/579122-simple-infix-expression-evaluation/"
# The funcion can calcolate the expression.
# 1) trasform all brackets into parenthesis
# 2) use a stack to process the mathematical expression
# 3) the division is an entire division
def Infix(expr):
    expr = list(trasform(expr))
    stack = list()
    num = ""

    while len(expr) > 0:
        c = expr.pop(0)
        if c in "0123456789.":
            num += c
        else:
            if num != "":
                stack.append(num)
                num = ""
            if c in "+-*/":
                stack.append(c)
            elif c == ")":
                num2 = stack.pop()
                op = stack.pop()
                num1 = stack.pop()
                if op == "+":
                    stack.append(str(int(num1) + int(num2)))
                elif op == "-":
                    stack.append(str(int(num1) - int(num2)))
                elif op == "*":
                    stack.append(str(int(num1) * int(num2)))
                elif op == "/":
                    stack.append(str(int(num1) // int(num2)))
    return stack.pop()


# The function trasforms the natural expression with brackets-->{[]}
# into an expression with only parenthesis-->()
def trasform(expr):
    opened = "{["
    closed = "}]"
    for ch in expr:
        if ch in opened:
            expr = expr.replace(ch, "(")
        if ch in closed:
            expr = expr.replace(ch, ")")
    return expr
