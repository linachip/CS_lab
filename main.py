from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
import json

main = Tk()
main.title('Laboratory work #1')
main.geometry('1000x600')
main.configure(bg='#5d5fef')
font = Font(family="Raleway", size=12)

global selected
selected = False

#function to create new file
def newFile():
    my_text.delete('1.0', END)

    main.title('New File')
    status_bar.config(text='New File       ')


def findAll(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


#function to open file
def openFile():
    my_text.delete('1.0', END)

    text_file = filedialog.askopenfilename(
        initialdir='lab1/audit/',
        title='Open File', filetypes=(('All Files', '*.*'),))


    name = text_file
    status_bar.config(text=f'{name}       ')
    name = name.replace('lab1/', '')
    main.title(f'{name}')

    text_file = open(text_file, 'r')
    contents = text_file.read()

    contents = contents.replace('            :', ':')
    contents = contents.replace('           :', ':')
    contents = contents.replace('          :', ':')
    contents = contents.replace('         :', ':')
    contents = contents.replace('        :', ':')
    contents = contents.replace('       :', ':')
    contents = contents.replace('      :', ':')
    contents = contents.replace('     :', ':')
    contents = contents.replace('    :', ':')
    contents = contents.replace('   :', ':')
    contents = contents.replace('  :', ':')
    contents = contents.replace(' :', ':')

    start = list(findAll(contents, '<custom_item>'))
    ending = list(findAll(contents, '</custom_item>'))

    custom_item = {}

    custom_item['REGISTRY_SETTING'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [],
                                       'reg_item': [], 'reg_option': [], 'info': []}
    custom_item['AUDIT_POWERSHELL'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                       'powershell_args': [],
                                       'only_show_cmd_output': [], 'check_type': [], 'severity': [], 'appcmd_list': [],
                                       'appcmd_filter': [], 'appcmd_filter_value': []}
    custom_item['PASSWORD_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                      'check_type': [],
                                      'password_policy': []}
    custom_item['LOCKOUT_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                     'check_type': [],
                                     'lockout_policy': []}
    custom_item['USER_RIGHTS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                         'check_type': [],
                                         'right_type': []}
    custom_item['CHECK_ACCOUNT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [],
                                    'account_type': []}
    custom_item['BANNER_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [],
                                   'reg_item': [], 'is_substring': []}
    custom_item['AUDIT_POLICY_SUBCATEGORY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                               'check_type': [],
                                               'audit_policy_policy': []}
    custom_item['REG_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                'reg_key': [], 'reg_item': [], 'key_item': []}
    custom_item['ANONYMOUS_SID_SETTING'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [],
                                            'check_type': []}

    general_custom_item = {}
    general_custom_item_keys = []

    for key in custom_item:
        keys_list = list(custom_item[key])
        for key_x in keys_list:
            if key_x not in general_custom_item_keys:
                general_custom_item_keys.append(key_x)
    for key in general_custom_item_keys:
        general_custom_item[key] = []

    for i in range(len(start)):
        content_type_block = contents[start[i] + 13: ending[i]]
        for element in list(general_custom_item.keys()):
            element_length = len(element) + 1
            if content_type_block.find(element) != -1:
                general_custom_item[element].append(content_type_block[content_type_block.find(
                    element + ':') + element_length: content_type_block[
                                                     content_type_block.find(element + ':') + element_length:].find(
                    '\n') + content_type_block.find(element + ':') + element_length].strip())
            else:
                general_custom_item[element].append('')

    to_json = []
    for i in range(len(general_custom_item['type'])):
        to_print = {}
        for element in list(general_custom_item.keys()):
            if general_custom_item[element][i] != '':
                to_print[element] = general_custom_item[element][i]
        to_json.append(to_print)

    my_text.insert(END, json.dumps(to_json, indent=4))

    text_file.close()


#function to save as file
def saveAs():
    text_file = filedialog.asksaveasfilename(
        defaultextension='.*',
        initialdir='lab1/audit/',
        title='Save File', filetypes=(('All Files', '*.*'),))
    if text_file:
        name = text_file
        status_bar.config(text=f'{name}       ')
        name = name.replace('lab1/audit/', '')
        main.title(f'{name}')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # close file
        text_file.close()


#main frame
my_frame = Frame(main)
my_frame.pack(pady=5)

#scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

horizontal_scroll = Scrollbar(my_frame, orient='horizontal')
horizontal_scroll.pack(side=BOTTOM, fill=X)

#text
my_text = Text(my_frame, width=80, height=25, font=font,
               undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=horizontal_scroll.set)
my_text.pack()

text_scroll.config(command=my_text.yview)
horizontal_scroll.config(command=my_text.xview)

#menu
my_menu = Menu(main)
main.config(menu=my_menu)

file_menu = Menu (my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=newFile)
file_menu.add_command(label='Open', command=openFile)
file_menu.add_command(label='Save As', command=saveAs)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=main.quit)


status_bar = Label(main, text='Start     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=10)

main.mainloop()