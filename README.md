<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/HelloEasytong/Pulse">
    <img src="icon/Geko Logo.png" alt="Logo" width="100" height="100">
  </a>

<h1 align="center">Pulse</h1>

<p>
    支持多功能的新一代编程语言
</p> </div>


<!-- ABOUT THE PROJECT -->
## 关于本项目

在兴趣驱动下完成的一个编程语言，是本人正式的第一个 Python 项目😫，支持模块导入，变量定义，IO，函数等功能，目前还在开发中，更新速度较慢🙁，也欢迎各位大佬来贡献代码，或者提出建议😘（Python 版本 > 3.12）。

## 版本
- 📦版本号：1.0.20250204
- 🕓日期：2025年2月4日

<!-- ROADMAP -->
## 计划

- ✅ 模块导入和编辑模块
- ✅ 函数定义和引用
- ✅ 变量定义和引用
- ✅ IO
- ✅ 使用 Python 进行编程
- ✅ 循环功能
- ✅ 基础的表达式判断
- ✅ 类之间的转换
- ✅ raise 语句
- ❌ 速度优化
  - ❌ 升级 Python 版本，突破 JIT 的性能瓶颈
  - ❌ 使用 Cython
  - ❌ 优化代码结构
- ❌ 错误处理
- ❌ 文件IO
- ❌ 集合类
- ❌ match 结构

到 [Open issues](https://github.com/HelloEasytong/Pulse/issues) 页面查看所有被请求的功能 (以及已知的问题) 。

<!-- IDEA -->
## 思路
> 1. 读取文件(main.py)
> 2. 使用正则表达式进行匹配(tokenizer.py)
> 3. 生成抽象语法树，定义一个变量用来确定当前位置，定义一个函数用来检测代码是否正确，定义一个函数用来解析表达式(paser.py)
> 4. 根据抽象语法树逐步运行(interpreter.py)

<!-- GETTING STARTED -->
## 使用

### 安装

#### 使用源码
```shell
git clone https://github.com/HelloEasytong/Pulse.git
```

#### 使用编译版本
> 预编译版本目前仅支持 Windows 系统

下载 Releases 里的 `.zip` 格式文件，解压，将里面的 `geko.exe` 放到 `PATH` 环境变量中即可使用。

### 使用

#### 使用源码
```shell
cd Pulse
python main.py <您要运行的 Pulse 文件> 
```
> 如有需要，可以在末尾添加 ‘-> token’ 或 ‘-> ast’ 来查看运行生成的 token 或 ast

#### 使用预编译版本
```shell
pulse <您要运行的 Pulse 文件>
```
> 同上

### 编程示例

#### 一个猜数字游戏（有BUG）
```c#
using rand
using time
ri = randint(1, 100)
text "一个猜数字游戏"
until True{
    num = read -> int
    if num == ri{
        text 1
        text "恭喜你猜对了！"
        finish}
    else{
        text 1
        if num > ri{
            text "猜大了！"}
        else{
            text "猜小了！"}}}
```
### 斐波那契数列
```c#
text '请输入要输出的斐波那契数列的长度：' -> 'N' 'RED'
num = read
num -> int
a = 0
b = 1
repeat num{
    a -> str
    text a + ' ' -> 'N' 'RED'
    a -> int
    a = a + b
    b = a - b}
```
> 具体语法请参考我的B站视频

<!-- LICENSE -->
## 许可证

根据 GPL v3.0 许可证分发。打开 `LICENSE` 查看更多内容。

Copyright © 2025 Easytong.

<!-- CONTACT -->
## 联系

![qq](https://img.shields.io/badge/QQ-3661724417_Easytong-aqua)

![bilibili](https://img.shields.io/badge/Bilibili-3546576561637431_Easytong-red)

![email](https://img.shields.io/badge/Email-helloeasytong%40outlook.com-blue)

![github](https://img.shields.io/badge/GitHub-HelloEasytong-green?logo=github)
