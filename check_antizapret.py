#!/usr/bin/env python 
#-*- coding: utf8 -*-
'''**************************************************************************
check_antizapret.py - Plugin for nagios to check domains or ip addresses in zapret-info.gov.ru
Using API service http://antizapret.info/

Copyright © 2013 Denis Khabarov aka 'Saymon21'
E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
***************************************************************************
'''

import urllib2, argparse
from simplejson import loads as json_load

cliparser = argparse.ArgumentParser(description='''Plugin for nagios to check domains or ip addresses in zapret-info.gov.ru
Copyright © 2013 by Denis Khabarov aka \'Saymon21\'
E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)
Homepage: http://opensource.hub21.ru/nagios_check_antizapret_info
Licence: GNU General Public License version 3
You can download full text of the license on http://www.gnu.org/licenses/gpl-3.0.txt''',
formatter_class=argparse.RawDescriptionHelpFormatter)
cliparser.add_argument('-H','--host',metavar='ADDR', help='domain name or ip address',required=True,type=str)
cliparser.add_argument('--timeout',metavar='VALUE',help='http query timeout',default=10,type=float)
cliargs = cliparser.parse_args()

def main():
	output = ''
	exit_code = 3
	url = "http://api.antizapret.info/get.php?item=%s&type=json" % cliargs.host
	try:
		result = urllib2.urlopen(url,timeout = cliargs.timeout)

	except urllib2.URLError as err_msg:
		output = ('Antizapret.info error: %s' % err_msg)
		exit_code = 3
	data = json_load(result.read())
	
	if data.has_key('register'):
		if data['register'] is None:
			print ('OK %s is not found in zapret-info.gov.ru. Updated: %s' %(cliargs.host,data['updateTime']))
			exit(0)
		for i in data['register']:
			output += ('\n%s is found in register. For get more information see: %s' % (i['url'],i['proof']))
			exit_code = 2
	print(output)
	exit(exit_code)
	
if __name__ == "__main__":
	main()
