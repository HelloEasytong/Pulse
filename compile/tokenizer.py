import re
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

# 定义token类型
TOKEN_TYPES = {
    'COMMENT': r'\/\/.*|\/\*[\s\S]*?\*\/',
    'KEYWORD': r'\b(text|if|struct|else|class|until|finish|repeat|foreach|rand|using|return|fun|read|null)\b',
    'CLASS': r'\b(str|int)\b',
    'BOOL': r'\b(True|False)\b',
    'NUMBER': r'\b\d+\b',
    'STRING': r'\'[^\']*\'|\"[^\"]*\"',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'EXCAPE': r'->',
    'OPERATOR': r'[+\-*/=<>!@#$%^&|]+',
    'LINE': r'[,;]',
    'BRACE': r'[{}()]',
    'COLON': r':+',
    'WHITESPACE': r'\s+',
}

# 定义tokenize函数，用于将代码字符串分解为token列表
def tokenize(code:str) -> list:
    # 初始化token列表
    tokens = []
    # 当代码字符串不为空时，循环执行以下操作
    while code:
        # 初始化匹配结果
        match = None
        # 遍历所有token类型和正则表达式
        for token_type, pattern in TOKEN_TYPES.items():
            # 编译正则表达式
            regex = re.compile(pattern)
            # 使用正则表达式匹配代码字符串
            match = regex.match(code) 
            # 如果匹配成功
            if match:
                # 如果token类型不是空白符或注释，将其添加到token列表中
                if token_type != 'WHITESPACE':  # 忽略空白符
                    if token_type != 'COMMENT' :  # 忽略注释
                        if token_type != 'LINE':  # 忽略其他
                            tokens.append((token_type, match.group(0)))
                # 截取代码字符串中已匹配的部分
                code = code[match.end():]
                # 跳出循环
                break
        # 如果匹配失败
        if not match: 
            # 抛出异常
            print(Fore.RED + f"Error parsing statement: {code[0]}" + Style.RESET_ALL) 
            return 
    # 返回token列表
    return tokens
