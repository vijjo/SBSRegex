from bs4 import BeautifulSoup, NavigableString, Tag
from pprint import pprint
import re
import mammoth


def tab_number(text):
    tabs = re.findall(r'\s*@+\s*', text) 
    return len(tabs)


def word_role(symbol):
    if symbol == 'v':
        result = 'verb'
    elif symbol == 'n':
        result = 'noun'
    elif symbol == 'pn':
        result = 'pron'
    else:
        result = symbol
    return result


def part_of_speech(symbol):
    if symbol == 'm':
        result = 'masc'
    elif symbol == 'f':
        result = 'fem'
    elif symbol == 'n':
        result = 'nom'
    elif symbol == 'ac':
        result = 'acc'
    else:
        result = symbol
    return result
    

with open('APC key to idioms.docx', 'rb') as f:
    result = mammoth.convert_to_html(f)
with open('idioms.html', 'w') as f:
    f.write(result.value.replace('\t', '@'))

with open('idioms.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if paragraph.string:
            if paragraph.string.strip().startswith('@'):
                previous = paragraph.previous_sibling
                if previous.string:
                    paragraph.string = previous.string + ' ' + paragraph.string.strip('\n @')
                previous.decompose()

    for paragraph in paragraphs:
        if paragraph.string and not paragraph.strong:
            if paragraph.string.strip().endswith('@'):
                paragraph.string = paragraph.string.rstrip('@\n ')
        elif paragraph.strong and paragraph.previous_sibling.strong:
            previous = paragraph.previous_sibling
            previous.append(soup.new_tag('br'))
            previous.extend(paragraph.contents)

    for paragraph in paragraphs:
        if paragraph.string and not paragraph.strong:
            text = paragraph.string.strip()
            tabs = tab_number(text)
            if tabs > 0:
                fragments = re.split(r'\s*@+\s*', text)
                fragments[1] = word_role(fragments[1])
                columns = []
                if tabs >= 3:
                    speech_parts = fragments[2].split('.')
                    for index, part in enumerate(speech_parts):
                        speech_parts[index] = part_of_speech(part)
                    fragments[2] = '.'.join(speech_parts)
                    for i in range(4):
                        new_tag = soup.new_tag('th')
                        if i in [0, 1, 2]:
                            new_tag.string = fragments[i]
                        elif i == 3:
                            new_tag.string = ' '.join(fragments[3:])
                        columns.append(new_tag)
                elif tabs == 2:
                    for i in range(4):
                        new_tag = soup.new_tag('th')
                        if i == 0 or i == 1:
                            new_tag.string = fragments[i]
                        elif i == 2:
                            new_tag.string = ''
                        elif i == 3:
                            new_tag.string = fragments[2]
                        columns.append(new_tag)
                elif tabs == 1:
                    for i in range(4):
                        new_tag = soup.new_tag('th')
                        if i == 0:
                            new_tag.string = fragments[i]
                        elif i == 1 or i == 2:
                            new_tag.string = ''
                        elif i == 3:
                            new_tag.string = fragments[1]
                        columns.append(new_tag)
                paragraph.name = 'tr'
                paragraph.string.replace_with(columns[0], columns[1], columns[2], columns[3])
            else:
                # if not re.match(r'^\d+$', paragraph.string) and \
                #     not paragraph.previous_sibling.name in ['h1', 'h2']:
                    paragraph.name = 'tr'
                    new_tag = soup.new_tag('th')
                    new_tag['colspan'] = "4"
                    new_tag.string = paragraph.string
                    paragraph.string.replace_with(new_tag)
        elif paragraph.strong or paragraph.br:
            paragraph.name = 'th'
            paragraph['colspan'] = "4"
            new_tag = soup.new_tag('tr')
            paragraph.wrap(new_tag)
            

with open('output_idioms.html', 'w') as f:
    prepend = """<!DOCTYPE html>
<html>
<head>
	<style>
		table, th, td {
			border: 1px solid;
		}
		th {
			font-weight: normal;
		}
		table {
			border-collapse: collapse;
			text-align: left;
		}
	</style>
</head>
<body>
"""
    append = '''
</body>
'''
    main_text = prepend + soup.prettify().replace('@', "") + append
    f.write(main_text)