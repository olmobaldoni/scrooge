import PySimpleGUI as sg
import src
from datetime import date
import database as db

entry_types = ['Stipendio', 'Assegno', 'Risparmio', 'Pensione', 'Altro']

outflow_types = ['Bolletta', 'Affitto', 'Tassa', 'Alimentari', 'Salute', 'Trasporto', 'Personali', 'Altro']

table_headers = ['TIPO_DI_MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']
table_headers_show = ['TIPO DI MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']


# Creo la parte di database con una tabella di prova chiamata OLMO e poi chiudo la connessione

database_test = db.Database('database_accounts.db')
database_test.create_table('OLMO', table_headers)
database_test.close_connection()

















menu_def = [['File', ['New', 'Open', 'Delete']],
            ['&Help', '&About...'], ]

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
        print(values['-NEW_TABLE-'])
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Add':
            database_test.create_table(values['-NEW_TABLE-'], table_headers)
            sg.popup('L\'account {} è stato aggiunto!'.format(values['-NEW_TABLE-']))
            break
    window.close()
    database_test.close_connection()

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

    window.close()


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



def main():



    # questa parte serve per recuperare i dati dalla tabella e mostrarla direttamente sull'interfaccia
    # devo riscire ad 'aprire' la tabella dell'ultimo account aperto
    database_test.open_connection('database_accounts.db')
    table_data = database_test.get('OLMO', table_headers)
    database_test.close_connection()

    sg.theme('DarkBlue3')

    layout = [
        [
            sg.Menu(menu_def, tearoff=False, pad=(200, 1))
        ],
        [
            sg.T('Account: '), sg.T(key='-ACTUAL_ACCOUNT-', size=(20, 1), justification='left')
        ],
        [
            sg.T('Inserisci Saldo iniziale: ', size=(20, 1), justification='right'),
            sg.I(key='-SALDO-', size=(20, 1), do_not_clear=True)
        ],
        [
            sg.Radio('Entrata', 'RADIO', key='-MOVIMENTO_ENTRATA-'), sg.Radio('Uscita', 'RADIO', key='-MOVIMENTO_USCITA-')
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
            sg.I(key='-DATA_MOVIMENTO-', size=(20,1), default_text=date.today().strftime('%d-%m-%Y')),
            sg.CalendarButton('Scegli data',  target='-DATA_MOVIMENTO-', format='%d-%m-%Y', enable_events=False)
        ],
        [
            sg.T('Il tuo saldo attuale è di: ', size=(20, 1), justification='right'),
            sg.T(key='-OUT_BILANCE-', size=(20, 1), justification='left')
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
                display_row_numbers=True,
                justification='center',
                num_rows=10,
                key='-TABLE-',
                # alternating_row_color='orange',
                selected_row_colors='black on yellow'),
        ],
        [
            sg.Exit()
        ]
    ]

    window = sg.Window('Scrooge', layout)

    while True:
        event, values = window.read()
        window['-TABLE-'].update(values=database_test.get('OLMO', table_headers))


        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':
            if values['-ENTRATA-'] != '' and values['-MOVIMENTO_ENTRATA-']:
                database_test.open_connection('database_accounts.db')
                database_test.write('OLMO', values)
                window['-TABLE-'].update(values=database_test.get('OLMO', table_headers))
                database_test.close_connection()

            a = src.Saldo(values['-SALDO-'])
            b = src.Entrata(values['-ENTRATA-'])
            c = src.Uscita(values['-USCITA-'])

            x = a.bilancio(b.income, c.outflow)

            window['-SALDO-'].update(x)
            window['-OUT_BILANCE-'].update(x)
        elif event == 'New':
            create_account()
        elif event == 'Open':
            open_account()
        elif event == 'Delete':
            delete_account()

    window.close()


if __name__ == '__main__':
    main()
