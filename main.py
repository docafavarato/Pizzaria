import PySimpleGUI as sg
import pandas as pd
from pycep_correios import get_address_from_cep, WebService, exceptions


layout = [
  [sg.Listbox(values=['Queijo', 'Calabresa', 'Portuguesa', 'Toscana', 'Marguerita', 'Brigadeiro', 'Especial'], size=(20, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE), sg.Listbox(['Pequena', 'Média', 'Grande'], size=(10, 3)), sg.Text(' '*4), sg.Text('Cupom: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='cupomBotao')],
  [sg.Text(' '*73), sg.Text('CEP: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='verificar')],
  [sg.Slider(orientation='horizontal'), sg.Text(' '*18), sg.Text('Endereço: '), sg.InputText(key='endereço', size=(25,10))],
  [sg.Text(' '*71), sg.Text('Bairro: '), sg.InputText(key='bairro', size=(25,10))],
  [sg.Button('Concluir Pedido', key='pedido'), sg.Button('Preço'), sg.Text('', key='preço')],
]


sg.theme('DarkTanBlue')
window = sg.Window('Pizzaria', layout, size=(630, 260), resizable=True)


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
            
  # Valida o cupom inserido pelo usuário e aplica o desconto
  if event == 'cupomBotao':
        if 'DOCA10' in valores[2]:
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
        
            if len(valores[0]) == 1:   
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1])
                print(df)

            elif len(valores[0]) == 2:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2])
                print(df)

            elif len(valores[0]) == 3:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})      
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3])
                print(df)

            elif len(valores[0]) == 4:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4])
                print(df)

            elif len(valores[0]) == 5:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5])
                print(df)
                
             elif len(valores[0]) == 6:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_6 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6])
                print(df)
                
             elif len(valores[0]) == 7:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_6 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_7 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6, pizza_7])
                print(df)
                
             elif len(valores[0]) == 8:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_6 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_7 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_8 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6, pizza_7, pizza_8])
                print(df)
                
             elif len(valores[0]) == 9:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_6 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_7 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_8 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_9 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6, pizza_7, pizza_8, pizza_9])
                print(df)
                
              elif len(valores[0]) == 10:
                pizza_1 = pd.Series({'Sabor': f'{valores[0][0]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_2 = pd.Series({'Sabor': f'{valores[0][1]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_3 = pd.Series({'Sabor': f'{valores[0][2]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_4 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_5 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_6 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_7 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_8 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_9 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                pizza_10 = pd.Series({'Sabor': f'{valores[0][3]}', 'Tamanho': '{}'.format(''.join(valores[1])), 'Qtd': f'{int(valores[4])}'})
                df = pd.DataFrame([pizza_1, pizza_2, pizza_3, pizza_4, pizza_5, pizza_6, pizza_7, pizza_8, pizza_9, pizza_10])
                print(df)
                
              
            
            
      
    

    
        

       
        

  

window.close()
