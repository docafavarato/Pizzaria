import PySimpleGUI as sg
import pandas as pd
from time import sleep
import random
from pycep_correios import get_address_from_cep, WebService, exceptions
import pyodbc

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-3PKKPL3\SQLEXPRESS;"
    "Database=PythonSQL;"
)

conexao = pyodbc.connect(dados_conexao)
print("Conexão Bem Sucedida")

cursor = conexao.cursor()

lista = []

frases = ['Existimos desde X.',
          'Nossa pizzaria foi premiada como a melhor de X.',
          'Você sabia que nós possuímos mais de X sabores de pizza?',
          'Realizamos entregas em toda a região.',
          'Temos forno à lenha.',
          'Nossa pizza especial leva um molho secreto.',
          'Somos a pizzaria mais antiga da região']

layoutPizza = [
    [sg.Listbox(values=['Queijo', 'Calabresa', 'Portuguesa', 'Toscana', 'Marguerita', 'Brigadeiro', 'Especial'], size=(20, 6)), sg.Listbox(['Pequena', 'Média', 'Grande'], size=(10, 3))],
    [sg.Slider(orientation='horizontal'), sg.Button('Salvar', key='salvar', border_width=1)]
]

layoutEnvio = [
    [sg.Text('Cupom: '), sg.InputText(size=(25,10)), sg.Text(' '*1), sg.Button('Verificar', key='cupomBotao')],
    [sg.Text('CEP: '), sg.Text(' '*4), sg.InputText(size=(25,10)), sg.Button('Verificar', key='verificar')],
    [sg.Text('Endereço: '), sg.InputText(key='endereço', size=(25,10))],
    [sg.Text('Bairro: '), sg.Text(' '*2), sg.InputText(key='bairro', size=(25,10))]
]

layout = [
  [sg.Frame('Sabores', layout=layoutPizza, ), sg.Frame('Envio', layout=layoutEnvio, size=(350, 150))],
  [sg.Button('Concluir Pedido', key='pedido'), sg.Button('Preço'), sg.Text('', key='preço'), sg.Text(' '*87), sg.Button('Sobre nós', key='sobre')],
]

sg.theme('Reddit')
window = sg.Window('Pizzaria', layout, size=(660, 220), resizable=True)

