"""
Daum Search Workflow for Alfred 2
Copyright (C) 2014  Jinuk Baek
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""



import sys

from workflow import web, Workflow

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
	import cgi;

	dic_req = wf.args[0]
	args = wf.args[1]

	wf.add_item(title = 'Searching Daum%s for \'%s\'' % (dic_req, args), 
				autocomplete=args, 
				arg=args,
				valid=True)

	def wrapper():
		return get_data(dic_req, args)


	res_json = wf.cached_data('d%s_%s' % (dic_req, args), wrapper , max_age=30)

	for txt in res_json['items']:
		if len(txt) > 0 :
			stxt = txt.split('|')
			wf.add_item(
				title = '%s  %s' % (stxt[1], stxt[2]) ,
				subtitle = 'Searching Daum%s for \'%s\'' % (dic_req, stxt[1]), 
				autocomplete=stxt[1], 
				arg=stxt[1],
				valid=True);
			
	wf.send_feedback()

				


if __name__ == '__main__':
	wf = Workflow()
	sys.exit(wf.run(main))

