import os, glob
from compile.parser import Parser
from compile.tokenizer import tokenize

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

# 模块管理
def get_module():
    # 当前工作目录
    current_directory = os.getcwd()
    # 获取当前目录及所有子目录中的 .pe 文件
    gkm_files = glob.glob(os.path.join(current_directory, '**', '*.pe'), recursive=True)
    # 获取上层目录中的 .pe 文件
    parent_directory = os.path.dirname(current_directory)
    gkm_files += glob.glob(os.path.join(parent_directory, '*.pe'))
    return gkm_files
def read_module(module_files):
    module_code = {}
    for cr in module_files: # 遍历所有模块
        with open(cr, 'r', encoding='utf-8') as f:
            code = f.read()
            tokens = tokenize(code)
            ast = Parser(tokens)
            module_code[os.path.basename(cr[:-3])] = ast.parse() # 编译模块并添加
    return module_code