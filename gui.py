import PySimpleGUI as sg
from datetime import date
import database as db
from matplotlib.figure import Figure
import account as acc

'''
 ######   ######  ########   #######   #######   ######   ######## 
##    ## ##    ## ##     ## ##     ## ##     ## ##    ##  ##       
##       ##       ##     ## ##     ## ##     ## ##        ##       
 ######  ##       ########  ##     ## ##     ## ##   #### ######   
      ## ##       ##   ##   ##     ## ##     ## ##    ##  ##       
##    ## ##    ## ##    ##  ##     ## ##     ## ##    ##  ##       
 ######   ######  ##     ##  #######   #######   ######   ########
'''

entry_types = ['Stipendio', 'Assegno', 'Risparmio', 'Pensione', 'Altro']
outflow_types = ['Bolletta', 'Affitto', 'Tassa', 'Alimentari', 'Salute', 'Trasporto', 'Personali', 'Altro']

# for databases
table_headers = ['ID', 'TIPO_DI_MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']

# for left table
table_headers_show = ['ID', 'TIPO DI MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']

# for right table
header_list = ['DATA', 'IMPORTO']

# main toolbar
toolbar_menu_def = [['File', ['New', 'Open', 'Delete']],
                    ['&Help', '&About...'], ]

# toolbar for deleting entries
row_menu_def = ['', ['Delete Row']]

# list for right table
data = []

# database object
database_test = db.Database()
database_test.close_connection()

# account object
account_test = acc.Account()

# font
font = 'Segoe 12 bold'


