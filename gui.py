import PySimpleGUI as sg
import src
from datetime import date
import database as db

entry_types = ['Stipendio', 'Assegno', 'Risparmio', 'Pensione', 'Altro']

outflow_types = ['Bolletta', 'Affitto', 'Tassa', 'Alimentari', 'Salute', 'Trasporto', 'Personali', 'Altro']

table_headers = ['ID', 'TIPO_DI_MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']
table_headers_show = ['ID', 'TIPO DI MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']

toolbar_menu_def = [['File', ['New', 'Open', 'Delete']],
                    ['&Help', '&About...'], ]
row_menu_def = ['', ['Delete Row']]

# Database object
database_test = db.Database()
database_test.close_connection()


def create_account():
    database_test.open_connection('database_accounts.db')
    layout = [
        [
            sg.T('Account name: ')
        ],
        [
            sg.I(key='-NEW_TABLE-')
        ],
        [
            sg.Button('Add'), sg.Exit()
        ]
    ]
    window = sg.Window('Add account', layout)
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Add':
            database_test.create_table(values['-NEW_TABLE-'])
            # database_test.create_table(values['-NEW_TABLE-'], table_headers)
            sg.popup('L\'account {} è stato aggiunto!'.format(values['-NEW_TABLE-']))
            break
    window.close()
    database_test.close_connection()
    return values['-NEW_TABLE-']


def open_account():
    database_test.open_connection('database_accounts.db')
    layout = [
        [
            sg.T('Choose the account to open: ')
        ],
        [
            sg.Listbox(values=database_test.list_tables(), size=(40, 5), select_mode="single", key="-ACCOUNT-")
        ],
        [
            sg.Button('Open'), sg.Exit()
        ]
    ]
    window = sg.Window('Open Account', layout)
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Open':
            with open('account.txt', 'w') as f:
                f.write(values['-ACCOUNT-'][0])
            break
    window.close()
    database_test.close_connection()
    if values['-ACCOUNT-']:
        return values['-ACCOUNT-'][0]


def delete_account():
    database_test.open_connection('database_accounts.db')
    layout = [
        [
            sg.T('Choose the account to delete: ')
        ],
        [
            sg.Listbox(values=database_test.list_tables(), size=(40, 5), select_mode="single", key="-ACCOUNT-")
        ],
        [
            sg.Button('Delete'), sg.Exit()
        ]
    ]
    window = sg.Window('Delete Account', layout)
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Delete':
            database_test.delete_table(values['-ACCOUNT-'][0])
            sg.popup('L\'account {} è stato eliminato!'.format(values['-ACCOUNT-'][0]))
            break
    window.close()
    database_test.close_connection()


def delete_table_row(window, table_name, data):
    row_number = data['-TABLE-'][0]
    temp_data = window['-TABLE-'].get()
    row_id = temp_data[row_number][0]
    database_test.open_connection('database_accounts.db')
    database_test.delete_row(table_name, row_id)
    database_test.close_connection()
    sg.popup('La riga con ID = {} è stata eliminata!'.format(row_id))


def main():
    try:
        with open('account.txt', 'r') as f:
            name_account = f.read()
    except FileNotFoundError as e:
        name_account = create_account()
        with open('account.txt', 'x') as f:
            f.write(name_account)
    finally:
        database_test.open_connection('database_accounts.db')
        table_data = database_test.get(name_account, table_headers)
        database_test.close_connection()

    sg.theme('DarkBlue3')

    layout = [
        [
            sg.Menu(toolbar_menu_def, tearoff=False, pad=(200, 1))
        ],
        [
            sg.T('Account: '), sg.T(name_account, key='-ACTUAL_ACCOUNT-', size=(20, 1), justification='left')
        ],
        [
            sg.Radio('Entrata', 'RADIO', key='-MOVIMENTO_ENTRATA-'),
            sg.Radio('Uscita', 'RADIO', key='-MOVIMENTO_USCITA-')
        ],
        [
            sg.T('Aggiungi Entrata: ', size=(20, 1), justification='right'),
            sg.Combo(entry_types, key='-TIPO_ENTRATA-', readonly=True, enable_events=False, size=(20, 1)),
            sg.I(key='-ENTRATA-', size=(20, 1), do_not_clear=False)
        ],
        [
            sg.T('Aggiungi Uscita: ', size=(20, 1), justification='right'),
            sg.Combo(outflow_types, key='-TIPO_USCITA-', readonly=True, enable_events=False, size=(20, 1)),
            sg.I(key='-USCITA-', size=(20, 1), do_not_clear=False)
        ],
        [
            sg.T('Data movimento: ', size=(20, 1), justification='right'),
            sg.I(key='-DATA_MOVIMENTO-', size=(20, 1), default_text=date.today().strftime('%d-%m-%Y')),
            sg.CalendarButton('Scegli data', target='-DATA_MOVIMENTO-', format='%d-%m-%Y', enable_events=False)
        ],
        [
            sg.Submit()
        ],
        [
            sg.Table(
                values=table_data,
                headings=table_headers_show,
                max_col_width=35,
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
            sg.Exit()
        ]
    ]

    window = sg.Window('Scrooge', layout)

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

            # a = src.Saldo(values['-SALDO-'])
            # b = src.Entrata(values['-ENTRATA-'])
            # c = src.Uscita(values['-USCITA-'])
            #
            # x = a.bilancio(b.income, c.outflow)
            #
            # window['-SALDO-'].update(x)
            # window['-OUT_BILANCE-'].update(x)

        elif event == 'New':
            create_account()
        elif event == 'Open':
            name_account = open_account()
            if name_account:
                window['-ACTUAL_ACCOUNT-'].update(name_account)
                database_test.open_connection('database_accounts.db')
                table_data = database_test.get(name_account, table_headers)
                database_test.close_connection()
                window['-TABLE-'].update(values=table_data)
        elif event == 'Delete':
            delete_account()
            database_test.open_connection('database_accounts.db')
            if not database_test.list_tables():
                name_account = create_account()
                with open('account.txt', 'w') as f:
                    f.write(name_account)
                window['-ACTUAL_ACCOUNT-'].update(name_account)
                # non ci va messo close_connection perché quando chiamo create_account la connessione viene automaticamente chiusa dentro la funzione
                # database_test.close_connection()
                database_test.open_connection('database_accounts.db')
                table_data = database_test.get(name_account, table_headers)
                database_test.close_connection()
                window['-TABLE-'].update(values=table_data)
        elif event == 'Delete Row':
            delete_table_row(window, name_account, values)
            database_test.open_connection('database_accounts.db')
            table_data = database_test.get(name_account, table_headers)
            database_test.close_connection()
            window['-TABLE-'].update(values=table_data)
        elif event == 'About...':
            sg.popup_no_titlebar('Scrooge\nVersion:     1.0.0\nAuthor:     Olmo Baldoni')
    window.close()


if __name__ == '__main__':
    main()
