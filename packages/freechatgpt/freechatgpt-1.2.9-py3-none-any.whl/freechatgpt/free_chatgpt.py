# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 10:42
# @Author  : abo123456789
# @Desc    : free_chatgpt.py
import json
from json import JSONDecodeError

import requests
import retrying
from requests import ReadTimeout


def retry_if_timeout_error(excep):
    return isinstance(excep, ReadTimeout)


class FreeChatgpt(object):

    @staticmethod
    def ask(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=4, stop_max_delay=100000,
                            wait_fixed=1500, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                # url = f'https://api.wqwlkj.cn/wqwlapi/chatgpt.php?msg={question.strip()}&type=json'
                # url = f"http://www.emmapi.com/chatgpt?text={question.strip()}"
                # url = f"https://v1.apigpt.cn/?q={question.strip()}"
                # url = f"https://api.caonm.net/api/ai/o.php?msg={question.strip()}"
                url = f"https://api.caonm.net/api/ai/o.php?msg={question.strip()}"
                print('AI问题思考中=====')
                res = requests.get(url, timeout=70)
                answer_q = None
                try:
                    if not res.text:
                        raise ReadTimeout()
                    res_json = json.loads(res.text)
                    answer_q = res_json.get("Output")
                    print(f'AI问题回答:{answer_q}')
                    if res_json.get('info'):
                        del res_json['info']
                except JSONDecodeError:
                    return {'code': 0, 'error': answer_q}
                return {'code': 1, 'text': answer_q}

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


if __name__ == '__main__':
    # r = FreeChatgpt.ask(question='帮我优化这段话:pandas快速替换所有字符中的特殊字符')
    # print(r)
    # t = FreeChatgpt.ask(question='中国文化的特点是什么？')
    # print(t)
    q = '马云'
    s = FreeChatgpt.ask(question=q)
    print(s)

