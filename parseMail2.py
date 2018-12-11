import os
import mailbox
import re
from bs4 import BeautifulSoup
from email.header import Header
from email.header import decode_header


mailHeaders = ['geriLaiskai', 'reklama']
directory = './Takeout/Mail/'
pavadinimas = 'Mail_3U'

dictionary = {
    #'htmlFontTags':'numeric',
    'textWordCount':'numeric',
    'letterWordCountText':'numeric',
    'htmlLinks':'numeric',
    'htmlImages':'numeric',
    'htmlTags':'numeric',
    'textLinks':'numeric',
    'receiverCount':'numeric',
    'whiteSpaceChars':'numeric',
    'nonStandardChars':'numeric',
    'textLength':'numeric',
    'imageParts':'numeric',
    'plainTextParts':'numeric',
    'htmlParts':'numeric',
    'nonStandardParts': 'numeric',
    'parts':'numeric',
    'class':",".join(mailHeaders)
    }
data = dict.fromkeys([d for d in dictionary])

WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

#PATAISYTI
def getHeaderStr(header):
    default_charset = 'ASCII'
    #if isinstance(header, Header):
        #print(''.join([ unicode(t[0], t[1] or default_charset) for t in decode_header(header)]))

def constructArffHeaders(f, dictionary):
    f.write('@relation \'' + pavadinimas + '\'\n\n')
    for d in dictionary:
        f.write('@attribute ' + d + ' ')
        if dictionary[d] == 'numeric':
            f.write('numeric')
        elif ',' in dictionary[d]:
            f.write('{' + dictionary[d] + '}')
        f.write('\n')
    f.write('\n@data\n\n')
    
def writeData(f, data, dictionary):
    f.write(','.join(str(data[d]) for d in data))
    f.write('\n')

def clearData(data):
    for key in data:
        if dictionary[key] == 'numeric':
            data[key] = 0.0
        elif "," in dictionary[key]:
            data[key] = dictionary[key].split(',')[0]

def parseMessage(message, data):
    clearData(data)
    data['receiverCount'] = float(len(message['To'].split(',')))
    getHeaderStr(message['subject'])
    #print(message['subject'], type(message['subject']))
    #print(re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", message['subject']))
    for label in message['X-Gmail-Labels'].split(','):
        if label in mailHeaders:
            data['class'] = label
            print(label)
    for part in message.walk():
        text = ''
        if part.get_content_type() == 'text/plain':
            text = part.get_payload()
            #text = quopri.decodestring(part.get_payload(decode=True))
            data['plainTextParts'] += 1
        elif part.get_content_type() == 'text/html':
            soup = BeautifulSoup(part.get_payload(), 'html.parser')
            text = soup.get_text()
            #print(text)     <----- PAZIURETI
            data['htmlTags'] = len(soup.findAll())
            data['htmlImages'] = len(soup.findAll('img'))
            data['htmlLinks'] = len(soup.findAll('a'))
            #data['htmlFontTags'] = len(soup.findAll('font'))
            data['htmlParts'] += 1
        elif part.get_content_maintype() != 'multipart':
            data['nonStandardParts'] += 1
        if text != '':
            data['textLength'] += len(text)
            data['textWordCount'] += len(text.split())
            data['nonStandardChars']+= len(re.sub('[\w\s]+','', text))
            data['whiteSpaceChars']+= len(re.sub('[\S]+', '', text))
            data['textLinks']+= len(re.findall(WEB_URL_REGEX, text))
            data['letterWordCountText']+= len(''.join((c if c.isalpha() else ' ') for c in text).split())
        if part.get_content_maintype() == 'image':
            data['imageParts'] += 1
        data['parts'] += 1
    #print(data[next(iter(data))], next(iter(data)))
    return data

stop = 500

with open('laiskai.arff', 'w') as outfile:
    constructArffHeaders(outfile, dictionary)
    for f in os.listdir(directory):
        if re.compile("^(.+)\.mbox$").search(f).group(1) in mailHeaders:
            mbox = mailbox.mbox(directory+f)
            i = 0
            for m in mbox:
                parseMessage(m, data)
                writeData(outfile, data, dictionary)
                #print(m.get_payload())
                #print(m['from'])
                i += 1
                if i > stop:
                    break
