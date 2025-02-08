from compile.modules import get_module, read_module
from colorama import Fore, Style

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

class Interpreter:
    def __init__(self):
        self.funiable = {} # 用于存储函数的字典
        self.funiable_var = {}
        self.variables = {'_name_':'pulse','_ver_':'1.0.20250106','_fun_':self.funiable,'_fun_var_':self.funiable_var}  # 用于存储全局变量的字典
        self.variables['_var_'] = self.variables
        self.kill = 0 
        self.struct_kill = 0 
        self.fun_return = None
        self.window_manager = []

    # 解释执行抽象语法树（AST）
    def interpret(self, ast):
        self.kill == 0
        try:
            len(ast)
        except:
            return
        for node in ast:
            try:
                self.execute(node)  # 执行每个AST节点
                if self.kill == 1:
                    self.kill == 0
                    break
                self.variables['_var_'] = self.variables
                self.variables['_fun_'] = self.funiable
                self.variables['_fun_var_'] = self.funiable_var
            except Exception as e:
                print(Fore.RED + f"Error executing node {node}: {e}" + Style.RESET_ALL)
                break  # 遇到错误则停止执行
    
    def struct_interpret(self,ast):
        self.struct_kill == 0
        try:
            len(ast)
        except:
            return
        for node in ast:
            try:
                self.execute(node)  # 执行每个AST节点
                if self.struct_kill == 1:
                    self.struct_kill == 0
                    break
            except Exception as e:
                print(Fore.RED + f"Error executing node {node}: {e}" + Style.RESET_ALL)
                break  # 遇到错误则停止执行

    # 执行单个节点
    def execute(self, node):
        try:
            node_type = node[0]

            # 处理返回值
            if node_type == 'return':
                self.fun_return = self.evaluate(node[1]) # 设置返回值
                self.struct_kill = 1 # 结束函数

            elif node_type == 'struct':
                self.struct_interpret(node[1]) # 执行结构

            # 处理输出文本的逻辑
            elif node_type == 'text':
                value = self.evaluate(node[1])  # 评估表达式
                end = '\n'
                if node[2]:
                    if node[3] == 'N':
                        end = ''
                    if node[4] == 'RED':
                        print(Fore.RED + str(value)  + Style.RESET_ALL, end = end)
                        return
                    if node[4] == 'YELLOW':
                        print(Fore.YELLOW + str(value)  + Style.RESET_ALL, end = end)
                        return
                    if node[4] == 'GREEM':
                        print(Fore.GREEN + str(value)  + Style.RESET_ALL, end = end)
                        return
                    if node[4] == 'BLUE':
                        print(Fore.BLUE + str(value)  + Style.RESET_ALL, end = end)
                        return
                    if node[2] == 'D':
                        pass
                print(str(value), end = end)

            # 结束语句
            elif node_type == 'finish':
                self.struct_kill = 1

            # 处理赋值语句
            elif node_type == 'assign':
                var_name = node[1]
                value = self.evaluate(node[2])  # 评估赋值表达式
                self.variables[var_name] = value

            # 处理输入语句
            elif node_type == 'read':
                user_input = input("")  # 从用户获取输入
                if node[1]:
                    if node[2] == "str":
                        user_input = str(user_input)
                    elif node[2] == "int":
                        user_input = int(user_input)
                return user_input

            # 处理条件语句
            elif node_type == 'if':
                condition = self.evaluate(node[1])  # 评估条件
                if condition:
                    self.struct_interpret(node[2])  # 执行满足条件的语句块
                elif len(node) > 3 and node[3] is not None: 
                    self.struct_interpret(node[3])  # 执行else语句块

            # 处理循环语句
            elif node_type == 'until':
                condition = self.evaluate(node[1])
                while condition:
                    print(node[2])
                    self.struct_interpret(node[2])  # 执行循环体
                    condition = self.evaluate(node[1])  # 重新评估循环条件
            
            # 处理重复循环语句
            elif node_type == 'repeat':
                condition = self.evaluate(node[1])
                for i in range(condition):
                    self.struct_interpret(node[2])

            # 处理自定义报错语句
            elif node_type == 'raise':
                text = self.evaluate(node[2])  # 评估条件
                print(Fore.RED + f"Error {node[1]}: {text}" + Style.RESET_ALL)
                self.kill == 1
                self.struct_kill == 1

            # 定义函数逻辑
            elif node_type == 'fun':
                self.funiable[node[1]] = node[2] # 自定义函数
                fun_var = node[3]
                self.funiable_var[node[1]] = fun_var # 添加局部变量
            
            # 转换与创建
            elif node_type == 'invert':
                if node[2] == 'str':
                    self.variables[node[1]] = str(self.variables[node[1]])
                elif node[2] == 'int':
                    self.variables[node[1]] = int(self.variables[node[1]])

            # 导入模块
            elif node_type == 'using':
                module = read_module(get_module())
                self.struct_interpret(module[node[1]])

            # 运行函数
            elif node_type == 'run_fun':
                sum = 0
                for i in node[2]: # 解析所有参数
                    # 别问我为什么要做这么多中间步骤,那是因为合起来会返回'~~'的错
                    j = node[1] # 将函数名称传入 j 
                    a = self.funiable_var[j] # 导航到此函数所期望的值
                    var = a[sum]
                    self.variables[var] = self.evaluate(i) # 设置变量
                    sum += 1
                self.struct_interpret(self.funiable[node[1]])
                fun_return = self.fun_return
                self.fun_return = None
                return fun_return
            
            elif node_type == 'python':
                exec(str(self.evaluate(node[1])))

        except Exception as e:
            print(Fore.RED + f"Error executing node {node}: {e}" + Style.RESET_ALL)
            self.kill = 1
            return  # 重新抛出异常以停止执行

    # 评估表达式
    def evaluate(self, node):
        try:
            node_type = node[0]

            # 处理数字
            if node_type == 'number':
                return node[1]
            
            # 处理字符串
            elif node_type == 'string': 
                return node[1]
            
            # 处理变量
            elif node_type == 'variable':
                var_name = node[1]
                if var_name not in self.variables:
                    raise NameError(f"Variable '{var_name}' is not defined")
                return self.variables[var_name]

            # 处理二元操作符
            elif node_type == 'binary_op':
                op = node[1]
                left = self.evaluate(node[2])
                right = self.evaluate(node[3])
                if op == '+':
                    return left + right
                elif op == '-':
                    return left - right
                elif op == '*':
                    return left * right
                elif op == '/':
                    return left / right
                elif op == '<':
                    return left < right
                elif op == '<=':
                    return left <= right
                elif op == '>':
                    return left > right
                elif op == '>=':
                    return left >= right
                elif op == '==':
                    return left == right
                elif op == '!=':
                    return left != right
                elif op == '&':
                    return left and right
                elif op == '|':
                    return left or right
                elif op == '>>':
                    return left >> right
                elif op == '<<':
                    return left << right
            
            # 解析关键词
            else:
                return self.execute(node)

            # 如果没有匹配到任何表达式，抛出语法错误
            raise SyntaxError(f"Unexpected evaluation: {node}")

        except Exception as e:
            print(Fore.RED + f"Error evaluating node {node}: {e}" + Style.RESET_ALL)
            self.kill = 1
            return  # 重新抛出异常以向上传播()
