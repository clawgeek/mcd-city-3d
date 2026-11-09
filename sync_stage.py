#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 mcd-city.html 的 module 脚本语法，并同步到 mcd3d/ 打包目录。

3D 段（stage3d.js 的内容）已内嵌进 mcd-city.html，本脚本只做两件事：
  1. 用 node 的 vm 模块做真实语法校验（防止括号不配对导致脚本静默失效）
  2. 把通过校验的文件同步到 mcd3d/index.html
"""
import pathlib, subprocess, sys

WS = pathlib.Path(__file__).resolve().parent
MAIN = WS / 'mcd-city.html'
PKG = WS / 'mcd3d' / 'index.html'
NODE = r"C://Users//10099//.workbuddy//binaries//node//versions//22.22.2-6//node.exe"


def check_syntax(text: str) -> str:
    tag = '<script type="module">'
    i = text.find(tag)
    if i < 0:
        return '找不到 module script'
    j = text.find('</script>', i)
    code = text[i + len(tag):j]
    tmp = WS / '_syntax_check.mjs'
    tmp.write_text(code, encoding='utf-8')
    r = subprocess.run(
        [NODE, '--experimental-vm-modules', '-e',
         "const fs=require('fs'),vm=require('vm');"
         "try{ new vm.SourceTextModule(fs.readFileSync(process.argv[1],'utf8')); console.log('OK'); }"
         "catch(e){ console.log(e.message); process.exit(1); }", str(tmp)],
        capture_output=True, text=True, encoding='utf-8')
    tmp.unlink(missing_ok=True)
    out = (r.stdout or '').strip()
    return '' if out == 'OK' else out


def main() -> int:
    text = MAIN.read_text(encoding='utf-8')
    err = check_syntax(text)
    if err:
        print('❌ 语法校验失败：', err)
        return 1
    print('✅ 语法校验通过')
    if PKG.parent.is_dir():
        PKG.write_text(text, encoding='utf-8')
        print('✅ 已同步到 mcd3d/index.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())
