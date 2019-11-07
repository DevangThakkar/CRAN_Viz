from lxml import html
import requests
from bs4 import BeautifulSoup

page = requests.get('https://cran.r-project.org/web/packages/available_packages_by_name.html')
webpage = html.fromstring(page.content)

packages = []
for link in webpage.xpath('//a/@href'):
	if 'packages/' not in link:
		continue
	packages.append(link.split('/')[4])
# print(packages)

page1 = requests.get('https://cran.r-project.org/web/packages/plotrix/index.html')
soup = BeautifulSoup(page1.text)

for td in soup.findAll('td'):
	if td.find(text='Depends:') is not None:
		print(td.text.strip())
		print(td.findNextSibling().text.strip())
		depends = td.findNextSibling().text.strip().split(', ')
		print(depends)
		depend_bool = []
		for depend_ in depends:
			if depend_ in packages:
				depend_bool.append('Y')
			else:
				depend_bool.append('N')
		print(depend_bool)
	if td.find(text='Imports:') is not None:
		print(td.text.strip())
		print(td.findNextSibling().text.strip())
		imports = td.findNextSibling().text.strip().split(', ')
		print(imports)
		import_bool = []
		for import_ in imports:
			if import_ in packages:
				import_bool.append('Y')
			else:
				import_bool.append('N')
		print(import_bool)
	if td.find(text='Suggests:') is not None:
		print(td.text.strip())
		print(td.findNextSibling().text.strip())
		suggests = td.findNextSibling().text.strip().split(', ')
		print(suggests)
		suggest_bool = []
		for suggest_ in suggests:
			if suggest_ in packages:
				suggest_bool.append('Y')
			else:
				suggest_bool.append('N')
		print(suggest_bool)