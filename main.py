import PySimpleGUI as sg
from pycep_correios import get_address_from_cep, WebService, exceptions



layout = [
  [sg.Listbox(values=['Queijo', 'Calabresa', 'Portuguesa', 'Toscana', 'Marguerita', 'Brigadeiro', 'Especial'], size=(20, 6), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE), sg.Listbox(['Pequena', 'Média', 'Grande'], size=(9, 3)), sg.Text(' '*4), sg.Text('Cupom: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='cupomBotao')],
  [sg.Text(' '*73), sg.Text('CEP: '), sg.InputText(size=(25,10)), sg.Button('Verificar', key='verificar')],
  [sg.Slider(orientation='horizontal'), sg.Text(' '*18), sg.Text('Endereço: '), sg.InputText(key='endereço', size=(25,10))],
  [sg.Text(' '*71), sg.Text('Bairro: '), sg.InputText(key='bairro', size=(25,10))],
  [sg.Button('Concluir Pedido', key='pedido'), sg.Button('Preço'), sg.Text('', key='preço')],
]


sg.theme('DarkTanBlue')
window = sg.Window('Pizzaria', layout, size=(630, 260), resizable=True)


while True:
  
  event, values = window.read()
 
  peq = 14.99 * values[4]
  med = 24.99 * values[4]
  gran = 39.99 * values[4]
    
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
    
  
  if event == 'Preço':
   
        if not values[1]:
            sg.PopupTimed('Nenhum tamanho foi selecionado!', auto_close_duration=1)
            
        if not values[0]:
            sg.PopupTimed('Nenhuma pizza foi selecionada!', auto_close_duration=1)
            
        else:
            
            if 'Pequena' in values[1]:
                multiplePequena(1)

            elif 'Média' in values[1]:
                multipleMedia(1)

            elif 'Grande' in values[1]:
                multipleGrande(1)
            

            
  if event == 'verificar':
        try:
            
            endereço = get_address_from_cep(values[3], webservice=WebService.APICEP)
            avenida = list(endereço.values())[3]
            bairro = list(endereço.values())[0]
            window.find_element('endereço').Update(avenida)
            window.find_element('bairro').Update(bairro)
        
        except exceptions.InvalidCEP as eic:
            sg.PopupTimed('CEP inválido!', auto_close_duration=1)
        
  if event == 'cupomBotao':
        if 'DOCA10' in values[2]:
            sg.PopupTimed('Cupom Válido!', auto_close_duration=1)
                       
            if 'Pequena' in values[1]:
                descontoPequena(1)
        
            elif 'Média' in values[1]:
                descontoMedia(1)
                #window.find_element('preço').Update('R${:.2f}'.format(med * 0.85))
        
            elif 'Grande' in values[1]:
                descontoGrande(1)
                #window.find_element('preço').Update('R${:.2f}'.format(gran * 0.85))
            
            
        else:
            sg.PopupTimed('Cupom inválido! :(', auto_close_duration=1)
            
            
            
  if event == 'pedido':
        pass
    

    
        

       
        

  

window.close()
