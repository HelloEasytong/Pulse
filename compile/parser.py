from colorama import Fore, Style
import glob
import os

#////////////////////////////////////////////////////////////////////
#//                          _ooOoo_                               //
#//                         o8888888o                              //
#//                         88" . "88                              //
#//                         (| ^_^ |)                              //
#//                         O\  =  /O                              //
#//                      ____/`---'\____                           //
#//                    .'  \\|     |//  `.                         //
#//                   /  \\|||  :  |||//  \                        //
#//                  /  _||||| -:- |||||-  \                       //
#//                  |   | \\\  -  /// |   |                       //
#//                  | \_|  ''\---/''  |   |                       //
#//                  \  .-\__  `-`  ___/-. /                       //
#//                ___`. .'  /--.--\  `. . ___                     //
#//              ."" '<  `.___\_<|>_/___.'  >'"".                  //
#//            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
#//            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
#//      ========`-.____`-.___\_____/___.-`____.-'========         //
#//                           `=---='                              //
#//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
#//         佛祖保佑       永无BUG     永不修改                     //
#////////////////////////////////////////////////////////////////////

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # 保存所有的词法分析得到的token
        self.position = 0     # 当前解析器的位置指针
        self.kill = 0  # 程序执行到目前是否有错（1 为 有错 0 为 无错）

    # 检查当前token类型和值是否与预期匹配
    def expect(self, expected_type:str, expected_value:str=None):
        token_type, value = self.tokens[self.position]
        # 如果类型或值不匹配，则抛出语法错误
        if token_type != expected_type or (expected_value is not None and value != expected_value):
            print(Fore.RED + f"Error grammatical: {expected_type} {'with value ' + expected_value if expected_value else ''}, but got {token_type} with value {value}" + Style.RESET_ALL)
            self.kill = 1
            return
        self.position += 1  # 如果匹配，指针向前移动

    # 解析整个程序，返回AST（抽象语法树）
    def parse(self):
        ast = []
        try:
            len_token = len(self.tokens)
        except:
            return
        # 循环解析直到所有token都被处理
        while self.position < len_token:
            ast.append(self.parse_statement())  # 解析语句并添加到AST
            if self.kill == 1:
                return
        return ast

    # 解析单个语句
    def parse_statement(self) -> tuple:
        token_type, value = self.tokens[self.position]

        try:
            # 解析结构
            if value == 'struct':
                self.position += 2
                self.expect('BRACE','{')
                body = self.parse_block()
                self.expect('BRACE','}')
                return ('struct', body)

            # 解析 read 语句
            elif value == 'read':
                self.position += 1
                try:
                    if self.tokens[self.position][1] == '->':
                        self.position += 1
                        parse_class = self.tokens[self.position][1]
                        self.expect("CLASS") # 期望一个类型
                        excape = True
                    else:
                        parse_class = ""
                        excape = False
                except:
                    pass
                return ('read', excape, parse_class)

            # 解析 text 语句
            elif value == 'text':
                self.position += 1
                expr = self.parse_expression()  # 解析表达式
                excape = False
                line_break = None
                color = None
                try:
                    if self.tokens[self.position][1] == '->':
                        excape = True
                        self.position += 1
                        emmm = self.tokens[self.position][1]
                        line_break = emmm.strip('\'')
                        self.expect("STRING") # 期望一个字符串
                        emmm = self.tokens[self.position][1]
                        color = emmm.strip('\'')
                        self.position += 1
                except:
                    pass
                return ('text', expr, excape, line_break, color)
            
            # 解析 finish 语句
            elif value == 'finish':
                self.position += 1
                return ('finish',)
            
            # 处理 raise 语句
            elif value == 'raise':
                self.position += 2
                error_name = self.tokens[self.position - 1][1]
                self.expect('BRACE', '(')
                error_text = self.parse_expression()  
                self.expect('BRACE', ')')
                return ('raise', error_name, error_text)

            # 解析 if 语句
            elif value == 'if':
                self.position += 1
                condition = self.parse_expression()  # 解析条件表达式
                self.expect('BRACE','{')
                body = self.parse_block()  # 解析语句块
                self.expect('BRACE','}')

                # 解析可选的 else 子句
                else_clause = None
                if self.position < len(self.tokens):
                    next_token_type, next_value = self.tokens[self.position]
                    if next_token_type == 'KEYWORD' and next_value == 'else':
                        self.position += 1
                        self.expect('BRACE')
                        else_clause = self.parse_block()
                        self.expect('BRACE')

                return ('if', condition, body, else_clause)

            # 解析 until 循环语句
            elif value == 'until':
                self.position += 1
                condition = self.parse_expression()  # 解析循环条件
                self.expect('BRACE','{')
                body = self.parse_block()
                self.expect('BRACE','}')
                return ('until', condition, body)
            
            # 解析 导入模块
            elif value == 'using':
                self.position += 2
                return ('using', self.tokens[self.position - 1][1])
            
            # 解析 repeat 循环语句
            elif value == 'repeat':
                self.position += 1
                condition = self.parse_expression() 
                self.expect('BRACE','{')
                body = self.parse_block()
                self.expect('BRACE','}')
                return ('repeat', condition, body)

            # 解析 return 语句
            elif value == 'return':
                self.position += 1
                return_value = self.parse_expression()
                return ('return', return_value)

            # 解析函数定义
            elif value == 'fun':
                self.position += 1
                fun_name = self.tokens[self.position][1]
                self.position += 1
                fun_var = []
                if self.tokens[self.position][1] == '->': # 如果自定义函数有参数
                    self.position += 1
                    while self.position < len(self.tokens) and self.tokens[self.position][1] != '{': # 匹配所有参数
                        fun_var.append(self.tokens[self.position][1]) # 添加这些参数
                        self.position += 1
                self.expect('BRACE','{')
                body = self.parse_block()
                self.expect('BRACE','}')
                return ('fun', fun_name, body, fun_var)
            
            # 解析赋值语句
            elif value == 'var':
                self.position += 1
                var = self.tokens[self.position][1]
                self.position += 1
                self.expect('OPERATOR', '=')  # 期望一个等号
                expr = self.parse_expression()
                return ('assign', var, expr)

            # 解析赋值语句
            elif token_type == 'IDENTIFIER':
                var = value
                self.position += 1
                try:
                    if self.tokens[self.position][1] == '->':
                        self.position += 2
                        return ('invert', var, self.tokens[self.position - 1][1])
                except IndexError:
                    pass 
                if self.tokens[self.position][1] == '(':
                    self.position += 1
                    fun_var = [] # 用户给的值
                    while True:
                        try:
                            if self.tokens[self.position][1] == ')':
                                break
                        except IndexError:
                            break
                        fun_var.append(self.parse_expression())
                    self.position += 1
                    return ('run_fun', var, fun_var)
                self.expect('OPERATOR', '=')  # 期望一个等号
                expr = self.parse_expression()
                return ('assign', var, expr)
            
            elif token_type == 'COLON':
                self.position += 1
                body = self.parse_expression()
                returns = False
                if value == '::':
                    returns = True
                return ('python', body, returns)

            # 如果没有匹配的语法结构，抛出错误
            print(self.position)
            print(Fore.RED + f"Error grammatical: {value}" + Style.RESET_ALL)
            self.kill = 1
            return
        
        except Exception as e:
            print(Fore.RED + f"Error executing node {self.tokens[self.position]}: {e}" + Style.RESET_ALL)
            self.kill = 1
            return  # 重新抛出异常以停止执行

    # 解析表达式
    def parse_expression(self) -> tuple:
        token_type, value = self.tokens[self.position]

        # 解析数字
        if token_type == 'NUMBER':
            self.position += 1
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
            # 检查是否有操作符
            if self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
                operator = self.tokens[self.position][1]
                self.position += 1
                right_expr = self.parse_expression()  # 解析右侧表达式
                return ('binary_op', operator, ('number', value), right_expr)
            return ('number', value)

        # 解析字符串
        elif token_type == 'STRING':
            self.position += 1
            # 检查是否有操作符
            if self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
                operator = self.tokens[self.position][1]
                self.position += 1
                right_expr = self.parse_expression()  # 解析右侧表达式
                return ('binary_op', operator, ('string', value[1:-1]), right_expr)
            return ('string', value[1:-1])

        # 解析变量
        elif token_type == 'IDENTIFIER':
            if value == ')':
                return self.parse_statement()
            self.position += 1
            # 检查是否有操作符
            if self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
                operator = self.tokens[self.position][1]
                self.position += 1
                right_expr = self.parse_expression()  # 解析右侧表达式
                return ('binary_op', operator, ('variable', value), right_expr)
            # 检查是否是函数
            if self.position < len(self.tokens) and self.tokens[self.position][1] == '(':
                self.position -= 1
                return self.parse_statement()

            return ('variable', value)

        # 解析二元运算符
        elif token_type == 'OPERATOR':
            op = value
            self.position += 1
            left = self.parse_expression()
            right = self.parse_expression()
            return ('binary_op', op, left, right)
        
        # 解析布尔值
        if token_type == 'BOOL':
            self.position += 1
            if value == 'True':
                expr =  ('binary_op', '==', ('number', 1), ('number', 1))
            else:
                expr =  ('binary_op', '==', ('number', 1), ('number', 2))
            # 检查是否有操作符
            if self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
                operator = self.tokens[self.position][1]
                self.position += 1
                right_expr = self.parse_expression()  # 解析右侧表达式
                return ('binary_op', operator, expr, right_expr)
            if value == 'true':
                return expr
            else:
                return expr
        
        if (token_type == 'KEYWORD') or (token_type == 'COLON'):
            self.position += 1
            # 检查是否有操作符
            if self.position < len(self.tokens) and self.tokens[self.position][0] == 'OPERATOR':
                self.position -= 1
                value = self.parse_statement()
                operator = self.tokens[self.position][1]
                right_expr = self.parse_expression()  # 解析右侧表达式
                return ('binary_op', operator,  value, right_expr)
            self.position -= 1
            return self.parse_statement()

        # 如果没有匹配的表达式，抛出错误
        print(Fore.RED + f"Error expression: {value}" + Style.RESET_ALL)
        self.kill = 1
        return  

    # 解析语句块
    def parse_block(self) -> list:
        block = []
        # 循环解析块中的所有语句，直到遇到'}'
        while self.position < len(self.tokens) and self.tokens[self.position][1] != '}':
            block.append(self.parse_statement())
        return block

