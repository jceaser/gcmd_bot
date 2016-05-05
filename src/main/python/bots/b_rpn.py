import sys, math

from b_bot import BBot

class BRpn(BBot):
    def __init__(self):
        BBot.__init__(self)
    
    def math(self, formula):
        stack = []
        for o in formula.split(" "):
            
            #floating point operations
            if o in ["+", "-", "*", "/", "^", "log"]:
                y,x = float(stack.pop()),float(stack.pop())
                if o == "+":
                    stack.append(x + y)
                elif o == "-":
                    stack.append(x - y)
                elif o == "*":
                    stack.append(x * y)
                elif o == "/":
                    stack.append(x / y)
                elif o == "^":
                    stack.append(x ** y)
                elif o == "log":
                    stack.append(math.log(x, y))
            
            #integer operations
            elif o in ["&", "|", "<<", ">>", "^^"]:
                y,x = int(stack.pop()),int(stack.pop())
                if o == "&":
                    stack.append(x & y)
                elif o == "|":
                    stack.append(x | y)
                elif o == "<<":
                    stack.append(x << y)
                elif o == ">>":
                    stack.append(x >> y)
                elif o == "^^":
                    stack.append(x ^ y)
            
            #single floating point operations
            elif o in ["sqrt", "sin", "cos", "tan"]:
                x = float(stack.pop())
                if o=="sqrt":
                    stack.append(math.sqrt(x))
                if o=="sin":
                    stack.append(math.sin(x))
                if o=="cos":
                    stack.append(math.cos(x))
                if o=="tan":
                    stack.append(math.tan(x))
            
            #single integer operations
            elif o in ["!", "~"]:
                x = int(stack.pop())
                if (o=="!" or o=="~"):
                    stack.append(~ x)
            
            #constant additions
            elif o in ["pi", "e"]:
                if o == "pi":
                    stack.append(math.pi)
                elif o=="e":
                    stack.append(math.e)
            else:
                stack.append(o)
        return stack.pop()
    
    
    def action(self, cmd, data, found):
       return str(self.math(found.group(1)))
       

def main(argv):
    bt = BRpn()
    print bt.math(argv[0])

if __name__ == "__main__": main(sys.argv[1:])
