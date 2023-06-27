import re
import sys
import clipboard


def clean(text):

    # remove trailing tabs at the end of line
    find = r'[\t ]+\n'
    replace = r'\n'
    text = re.sub(find, replace, text)

    # remove space+tab with tab:
    find = r'( +\t|\t +)'
    replace = r'\t'
    text = re.sub(find, replace, text)

    # remove 6+ tabs with space:
    find = r'\t{6,}'
    replace = r' '
    text = re.sub(find, replace, text)

    # remove the single tab in the middle of line:
    find = r'^([^\t\n]*)\t+([^\n\t]*\n\n)'
    replace = r'\1 \2'
    text = re.sub(find, replace, text, flags=re.MULTILINE)
    
    # remove excessive spaces
    find = r' +'
    replace = ' '
    text = re.sub(find, replace, text)

    # remove tab comma with comma only
    find = r'\s+,'
    replace = ','
    text = re.sub(find, replace, text)


    # remove all excessive tabs between word and pos:
    pos = r'(adj|c|card|n|v|V|ind|pp|prp|idiom|pm|ptp|pn|pr|pr\.|pt\.|v\. ?refl|pn+ind)'
    find = r'^([^\t\n]+)[\t ]+' + pos+ r'(.*\t.*)$'
    replace = r'\1{onetab}\2\3'
    text = re.sub(find, replace, text, flags=re.MULTILINE)

    # replace 2+ tabs with 2 tabs when they are after pos and there's no grammar
    find = pos + r'\t{2,}([^\t\n]*)$'
    replace = r'\1{twotabs}\2'
    text = re.sub(find, replace, text, flags=re.MULTILINE)

    # remove 2+ tabs after grammar
    grammar = r'(?:f\.|ac\.|s\.|voc\.|nt|neg|pr\.|-\.|x\.|pl|per\.|irr\.|dat|reflex\.|\/|ins\.|imperf\.|refl\.|adv|aor\.|dat\.|imp\.|loc|perf\.|inf|abl\.|abs|fut\.|m|m\.|conj|n\.|nt\.|gen\.|loc\.|opt\.|ac\.|3\.|2\.|1\.){1,}s?'
    # grammar = r'(?:f|1|2|3|-|abl|abs|ac|acc|adv|aor|conj|dat|dat|fut|gen|ger|imp|Imp|imperf|inf|ins|inter|interrog|irr|loc|l|m|n|neg|nom|nt|opt|p|per|perf|pl|pr|refl|reflex|s|voc|x|\.|\,){1,}s?'
    find = r'(\t' + grammar + r')\t\t+([^\t\n]+)$'
    replace = r'\1\t\2'
    text = re.sub(find, replace, text, flags=re.MULTILINE)

    # remove 2+ tabs between pos and grammar
    find = r'\t{2,}(' + grammar + r')'
    replace = r'\t\1'
    text = re.sub(find, replace, text, flags=re.MULTILINE)

    text = text.replace('{twotabs}', '\t\t')
    text = text.replace('{onetab}', '\t')

    return(text)


if __name__ == '__main__':
    # text = clipboard.paste()
    # print(text)
    # print('---------------')
    # print(clean(text))
    with open('BD ex book 3.txt') as f:
        text = f.read()
    cleaned_text = clean(text)
    with open('cleaned_text.txt', 'w') as f:
        f.write(cleaned_text)
    clipboard.copy(cleaned_text)