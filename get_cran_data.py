import json
import requests
from bs4 import BeautifulSoup
from lxml import html
from pprint import pprint

def parse_cran_package(package):
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

		if td.find(text='Imports:') is not None:
			imports = td.findNextSibling().text.strip().split(', ')
			import_bool = []
			for import_ in imports:
				dict_['imports'][import_] = dict()

		if td.find(text='Suggests:') is not None:
			suggests = td.findNextSibling().text.strip().split(', ')
			suggest_bool = []
			for suggest_ in suggests:
				dict_['suggests'][suggest_] = dict()

	return dict_


def parse_bioc_package(package):
	page = requests.get('https://cran.r-project.org/web/packages/{}/index.html'.format(package))
	soup = BeautifulSoup(page.text, features='lxml')

	dict_ = dict()
	dict_['name'] = package
	dict_['depends'] = dict()
	dict_['imports'] = dict()
	dict_['suggests'] = dict()
	for td in soup.findAll('td'):
		if td.find(text='Depends') is not None:
			depends = td.findNextSibling().text.strip().split(', ')
			depend_bool = []
			for depend_ in depends:
				dict_['depends'][depend_] = dict()

		if td.find(text='Imports') is not None:
			imports = td.findNextSibling().text.strip().split(', ')
			import_bool = []
			for import_ in imports:
				dict_['imports'][import_] = dict()

		if td.find(text='Suggests') is not None:
			suggests = td.findNextSibling().text.strip().split(', ')
			suggest_bool = []
			for suggest_ in suggests:
				dict_['suggests'][suggest_] = dict()

	return dict_


def parse_home(link1, link2):
	page1 = requests.get(link1)
	webpage1 = html.fromstring(page1.content)
	page2 = requests.get(link2)
	webpage2 = html.fromstring(page2.content)

	packages_dict = dict()
	cran_packages = []
	bioc_packages = []
	for link in webpage1.xpath('//a/@href'):
		if 'packages/' not in link:
			continue
		package = link.split('/')[4]
		cran_packages.append(package)

	for link in webpage2.xpath('//a/@href'):
		if 'html/' not in link or '.html' not in link:
			continue
		package = link.split('/')[1].replace('.html', '')
		bioc_packages.append(package)
	
	i = 0
	for package in cran_packages:
		i+=1
		print(i)
		print(package)
		packages_dict[package] = parse_cran_package(package)

	for package in bioc_packages:
		i+=1
		print(i)
		print(package)
		packages_dict[package] = parse_bioc_package(package)

	with open('cran_packages.json', 'w') as f:
		json.dump(packages_dict, f, sort_keys=True, indent=4)



def main():
	link1 = 'https://cran.r-project.org/web/packages/available_packages_by_name.html'
	link2 = 'http://bioconductor.org/packages/3.10/bioc/'
	parse_home(link1, link2)


if __name__ == '__main__':
	main()