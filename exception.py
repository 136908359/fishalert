class ruleError(Exception):
    def __init__(self, expr):
        self.expr = expr    
    def __str__(self):
        return 'The rule format cannot be analysis: {expr}'.format(expr = self.expr)