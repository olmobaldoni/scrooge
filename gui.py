import PySimpleGUI as sg
import src
from datetime import date

entry_types = ['Stipendio', 'Assegno', 'Risparmio', 'Pensione', 'Altro']

outflow_types = ['Bolletta', 'Affitto', 'Tassa', 'Alimentari', 'Salute', 'Trasporto', 'Personali', 'Altro']

table_headers = ['TIPO DI MOVIMENTO', 'CATEGORIA', 'DATA', 'IMPORTO']




def main():
    table_data = []
    sg.theme('DarkBlue3')
    layout = [
        [
            sg.T('Inserisci Saldo iniziale: ', size=(20, 1), justification='right'),
            sg.I(key='-SALDO-', size=(20, 1), do_not_clear=True)
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
            sg.CalendarButton('Scegli data',  target='-DATA_MOVIMENTO-', format='%d-%m-%Y')
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
                headings=table_headers,
                max_col_width=35,
                auto_size_columns=True,
                row_height=35,
                display_row_numbers=True,
                justification='center',
                num_rows=10,
                key='-TABLE-',
                selected_row_colors='black on yellow')
        ],
        [
            sg.Exit()
        ]
    ]

    window = sg.Window('Simple example', layout)

    while True:

        event, values = window.read()
        if event == 'Exit' or event == sg.WINDOW_CLOSED:
            break
        elif event == 'Submit':

            if values['-ENTRATA-'] != '':
                table_data.append(['ENTRATA', values['-TIPO_ENTRATA-'], values['-DATA_MOVIMENTO-'], values['-ENTRATA-']])
                window['-TABLE-'].update(values=table_data)
            elif values['-USCITA-'] != '':
                table_data.append(['USCITA', values['-TIPO_USCITA-'], values['-DATA_MOVIMENTO-'], values['-USCITA-']])
                window['-TABLE-'].update(values=table_data)

            print(values)
            print(event)
            a = src.Saldo(values['-SALDO-'])
            b = src.Entrata(values['-ENTRATA-'])
            c = src.Uscita(values['-USCITA-'])

            x = a.bilancio(b.income, c.outflow)

            window['-SALDO-'].update(x)
            window['-OUT_BILANCE-'].update(x)

            # print(a.bilancio(b.income, c.outflow))

    window.close()


if __name__ == '__main__':
    main()
