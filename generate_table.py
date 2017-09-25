import json
import urllib
from BeautifulSoup import BeautifulSoup

def get_description(name):
    name = name.replace('sys_', '')
    c = urllib.urlopen('http://man7.org/linux/man-pages/man2/' + name + '.2.html').read()
    soup = BeautifulSoup(c)
    try:
        p1 = soup('pre')[1].string
        p2 = p1.replace('<pre>', '')
        return p2.replace('</pre>', '').split('-')[1].strip()
    except:
        return ''

def get_definition_dom(filename, lineno):
    url = 'http://lxr.free-electrons.com/source/' + filename + '#L' + str(lineno)
    visible = filename + ':' + str(lineno)
    return '<a href="' + url + '">' + visible + '</a>'

def get_hyperlinked_name(name):
    url = 'http://man7.org/linux/man-pages/man2/' + name + '.2.html'
    return '<a href="' + url + '">' + name + '</a>'

def generate_html(syscalls):
    print '<html>'
    print '<head>'
    print '  <meta charset="utf-8">'
    print '  <meta name="viewport" content="width=device-width, initial-scale=1">'
    print '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
    print '  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>'
    print '  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'
    print '  <style>'
    print '    body {'
    print '      font-family: "Roboto",Corbel,Avenir,"Lucida Grande","Lucida Sans",sans-serif!important;'
    print '      line-height: 1.2;'
    print '      color: #3e4349;'
    print '      font-size: 13px;'
    print '      text-align: justify;'
    print '    }'
    print '  </style>'
    print '</head>'
    print '<body>'
    print '<h2>Linux System Call Table</h2>'
    print '<p>Code hosted at https://github.com/thevivekpandey/syscalls-table-64bit</p>'
    print '<div class="container">'
    print '<table class="table table-striped">'
    print '<tr>'
    print '<th>S.No.</th>'
    print '<th>Name</th>'
    print '<th>Description</th>'
    print '<th colspan=6> Registers</th>'
    print '<th>Definition</th>'
    print '</tr>'
    print '<tr>'
    print '<td></td>'
    print '<td></td>'
    print '<td></td>'
    print '<td>eax</td>'
    print '<td>ebx</td>'
    print '<td>ecx</td>'
    print '<td>edx</td>'
    print '<td>esi</td>'
    print '<td>edi</td>'
    print '<td></td>'
    print '</tr>'
    for idx, syscall in enumerate(syscalls):
        desc = get_description(syscall[1])
        print '<tr>'
        print '<td> ' + str(idx + 1) + '</td>'
        print '<td> ' + get_hyperlinked_name(syscall[1].replace('sys_', '')) + '</td>' 
        print '<td> ' + desc.encode('utf-8') + '</td>' 
        print '<td>0x{:02x}</td>'.format(idx)
        args = syscall[2].replace('(', '').replace(')', '').split(',')
        print '<td>' + (args[1] if len(args) > 1 else '') + '</td>'
        print '<td>' + (args[2] if len(args) > 2 else '') + '</td>'
        print '<td>' + (args[3] if len(args) > 3 else '') + '</td>'
        print '<td>' + (args[4] if len(args) > 4 else '') + '</td>'
        print '<td>' + (args[5] if len(args) > 5 else '') + '</td>'
        print '<td>' + get_definition_dom(syscall[9], syscall[10]) + '</td>'
        print '</tr>'
       
    print '</table>'
    print '</div>'
    print '</body>'
    print '</html>'

def get_data():
    f = open('www/syscalls-x86_64.js')
    syscalls = json.loads(f.read())
    data = []
    for idx, syscall in enumerate(syscalls['aaData']):
        name = syscall[1]
        if name != '' and name != 'not implemented':
            data.append(syscall)
    f.close()
    return data

if __name__ == '__main__':
    data = get_data()
    generate_html(data)