def main():

    # if there are no accounts, one is created. Otherwise, the last active account is reopened
    try:
        with open('account.txt', 'r') as f:
            name_account = f.read()
    except FileNotFoundError as e:
        name_account = account_test.create_account()
        with open('account.txt', 'x') as f:
            f.write(name_account)
    finally:
        database_test.open_connection('database_accounts.db')
        table_data = database_test.get(name_account, table_headers)
        database_test.close_connection()

    sg.theme('DarkBlue3')

    # left layout
    left_column = sg.Column([
        [
            sg.Menu(toolbar_menu_def, tearoff=False, pad=(200, 1), font=font)
        ],
        [
            sg.T('Account: ', font=font), sg.T(name_account, key='-ACTUAL_ACCOUNT-', size=(20, 1), justification='left', font=font)
        ],
        [
            sg.Radio('Entrata', 'RADIO', key='-MOVIMENTO_ENTRATA-', font=font),
            sg.Radio('Uscita', 'RADIO', key='-MOVIMENTO_USCITA-', font=font)
        ],
        [
            sg.T('Aggiungi Entrata: ', size=(20, 1), justification='right', font=font),
            sg.Combo(entry_types, key='-TIPO_ENTRATA-', readonly=True, enable_events=False, size=(20, 1), font=font),
            sg.I(key='-ENTRATA-', size=(20, 1), do_not_clear=False, font=font)
        ],
        [
            sg.T('Aggiungi Uscita: ', size=(20, 1), justification='right', font=font),
            sg.Combo(outflow_types, key='-TIPO_USCITA-', readonly=True, enable_events=False, size=(20, 1), font=font),
            sg.I(key='-USCITA-', size=(20, 1), do_not_clear=False, font=font)
        ],
        [
            sg.T('Data movimento: ', size=(20, 1), justification='right', font=font),
            sg.I(key='-DATA_MOVIMENTO-', size=(20, 1), default_text=date.today().strftime('%d-%m-%Y'), font=font),
            sg.CalendarButton('Scegli data', target='-DATA_MOVIMENTO-', format='%d-%m-%Y', enable_events=False, font=font)
        ],
        [
            sg.Submit(font=font)
        ],
        [
            sg.Table(
                values=table_data,
                headings=table_headers_show,
                font=font,
                max_col_width=45,
                auto_size_columns=True,
                row_height=35,
                display_row_numbers=False,
                right_click_selects=True,
                right_click_menu=row_menu_def,
                justification='center',
                num_rows=10,
                key='-TABLE-',
                selected_row_colors='black on yellow'),
        ],
        [
            sg.Exit(font=font)
        ]
    ])

    # right layout
    tab_layout_1 = [
        [sg.Canvas(key='-CANVAS_CONTROL_1-')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='-CANVAS_FIGURE_1-',
                           # it's important that you set this size
                           # size=(470, 392)
                           size=(650, 450)
                           )]
            ],
            background_color='#DAE0E6',
            pad=(0, 0)
        )],
        [
            sg.Table(values=data,
                     headings=header_list,
                     display_row_numbers=True,
                     auto_size_columns=False,
                     num_rows=5,
                     def_col_width=25,
                     key='-TABLE_1-',
                     font=font)
        ],
        [
            sg.SaveAs(button_text='Save As Excel File', file_types=(('Excel Files', '*.xlsx'),),
                      key='-SAVE_BUTTON_MONTH-',
                      enable_events=True, font=font)
        ]
    ]

    tab_layout_2 = [
        [sg.Canvas(key='-CANVAS_CONTROL_2-')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='-CANVAS_FIGURE_2-',
                           size=(650, 450)
                           )]
            ],
            background_color='#DAE0E6',
            pad=(0, 0)
        )],
        [
            sg.Table(values=data,
                     headings=header_list,
                     display_row_numbers=True,
                     auto_size_columns=False,
                     num_rows=5,
                     def_col_width=25,
                     key='-TABLE_2-',
                     font=font)
        ],
        [
            sg.SaveAs(button_text='Save As Excel File', file_types=(('Excel Files', '*.xlsx'),),
                      key='-SAVE_BUTTON_YEAR-',
                      enable_events=True, font=font)
        ]
    ]

    right_column = sg.Column([
        [
            sg.Radio('Entrata', 'group_2', enable_events=True, key='-RADIO_ENTRATA_2-', font=font),
            sg.Radio('Uscita', 'group_2', enable_events=True, key='-RADIO_USCITA_2-',font=font)
        ],
        [
            sg.Column([
                [
                    sg.T('Choose entry category:      ', size=(20, 1), font=font)
                ],
                [
                    sg.Combo(entry_types, key='-TIPO_ENTRATA_2-', readonly=True, enable_events=False, size=(20, 1), font=font)
                ]
            ], pad=(0, 0), key='FRAME_1', visible=False, metadata=False),
            sg.Column([
                [
                    sg.T('Choose output category:      ', size=(20, 1), font=font)
                ],
                [
                    sg.Combo(outflow_types, key='-TIPO_USCITA_2-', readonly=True, enable_events=False, size=(20, 1), font=font)
                ]
            ], pad=(0, 0), key='FRAME_2', visible=False, metadata=False)
        ],
        [
            sg.Button('Analyse', key='-ANALYSE-', font=font)
        ],
        [
            sg.TabGroup([[
                sg.Tab('Mese', tab_layout_1), sg.Tab('Anno', tab_layout_2)
            ]], font=font)
        ]
    ])

    # window layout
    layout = [
        [
            left_column, sg.VerticalSeparator(), right_column
        ]
    ]

    # gui icon
    icon = b'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28DFdUuT94DLHaD/SZcMyZH8NIVCAXg/o2/KAX23QNeq21tzH6cPQIa6WroBDg6B0SJlr3m8O9je279nmv39AGj7cqN/A62wAAANGGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDo4MDRhZWMwZS0zYjQ3LTRmMmYtOGZkNy1jMWRhOWM1MDViMzQiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6YjBmZmVkMWItNDA2Yy00MWI2LWI5M2QtMTgwYzRjMjg0MTY4IgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6NDU3ZjA0NjUtZGI3OC00YmUzLWI4OTQtN2NkMTU1NTBjODQ2IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NjE1ODU3NDYyODIxOTciCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zMCIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo2YWFjMTMxMi1jNDYxLTQ1YmUtYTgwMy1mZjQ4NDczMThjMTciCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMDgtMjdUMDk6MzU6NDYiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+3Dv8SAAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+YIGwcjLtyRpUsAACAASURBVHja7Z15fFPF+v/fSdMl6b5QoFBa1rYUCkUKCC07BRFkqYrgAiKrCKKI14uiX/erXrkuV6/bVX969YKIiCjIviOUtZWy74WWpQt035L8/kj0AjknTdqkSZp5v155Uc7MOSdn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'    ####################################################################################################################

    # main window
    window = sg.Window('Scrooge', layout, resizable=True, element_justification='c', icon=icon, finalize=True, font=font)

    # change the colour of the entrances depending on the type of movement
    account_test.change_row_color(window)

    # show blank figures at start-up
    fig = Figure(figsize=(6.3, 4.3))
    account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_1-'].TKCanvas, fig, window['-CANVAS_CONTROL_1-'].TKCanvas)
    account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_2-'].TKCanvas, fig, window['-CANVAS_CONTROL_2-'].TKCanvas)

    # event loop
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':
            if (values['-ENTRATA-'] != '' and values['-MOVIMENTO_ENTRATA-']) or (
                    values['-USCITA-'] != '' and values['-MOVIMENTO_USCITA-']):
                database_test.open_connection('database_accounts.db')
                database_test.write(name_account, values)
                window['-TABLE-'].update(values=database_test.get(name_account, table_headers))
                database_test.close_connection()
                account_test.change_row_color(window)
        elif event == 'New':
            # create a new account
            account_test.create_account()
        elif event == 'Open':
            name_account = account_test.open_account(window)
            if name_account and name_account != window['-ACTUAL_ACCOUNT-'].get():
                window['-ACTUAL_ACCOUNT-'].update(name_account)
                database_test.open_connection('database_accounts.db')
                table_data = database_test.get(name_account, table_headers)
                database_test.close_connection()
                window['-TABLE-'].update(values=table_data)
                account_test.change_row_color(window)

                # show empty figures when changing accounts
                fig = Figure(figsize=(6.3, 4.3))
                account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_1-'].TKCanvas, fig, window['-CANVAS_CONTROL_1-'].TKCanvas)
                account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_2-'].TKCanvas, fig, window['-CANVAS_CONTROL_2-'].TKCanvas)
                window['-TABLE_1-'].update(values=data)
                window['-TABLE_2-'].update(values=data)

        elif event == 'Delete':
            deleted_account = account_test.delete_account()
            if window['-ACTUAL_ACCOUNT-'].get() == deleted_account:
                database_test.open_connection('database_accounts.db')
                if database_test.list_tables():
                    name_account = database_test.list_tables()[0]
                    with open('account.txt', 'w') as f:
                        f.write(name_account)
                    window['-ACTUAL_ACCOUNT-'].update(name_account)
                    table_data = database_test.get(name_account, table_headers)
                    window['-TABLE-'].update(values=table_data)
                    account_test.change_row_color(window)
                else:
                    name_account = account_test.create_account()
                    with open('account.txt', 'w') as f:
                        f.write(name_account)
                    window['-ACTUAL_ACCOUNT-'].update(name_account)
                    database_test.open_connection('database_accounts.db')
                    table_data = database_test.get(name_account, table_headers)
                    window['-TABLE-'].update(values=table_data)
                database_test.close_connection()
                account_test.change_row_color(window)
                fig = Figure(figsize=(6.3, 4.3))
                account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_1-'].TKCanvas, fig, window['-CANVAS_CONTROL_1-'].TKCanvas)
                account_test.draw_figure_w_toolbar(window['-CANVAS_FIGURE_2-'].TKCanvas, fig, window['-CANVAS_CONTROL_2-'].TKCanvas)
                window['-TABLE_1-'].update(values=data)
                window['-TABLE_2-'].update(values=data)

        elif event == 'Delete Row':
            account_test.delete_table_row(window, name_account, values)
            database_test.open_connection('database_accounts.db')
            table_data = database_test.get(name_account, table_headers)
            database_test.close_connection()
            window['-TABLE-'].update(values=table_data)
            account_test.change_row_color(window)

        elif event == '-RADIO_ENTRATA_2-':
            visible = not window['FRAME_1'].metadata
            window['FRAME_1'].update(visible=visible)
            window['FRAME_1'].metadata = visible
            if window['FRAME_2'].metadata:
                visible = False
                window['FRAME_2'].update(visible=visible)
                window['FRAME_2'].metadata = visible

        elif event == '-RADIO_USCITA_2-':
            visible = not window['FRAME_2'].metadata
            window['FRAME_2'].update(visible=visible)
            window['FRAME_2'].metadata = visible
            if window['FRAME_1'].metadata:
                visible = False
                window['FRAME_1'].update(visible=visible)
                window['FRAME_1'].metadata = visible

        elif event == '-ANALYSE-' and (values['-RADIO_ENTRATA_2-'] or values['-RADIO_USCITA_2-']):
            month_df, year_df = account_test.analyse_data(name_account, values, window)

        elif event == '-SAVE_BUTTON_MONTH-' or event == '-SAVE_BUTTON_YEAR-':
            account_test.save_data_as_excel(values, month_df, year_df)

        elif event == 'About...':
            sg.popup_no_titlebar('Scrooge\nVersion:     1.0.0\nAuthor:     Olmo Baldoni', image=icon, font=font)
    window.close()


if __name__ == '__main__':
    main()
