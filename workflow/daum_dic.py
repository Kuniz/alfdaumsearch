"""
Daum Search Workflow for Alfred 2
Copyright (c) 2021 Jinuk Baek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

from workflow import web, Workflow


# lan : all
# eng : English

def get_data(dic_req, word):
    url = 'https://suggest.dic.daum.net/language/v1/search.json'

    params = dict(cate=dic_req,
                  q=word
                  )

    r = web.get(url, params)
    r.raise_for_status()
    return r.json()


def main(wf):
    dic_req = wf.args[0]
    args = wf.args[1]

    it = wf.add_item(title='Searching Daum%s for \'%s\'' % (dic_req, args),
                autocomplete=args,
                arg=args,
                copytext=args,
                largetext=args,
                quicklookurl='https://dic.daum.net/search.do?dic=%s&q=%s' % (dic_req, args),
                valid=True)
    it.setvar('lang', dic_req)

    def wrapper():
        return get_data(dic_req, args)

    res_json = wf.cached_data('d%s_%s' % (dic_req, args), wrapper, max_age=30)

    for txt in res_json['items'][dic_req]:
        if len(txt['item']) > 0:
            stxt = txt['item'].split('|')
            it = wf.add_item(
                title='%s  %s' % (stxt[1], stxt[2]),
                subtitle='Searching Daum%s for \'%s\'' % (dic_req, stxt[1]),
                autocomplete=stxt[1],
                arg=stxt[1],
                copytext=stxt[2],
                largetext=stxt[1],
                quicklookurl='https://dic.daum.net/search.do?dic=%s&q=%s' % (dic_req, stxt[1]),
                valid=True)
            it.setvar('lang', dic_req)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
