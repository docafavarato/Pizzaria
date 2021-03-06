import PySimpleGUI as sg
import pandas as pd
from time import sleep
import random
from pycep_correios import get_address_from_cep, WebService, exceptions
from itertools import chain

frases = ['Existimos desde 1959.',
          'Nossa pizzaria foi premiada como a melhor de SP.',
          'Você sabia que nós possuímos mais de 10 sabores de pizza?',
          'Realizamos entregas em toda a região.',
          'Temos forno à lenha.',
          'Nossa pizza especial leva um molho secreto.',
          'Somos a pizzaria mais antiga da região']
lista = []

layout = [
  [sg.Listbox(values=['Queijo', 'Calabresa', 'Portuguesa', 'Toscana', 'Marguerita', 'Brigadeiro', 'Especial'], size=(20, 6)), sg.Listbox(['Pequena', 'Média', 'Grande'], size=(10, 3)), sg.Text(' '*3), sg.Text('Cupom: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='cupomBotao')],
  [sg.Button('Salvar', key='salvar', border_width=1), sg.Text(' '*59), sg.Text('CEP: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='verificar')],
  [sg.Slider(orientation='horizontal'), sg.Text(' '*18), sg.Text('Endereço: '), sg.InputText(key='endereço', size=(25,10))],
  [sg.Text(' '*71), sg.Text('Bairro: '), sg.InputText(key='bairro', size=(25,10))],
  [sg.Button('Concluir Pedido', key='pedido'), sg.Button('Preço'), sg.Text('', key='preço'), sg.Text(' '*87), sg.Button('Sobre nós', key='sobre')],
]


sg.theme('Reddit')
window = sg.Window('Pizzaria', layout, size=(640, 260), resizable=True)


while True:
  
  event, valores = window.read()
 
  # Define os preços por tamanho
  peq = 14.99 * valores[4]
  med = 24.99 * valores[4]
  gran = 39.99 * valores[4]
    
  # Permite que todas as pizzas selecionadas sejam contabilizadas no preço
  def multiplePequena(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format(peq * len(valores[0])))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(peq))
        
  def multipleMedia(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format(med * len(valores[0])))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(med))
        
  def multipleGrande(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format(gran * len(valores[0])))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(gran))
        
  # Calcula um desconto sobre uma porcentagem (15%)       
  def descontoPequena(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format((peq * len(valores[0]))* 0.85))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(peq * 0.85))
        
  def descontoMedia(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format((med * len(valores[0]))* 0.85))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(med * 0.85))
        
  def descontoGrande(x):
    if len(valores[0]) > x:
        window.find_element('preço').Update('R${:.2f}'.format((gran * len(valores[0]))* 0.85))
    else:
        window.find_element('preço').Update('R${:.2f}'.format(gran * 0.85))
        
  
                                          
                                            
  
  if event == sg.WIN_CLOSED:
        break  
    
    
  if event == 'salvar':
    lista.append(valores[0])
    lista.append(valores[1])
    lista.append(valores[4])
    
    def calcular_preço():    
        if 'Pequena' in valores[1]:
            return '{:.2f}'.format(peq)
        elif 'Média' in valores[1]:
            return '{:.2f}'.format(med)
        elif 'Grande' in valores[1]:
            return '{:.2f}'.format(gran)
        
  if event == 'Preço':

        if not valores[1]:
            sg.PopupTimed('Nenhum tamanho foi selecionado!', auto_close_duration=1)
            window.find_element('preço').Update('R$0.00')
            
        if not valores[0]:
            sg.PopupTimed('Nenhuma pizza foi selecionada!', auto_close_duration=1)
            window.find_element('preço').Update('R$0.00')
            
        else:
            
            if 'Pequena' in valores[1]:
                multiplePequena(1)

            elif 'Média' in valores[1]:
                multipleMedia(1)

            elif 'Grande' in valores[1]:
                multipleGrande(1)
                
  # Exibe informações sobre a pizzaria
  if event == 'sobre':
    sg.Popup(random.choice(frases), title='')
            

  # Realiza uma busca pelo CEP do usuário e preenche as labels de endereço automaticamente       
  if event == 'verificar':
        try:
            
            endereço = get_address_from_cep(valores[3], webservice=WebService.APICEP)
            avenida = list(endereço.values())[3]
            bairro = list(endereço.values())[0]
            window.find_element('endereço').Update(avenida)
            window.find_element('bairro').Update(bairro)
        
        except exceptions.InvalidCEP as eic:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
        except exceptions.CEPNotFound:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
        except exceptions.BaseException:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
            
  # Valida o cupom inserido pelo usuário e aplica o desconto
  if event == 'cupomBotao':
        if 'DOCA15' in valores[2]:
            sg.PopupTimed('Cupom Válido!', auto_close_duration=1)
                       
            if 'Pequena' in valores[1]:
                descontoPequena(1)
        
            elif 'Média' in valores[1]:
                descontoMedia(1)
        
        
            elif 'Grande' in valores[1]:
                descontoGrande(1)
                     
            
        else:
            sg.PopupTimed('Cupom inválido! :(', auto_close_duration=1)
  
        
  # Constrói uma tabela com as informações do pedido      
  if event == 'pedido':
        if not valores[1]:
            sg.PopupTimed('Nenhum tamanho foi selecionado!', auto_close_duration=1)
            
        else:
        
            if len(lista) == 3:   
                try:
                    pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                    df = pd.DataFrame([pizza_1])
                    print(df)
                    
                except IndexError:
                    sg.PopupError('Lista fora do alcance')

            elif len(lista) == 6:
                pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                pizza_2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                df = pd.DataFrame([pizza_1, pizza_2])
                print(df)

            elif len(lista) == 9:
                pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                pizza_2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                pizza_3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3])
                print(df)

            elif len(lista) == 12:
                pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                pizza_2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                pizza_3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                pizza_4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4])
                print(df)

            elif len(lista) == 15:
                
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5])
                print(df)
                
            elif len(lista) == 18:
                pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                pizza_2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                pizza_3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                pizza_4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                pizza_5 = pd.Series({'Sabor': '{}'.format(''.join(lista[12])), 'Tamanho': '{}'.format(''.join(lista[13])), 'Qtd': f'{int(lista[14])}', 'Preço': f'{calcular_preço()}'})
                pizza_6 = pd.Series({'Sabor': '{}'.format(''.join(lista[15])), 'Tamanho': '{}'.format(''.join(lista[16])), 'Qtd': f'{int(lista[17])}', 'Preço': f'{calcular_preço()}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6])
                print(df)
                
            elif len(lista) == 21:
                pizza_1 = pd.Series({'Sabor': '{}'.format(''.join(lista[0])), 'Tamanho': '{}'.format(''.join(lista[1])), 'Qtd': f'{int(lista[2])}', 'Preço': f'{calcular_preço()}', 'Endereço': f'{avenida}'})
                pizza_2 = pd.Series({'Sabor': '{}'.format(''.join(lista[3])), 'Tamanho': '{}'.format(''.join(lista[4])), 'Qtd': f'{int(lista[5])}', 'Preço': f'{calcular_preço()}'})
                pizza_3 = pd.Series({'Sabor': '{}'.format(''.join(lista[6])), 'Tamanho': '{}'.format(''.join(lista[7])), 'Qtd': f'{int(lista[8])}', 'Preço': f'{calcular_preço()}'})      
                pizza_4 = pd.Series({'Sabor': '{}'.format(''.join(lista[9])), 'Tamanho': '{}'.format(''.join({lista[10]})), 'Qtd': f'{int(lista[11])}', 'Preço': f'{calcular_preço()}'})
                pizza_5 = pd.Series({'Sabor': '{}'.format(''.join(lista[12])), 'Tamanho': '{}'.format(''.join(lista[13])), 'Qtd': f'{int(lista[14])}', 'Preço': f'{calcular_preço()}'})
                pizza_6 = pd.Series({'Sabor': '{}'.format(''.join(lista[15])), 'Tamanho': '{}'.format(''.join(lista[16])), 'Qtd': f'{int(lista[17])}', 'Preço': f'{calcular_preço()}'})
                pizza_7 = pd.Series({'Sabor': '{}'.format(''.join(lista[18])), 'Tamanho': '{}'.format(''.join(lista[19])), 'Qtd': f'{int(lista[20])}', 'Preço': f'{calcular_preço()}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6, pizza_7])
                print(df)
                
    

  

window.close()
