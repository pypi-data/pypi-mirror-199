class MathJSON:
    def __init__(self, dict):
        self.dict = dict
        
    def __add__(self, other):
        return MathJSON({
            "operation": "ADD",
            "arguments": [self.dict, other.dict]
        })
    
    def __mul__(self, other):
        return MathJSON({
            "operation": "MULTIPLY",
            "arguments": [self.dict, other.dict]
        })
    
    def __sub__(self, other):
        return MathJSON({
            "operation": "SUBTRACTION",
            "arguments": [self.dict, other.dict]
        })

    def __pow__(self, other):
        return MathJSON({
            "operation": "POWER",
            "arguments": [self.dict, other.dict]
        })
    
    def __truediv__(self, other):
        return MathJSON({
            "operation": "DIVISION",
            "arguments": [self.dict, other.dict]
        })

    def func(self, variables):
        return MathJSON({
            "operation": "FUNCTION",
            "arguments": [self.dict, variables.dict]
        })

    def integrate(self, measure):
        return MathJSON({
            "operation": "INTEGRAL",
            "arguments": [self.dict, measure.dict]
        })

    def differentiate(self, measure):
        return MathJSON({
            "operation": "DIFFERENTIAL",
            "arguments": [self.dict, measure.dict]
        })

    def limit(self, measure):
        return MathJSON({
            "operation": "LIMIT",
            "arguments": [self.dict, measure.dict]
        })

    def series(self, measure):
        return MathJSON({
            "operation": "SERIES",
            "arguments": [self.dict, measure.dict]
        })

    def solve(self, measure):
        return MathJSON({
            "operation": "SOLVE",
            "arguments": [self.dict, measure.dict]
        })

    def simplify(self, measure):
        return MathJSON({
            "operation": "SIMPLIFY",
            "arguments": [measure.dict]
        })

    def expand(self, measure):
        return MathJSON({
            "operation": "EXPAND",
            "arguments": [measure.dict]
        })

    def numerical(self, measure):
        return MathJSON({
            "operation": "NUMERICAL",
            "arguments": [self.dict, measure.dict]
        })

    def plot(self, measure):
        return MathJSON({
            "operation": "PLOT",
            "arguments": [measure.dict]
        })

    def function(self, measure):
        return MathJSON({
            "operation": "FUNCTION",
            "arguments": [self.dict, measure.dict]
        })

    def build_int(self, integer):
        return MathJSON({
            "operation": "BUILD_INT",
            "arguments": str(integer)
        })

    def build_float(self, float):
        return MathJSON({
            "operation": "BUILD_FLOAT",
            "arguments": str(float)
        })

    def build_tensor(self, tensor_repr):
        return MathJSON({
            "operation": "BUILD_TENSOR",
            "arguments": str(tensor_repr)
        })

    def build_variable(self, variable_repr):
        return MathJSON({
            "operation": "BUILD_VARIABLE",
            "arguments": str(variable_repr)
        })

    def build_function(self, function):
        return MathJSON({
            "operation" : "BUILD_FUNCTION",
            "arguments" : str(function)
        })

    def build_minus(self, object):
        return MathJSON({
            "operation": "BUILD_MINUS",
            "arguments": [object.dict]
        })

    def array(self, objects : list):
        "Expects an list of MathJSON objects, or Nodes."
        return MathJSON({
            "operation": "ARRAY",
            "arguments": objects
        })

    def sin(self):
        return MathJSON({
            "operation": "SIN",
            "arguments": [self.dict]
        })

    def cos(self):
        return MathJSON({
            "operation": "COS",
            "arguments": [self.dict]
        })

    def tan(self):
        return MathJSON({
            "operation": "TAN",
            "arguments": [self.dict]
        })

    def asin(self):
        return MathJSON({
            "operation": "ASIN",
            "arguments": [self.dict]
        })

    def acos(self):
        return MathJSON({
            "operation": "ACOS",
            "arguments": [self.dict]
        })

    def atan(self):
        return MathJSON({
            "operation": "ATAN",
            "arguments": [self.dict]
        })

    def sinh(self):
        return MathJSON({
            "operation": "SINH",
            "arguments": [self.dict]
        })

    def cosh(self):
        return MathJSON({
            "operation": "COSH",
            "arguments": [self.dict]
        })

    def tanh(self):
        return MathJSON({
            "operation": "TANH",
            "arguments": [self.dict]
        })

    def asinh(self):
        return MathJSON({
            "operation": "ASINH",
            "arguments": [self.dict]
        })

    def acosh(self):
        return MathJSON({
            "operation": "ACOSH",
            "arguments": [self.dict]
        })

    def atanh(self):
        return MathJSON({
            "operation": "ATANH",
            "arguments": [self.dict]
        })

    def exp(self):
        return MathJSON({
            "operation": "EXP",
            "arguments": [self.dict]
        })

    def constant(self):
        return MathJSON({
            "operation": "CONSTANT",
            "arguments": [self.dict]
        })