while True:
  
    event, values = window.read()
       
    peq = 14.99 * values[2]
    med = 24.99 * values[2]
    gran = 39.99 * values[2]

    def multiplePequena(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format(peq * len(values[0])))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(peq))
            
    def multipleMedia(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format(med * len(values[0])))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(med))
        
    def multipleGrande(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format(gran * len(values[0])))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(gran))

    def descontoPequena(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format((peq * len(values[0]))* 0.85))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(peq * 0.85))
        
    def descontoMedia(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format((med * len(values[0]))* 0.85))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(med * 0.85))
        
    def descontoGrande(x):
        if len(values[0]) > x:
            window.find_element('preço').Update('R${:.2f}'.format((gran * len(values[0]))* 0.85))
        else:
            window.find_element('preço').Update('R${:.2f}'.format(gran * 0.85))
            
            
    if event == sg.WIN_CLOSED:
        break
  

    if event == 'salvar':
        lista.append(values[0])
        lista.append(values[1])
        lista.append(values[2])
        
        def calcular_preço():
            if 'Pequena' in values[1]:
                return '{:.2f}'.format(peq)
            elif 'Média' in values[1]:
                return '{:.2f}'.format(med)
            elif 'Grande' in values[1]:
                return '{:.2f}'.format(gran)
   
    if event == 'Preço':
        if not values[1]:
            sg.PopupTimed('Nenhum tamanho foi selecionado!', auto_close_duration=1)
            window.find_element('preço').Update('R$0.00')
            
        if not values[0]:
            sg.PopupTimed('Nenhuma pizza foi selecionada!', auto_close_duration=1)
            window.find_element('preço').Update('R$0.00')
            
        else:
            if 'Pequena' in values[1]:
                multiplePequena(1)
            elif 'Média' in values[1]:
                multipleMedia(1)
            elif 'Grande' in values[1]:
                multipleGrande(1)
                
    if event == 'sobre':
         sg.Popup(random.choice(frases), title='')
    
    
    if event == 'verificar':
    
        try:
            endereço = get_address_from_cep(values[4], webservice=WebService.APICEP)
            avenida = list(endereço.values())[3]
            bairro = list(endereço.values())[0]
            window.find_element('endereço').Update(avenida)
            window.find_element('bairro').Update(bairro)
            
        except exceptions.InvalidCEP:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
        except exceptions.CEPNotFound:
            sg.PopupTimed('CEP não encontrado!', auto_close_duration=1)
        except exceptions.BaseException:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
            
    if event == 'cupomBotao':
         if 'DOCA15' in values[3]:
            if 'Pequena' in values[1]:
                descontoPequena(1)
                
            elif 'Média' in values[1]:
                descontoMedia(1)
            
            elif 'Grande' in values[1]:
                descontoGrande(1)
                
         else:
             sg.PopupTimed('Cupom inválido!', auto_close_duration=1)
            
    if event == 'pedido':
          if not values[1]:
                
                sg.PopupTimed('Nenhum tamanho foi selecionado!', auto_close_duration=1)
                
          elif not values[0]:
                sg.PopupTimed('Nenhuma pizza foi selecionada!', auto_close_duration=1)
                
          else:
                if len(lista) == 3:
                    
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
    
                    comando = f"""INSERT INTO Pizzas(Sabor, Tamanho, Quantidade, Preço) 
                                  VALUES
                                      ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}')"""

                    cursor.execute(comando)
                    cursor.commit()
        
                        
                elif len(lista) == 6:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    df = pd.DataFrame([pizza1, pizza2])
                    print(df)
                    
                elif len(lista) == 9:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    pizza3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                    df = pd.DataFrame([pizza1, pizza2, pizza3])
                    print(df) 
                    
                elif len(lista) == 12:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    pizza3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                    pizza4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                    df = pd.DataFrame([pizza1, pizza2, pizza3, pizza4])
                    print(df)
                    
                elif len(lista) == 15:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    pizza3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                    pizza4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                    pizza5 = pd.Series({'Sabor': '{}'.format(''.join(lista[12])), 'Tamanho': '{}'.format(''.join({lista[13]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                
                    df = pd.DataFrame([pizza1, pizza2, pizza3, pizza4, pizza5])
                    print(df)
                    
                elif len(lista) == 18:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}'})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    pizza3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                    pizza4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                    pizza5 = pd.Series({'Sabor': '{}'.format(''.join(lista[12])), 'Tamanho': '{}'.format(''.join(lista[13])), 'Qtd': f'{int(lista[14])}', 'Preço': f'{calcular_preço()}'})
                    pizza6 = pd.Series({'Sabor': '{}'.format(''.join(lista[15])), 'Tamanho': '{}'.format(''.join(lista[16])), 'Qtd': f'{int(lista[17])}', 'Preço': f'{calcular_preço()}'})
                    df = pd.DataFrame([pizza1, pizza2, pizza3, pizza4, pizza5, pizza6])
                    print(df)
                    
                elif len(lista) == 21:
                    pizza1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}',})
                    pizza2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                    pizza3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                    pizza4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                    pizza5 = pd.Series({'Sabor': '{}'.format(''.join(lista[12])), 'Tamanho': '{}'.format(''.join(lista[13])), 'Qtd': f'{int(lista[14])}', 'Preço': f'{calcular_preço()}'})
                    pizza6 = pd.Series({'Sabor': '{}'.format(''.join(lista[15])), 'Tamanho': '{}'.format(''.join(lista[16])), 'Qtd': f'{int(lista[17])}', 'Preço': f'{calcular_preço()}'})
                    pizza7 = pd.Series({'Sabor': '{}'.format(''.join(lista[18])), 'Tamanho': '{}'.format(''.join(lista[19])), 'Qtd': f'{int(lista[20])}', 'Preço': f'{calcular_preço()}'})
                    df = pd.DataFrame([pizza1, pizza2, pizza3, pizza4, pizza5, pizza6, pizza7])
                    print(df)
               
            
            
            
    

    
  


window.close()
