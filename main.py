# -*- coding:utf-8 -*-
import base64
import hmac
import re
import sys

from workflow import Workflow3


def base64_hmac(key, string, length=12):
    h = hmac.new(key.encode(), string.encode()).digest()
    pwd = re.sub(r'[^\w\s]', '', base64.standard_b64encode(h))[:length]
    return pwd


def main(wf):
    try:
        args = wf.args
        arg_length = len(args[0].split())

        if arg_length == 2:
            account, salt = args[0].split()
            pwd = base64_hmac(salt, account)

            '''
                第一个参数是标题
                第二个参数是副标题
                copytext:   Ctrl + C 复制到剪切板的内容
                valid:      是否可选择
                arg:        传递给下一个动作的参数，如 {query}
            '''

            wf.add_item("Password Generator", pwd, copytext=pwd, valid=True, arg=pwd)
            wf.send_feedback()

        elif arg_length == 3:
            account, salt, length = args[0].split()
            try:
                length = int(length)
            except:
                wf.add_item("Password Generator", "第三个参数要求是数字")
                wf.send_feedback()
                return

            pwd = base64_hmac(salt, account, int(length))

            wf.add_item("Password Generator", pwd, copytext=pwd, valid=True, arg=pwd)
            wf.send_feedback()

        else:
            wf.add_item("Password Generator", "例: account@example.com 123456")
            wf.send_feedback()
    except:
        wf.add_item("Password Generator", "输入错误")
        wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
