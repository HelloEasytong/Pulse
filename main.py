from compile.tokenizer import tokenize
from compile.parser import Parser
from compile.interpreter import Interpreter
import sys

#  ____          _
# |  _ \  _   _ | | ___   ___
# | |_) || | | || |/ __| / _ \
# |  __/ | |_| || |\__ \|  __/
# |_|     \__,_||_||___/ \___|

# Pulse 是一款面向过程（目前）,弱类型（目前）,简易的解释型语言，由于使用正则表达式经行匹配代码，其代码灵活性也很好

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

def main(cr = sys.argv[1]):
    with open(cr, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = tokenize(code) # 编译代码
    parser = Parser(tokens) 
    ast = parser.parse() # 编译 token
    if len(sys.argv) == 2:
        interpreter = Interpreter()
        interpreter.interpret(ast) # 编译 ast
    else:
        if sys.argv[2] == '->':
            match sys.argv[3]:
                case 'token':
                    print(tokens)
                case 'ast':
                    print(ast)

if __name__ == '__main__':
    main()