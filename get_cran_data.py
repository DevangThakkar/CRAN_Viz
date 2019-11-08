import json
import requests
from bs4 import BeautifulSoup
from lxml import html
from pprint import pprint

def parse_package(package, packages):
	page = requests.get('https://cran.r-project.org/web/packages/{}/index.html'.format(package))
	soup = BeautifulSoup(page.text, features='lxml')

	dict_ = dict()
	dict_['name'] = package
	dict_['depends'] = dict()
	dict_['imports'] = dict()
	dict_['suggests'] = dict()
	for td in soup.findAll('td'):
		if td.find(text='Depends:') is not None:
			depends = td.findNextSibling().text.strip().split(', ')
			depend_bool = []
			for depend_ in depends:
				dict_['depends'][depend_] = dict()
				if depend_ in packages:
					depend_bool.append('Y')
					dict_['depends'][depend_]['link_exists'] = 'Y'
				else:
					depend_bool.append('N')
					dict_['depends'][depend_]['link_exists'] = 'N'

		if td.find(text='Imports:') is not None:
			imports = td.findNextSibling().text.strip().split(', ')
			import_bool = []
			for import_ in imports:
				dict_['imports'][import_] = dict()
				if import_ in packages:
					import_bool.append('Y')
					dict_['imports'][import_]['link_exists'] = 'Y'
				else:
					import_bool.append('N')
					dict_['imports'][import_]['link_exists'] = 'N'

		if td.find(text='Suggests:') is not None:
			suggests = td.findNextSibling().text.strip().split(', ')
			suggest_bool = []
			for suggest_ in suggests:
				dict_['suggests'][suggest_] = dict()
				if suggest_ in packages:
					suggest_bool.append('Y')
					dict_['suggests'][suggest_]['link_exists'] = 'Y'
				else:
					suggest_bool.append('N')
					dict_['suggests'][suggest_]['link_exists'] = 'N'

	return dict_


def parse_cran_home(link):
	page = requests.get(link)
	webpage = html.fromstring(page.content)

	packages_dict = dict()
	packages = []
	for link in webpage.xpath('//a/@href'):
		if 'packages/' not in link:
			continue
		package = link.split('/')[4]
		packages.append(package)
	
	for package in packages:
		print(package)
		packages_dict[package] = parse_package(package, packages)

	with open('cran_packages.json', 'w') as f:
		json.dump(packages_dict, f, sort_keys=True, indent=4)



def main():
	link = 'https://cran.r-project.org/web/packages/available_packages_by_name.html'
	parse_cran_home(link)


if __name__ == '__main__':
	main()