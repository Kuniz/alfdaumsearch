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

if sys.version[0] == "2":
    from workflow import web, Workflow
else:
    from workflow3 import web, Workflow


# lan : all
# eng : English

def get_data(dic_req, word):
    url = 'http://suggest.dic.daum.net/dic_all_ctsuggest'

    params = dict(mod='json',
                  code='utf_in_out',
                  enc='utf',
                  cate=dic_req,
                  q=word
                  )

    r = web.get(url, params)
    r.raise_for_status()
    return r.json()


def main(wf):
    dic_req = wf.args[0]
    args = wf.args[1]

    wf.add_item(title='Searching Daum%s for \'%s\'' % (dic_req, args),
                autocomplete=args,
                arg=args,
                valid=True)

    def wrapper():
        return get_data(dic_req, args)

    res_json = wf.cached_data('d%s_%s' % (dic_req, args), wrapper, max_age=30)

    for txt in res_json['items']:
        if len(txt) > 0:
            stxt = txt.split('|')
            wf.add_item(
                title='%s  %s' % (stxt[1], stxt[2]),
                subtitle='Searching Daum%s for \'%s\'' % (dic_req, stxt[1]),
                autocomplete=stxt[1],
                arg=stxt[1],
                valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
