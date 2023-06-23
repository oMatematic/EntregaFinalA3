from Banco.banco import *
import re
from datetime import datetime, timedelta
import requests
import time
from Banco.banco import*


tamanho = 1024
padrao = ("utf-8")



def Vendedor_CadastrarVenda(con):
    con.send("Informe Seu CPF".encode(padrao))
    isNum=False
    while not isNum:
        
        cpf = str(con.recv(tamanho).decode(padrao))
        

        if tem_letras_ou_caracteres_especiais(cpf): 
                con.send( "[ERRO] Digite apenas número." .encode(padrao))
        elif len(cpf)!=11:
            con.send( "[ERRO] CPF incompleto, o CPF deve possuir 11 dígitos." .encode(padrao))
        elif not testar_cpf(cpf):
            con.send( "[ERRO] CPF inválido, o CPF deve Autêntico." .encode(padrao))
        elif buscarVendedor(cpf)==None:
             con.send( "[ERRO] CPF não cadastrado, consulte o Gerente." .encode(padrao))
        else:
            isNum=True
    vendedor=buscarVendedor(cpf)


    print(vendedor)
    naoNum = True
    con.send(f" Olá {vendedor[1]} Informe Valor da Venda".encode(padrao))
    while (naoNum):

        try:
            valor = float(con.recv(tamanho))
            naoNum = False
            print(valor)
        except:
            con.send(
                "Erro! insira uma configuração de moeda válida. Ex: 19.00".encode(padrao))
            

    agora = datetime.now()
    formato = "%Y-%m-%d"
    data_formatada = agora.strftime(formato)
    resposta = CadastrarVenda(vendedor[0], valor, vendedor[4],data_formatada)
    con.send(resposta.encode(padrao))


def Vendedor_ListarVenda(con):
    con.send("Informe o nome do vendedor".encode(padrao))
    nome = str(con.recv(tamanho).decode(padrao)).upper()
    print(nome)
    vendas = ListarVendas(nome)
    if vendas[0]==None:
        resposta="Vendedor não encontrado!"
    else:
        resposta = (f"O valor total de vendas de [{nome}] foi de R$ {vendas[0]:.2f}")
    con.send(resposta.encode(padrao))
    con.send('fim'.encode(padrao))



    
def cadastroDeLoja(con):

    fim=False
    dados=None
    nomeVazio=True
    while not fim:
        con.send("Informe o nome da loja".encode(padrao))
        while nomeVazio:

            
            nome = str(con.recv(tamanho).decode(padrao)).upper()
       
            if nome=="" or nome=="invalido":
                con.send("Erro! O nome da loja não pode ser vazio\n... >>> O servidor me respondeu: Informe o nome da loja".encode(padrao))
            elif tem_espaco_inicio(nome):
                con.send("Erro! Nome contém espaço antes do primeiro caractere\n... >>> O servidor me respondeu: Informe o nome da loja".encode(padrao))
            else:
                nomeVazio=False
        incompleto = True
        temLetra=False
        con.send("Informe o Cep da Loja".encode(padrao))
        while (incompleto):
            
            try:
                cep = str(con.recv(tamanho).decode(padrao))
          
                if tem_letras_ou_caracteres_especiais(cep) or len(cep)!=8 :
                     con.send(
                    "[ERRO] Insira apenas números. Ex: 41305100 [Elemento (-) ou espaco não e necessario]" .encode(padrao))
                
                dados=consultar_cep(cep)
                if len(dados)==1:
                    con.send(
                    "[ERRO] Cep Não encontrado! Insira um Cep Válido." .encode(padrao))
                else:
                    con.send(
                    f"Localização \n +++  Cep: {cep} \n +++  Bairro: {dados['bairro']} \n +++  Cidade: {dados['localidade']} \n +++  Estado: {dados['uf']} \n\n Confirma esses Dados? Digite:\n 1) Sim \n 2) Não" .encode(padrao))
                    estado= True
                    while estado:
                        resposta = str(con.recv(tamanho).decode(padrao))
                 
                        if resposta=="1":
                            con.send("Informe o Numero de identificação da Loja".encode(padrao))
                            while estado:
                                
                                numero = str(con.recv(tamanho).decode(padrao))
                       
                   
                                if tem_espaco_inicio(numero) or tem_letras_ou_caracteres_especiais(numero):
                                     con.send( "[ERRO] Digite apenas número." .encode(padrao))
                                else:
                                    incompleto=False
                                    estado=False
                        elif resposta =="2":
                            estado=False
                            con.send("Informe o Cep da Loja".encode(padrao))
                        else:
                            con.send(f"Opção inválida! digite 1 ou 2" .encode(padrao))
                    
            except:
                next
        if buscarLoja(nome,cep,numero)!= None:
            con.send(f"Erro! a Empresa [{nome}] Já foi Cadastrada" .encode(padrao))
            time.sleep(3)
            fim=True
        else:
            resposta=cadastrarLoja(nome,cep,numero,dados['localidade'],dados['uf'])
            if resposta:
                con.send(f" a Empresa [{nome}] foi Cadastrada Com Sucesso" .encode(padrao))
                time.sleep(3)
                fim=True
            else:
                con.send(f"Erro! ao cadastrar a Empresa [{nome}], Tente novamente mais tarde" .encode(padrao))
                time.sleep(3)
                fim=True
    con.send('fim'.encode(padrao))

def CadastrarVendedor(con):

    isNum=False
    nomeVazio=True
    dataSuperior=True
    semLoja=True
    con.sendall("Informe o nome do vendedor".encode(padrao)) 
    while nomeVazio:
        nome = str(con.recv(tamanho).decode(padrao)).upper()

        if nome=="" or nome=="invalido":
                con.send("Erro! do vendedor não pode ser vazio\n... >>> O servidor me respondeu: Informe o nome do vendedor".encode(padrao))
        elif tem_espaco_inicio(nome):
            con.send("Erro! Nome contém espaço antes do primeiro caractere\n... >>> O servidor me respondeu: Informe o nome do vendedor".encode(padrao))
        else:
           nomeVazio=False
    con.send("Informe o cpf do vendedor".encode(padrao))
    while not isNum:
        
        cpf = str(con.recv(tamanho).decode(padrao))
    
        if tem_letras_ou_caracteres_especiais(cpf): 
                con.send( "[ERRO] Digite apenas número." .encode(padrao))
        elif len(cpf)!=11:
            con.send( "[ERRO] CPF incompleto, o CPF deve possuir 11 dígitos." .encode(padrao))
        elif not testar_cpf(cpf):
            con.send( "[ERRO] CPF inválido, o CPF deve Autêntico." .encode(padrao))
        else:
            isNum=True
    con.send( "Informe a data de contratação" .encode(padrao))
    while dataSuperior:
        data_contratacao=  str(con.recv(tamanho).decode(padrao))
      
       
        
        if not testar_padrao_data(data_contratacao) :
            con.send( "[ERRO] Data não aceita, padrão aceito dd-mm-aaaa." .encode(padrao))
       
        elif  not verificar_data_valida(data_contratacao):
            con.send( "[ERRO] Data inválida, verifique a data e tente novamente." .encode(padrao))
        else:
            data_contratacao=datetime.strptime(data_contratacao, "%d-%m-%Y").date()
            if data_maior_que_hoje(data_contratacao):
                con.send( "[ERRO] Data de contratação superior a data atual!." .encode(padrao))
            elif data_inferior_100_anos(data_contratacao):
                con.send( "[ERRO] Data de contratação não pode ser inferior a 100 anos!." .encode(padrao))
            else:
                dataSuperior=False
    Lojas=listarTodasLojas()
    msg, ids =preprarar_listasLojas(Lojas)
    if msg=="":
        con.send( f"Não existem lojas cadastradas" .encode(padrao))
    else:
        con.send( f"Escolha uma das lojas Abaixo e informe o ID correspondente.\n {msg}" .encode(padrao))
        while(semLoja):
            
            
            loja= str(con.recv(tamanho).decode(padrao))

            if tem_letras_ou_caracteres_especiais(loja): 
                    con.send( "[ERRO] Digite apenas o número." .encode(padrao))
                
            elif not int(loja) in ids:
                con.send( "[ERRO] Id invalido, verifique a loja e tente novamente." .encode(padrao))
            else:
                semLoja=False

        if buscarVendedor(cpf)!= None:
                con.send(f"Erro! Já possui um vendedor cadastrado Com esse CPF" .encode(padrao))
                time.sleep(3)
                
        else:
                resposta=cadastrarFuncionario(nome, cpf, data_contratacao, loja)
                if resposta:
                    con.send(f" [{nome}] foi Cadastrada Com Sucesso" .encode(padrao))
                    time.sleep(3)
                
                else:
                    con.send(f"Erro! ao cadastrar Vendedor(a) [{nome}], Tente novamente mais tarde" .encode(padrao))
                    time.sleep(3)
                    fim=True
    con.send('fim'.encode(padrao))

def vendasDeUmaLoja(con):
    semLoja=True
    Lojas=listarTodasLojas()
    msg, ids =preprarar_listasLojas(Lojas)
    if msg=="":
        con.send( f"Não existem lojas cadastradas" .encode(padrao))
    else:
        con.send( f"Escolha uma das lojas Abaixo e informe o ID correspondente.\n {msg}" .encode(padrao))
        while(semLoja):
            
            
            loja= str(con.recv(tamanho).decode(padrao))

            if tem_letras_ou_caracteres_especiais(loja): 
                    con.send( "[ERRO] Digite apenas o número." .encode(padrao))
                
            elif not int(loja) in ids:
                con.send( "[ERRO] Id invalido, verifique a loja e tente novamente." .encode(padrao))
            else:
                semLoja=False
    resposta,nome =ListarVendasUmaLoja(loja)

   
    if resposta[0]==None:
        resposta='A loja não possui Vendas'
    else:
        resposta = (f"O valor total de vendas de [{nome[0]}] foi de R$ {resposta[0]:.2f}")
    con.send(resposta.encode(padrao))
    con.send('fim'.encode(padrao))

def vendasPorPeriodo(con):
    dataErro=True
    dataSuperior=True  
    con.send( "Informe a data de inicial do Periodo" .encode(padrao))
    while dataSuperior:
        data_inical=  str(con.recv(tamanho).decode(padrao))

        
        if not testar_padrao_data(data_inical) :
            con.send( "[ERRO] Data não aceita, padrão aceito dd-mm-aaaa." .encode(padrao))
       
        elif  not verificar_data_valida(data_inical):
            con.send( "[ERRO] Data inválida, verifique a data e tente novamente." .encode(padrao))
        else:
            data_inical=datetime.strptime(data_inical, "%d-%m-%Y").date()
            if data_maior_que_hoje(data_inical):
                con.send( "[ERRO] Data de consulta superior a data atual!." .encode(padrao))
            elif data_inferior_100_anos(data_inical):
                con.send( "[ERRO] Data de consulta não pode ser inferior a 100 anos!." .encode(padrao))
            else:
                dataSuperior=False
    con.send( "Informe a data de Final do Periodo" .encode(padrao))
    while dataErro:
        data_final=  str(con.recv(tamanho).decode(padrao))
        
        if not testar_padrao_data(data_final) :
            con.send( "[ERRO] Data não aceita, padrão aceito dd-mm-aaaa." .encode(padrao))
       
        elif  not verificar_data_valida(data_final):
            con.send( "[ERRO] Data inválida, verifique a data e tente novamente." .encode(padrao))
        else:
            data_final=datetime.strptime(data_final, "%d-%m-%Y").date()
            if data_maior_que_hoje(data_final):
                con.send( "[ERRO] Data de consulta superior a data atual!." .encode(padrao))
            elif data_inferior_100_anos(data_final):
                con.send( "[ERRO]Data de consulta não pode ser inferior a 100 anos!." .encode(padrao))
            elif data_final<data_inical:
                con.send( "[ERRO] Data Final é maior que a Data inicial." .encode(padrao))
            else:
                dataErro=False

    Lojas=listarTodasLojas()
    msg=preprarar_VendasLojas(Lojas,data_inical,data_final)
    con.send(msg.encode(padrao))
    time.sleep(10)
    con.send('fim'.encode(padrao))

def melhorVendedor(con):
    msg, nome=buscarMelhorVendedor()
    if msg==None:
        msg=("Não houve melhor vendedor!")
    else:
        msg=(f"[{nome}] foi o melhor vendedor de toda a rede Com R$: {msg:.2f}")
    con.send(msg.encode(padrao))
    time.sleep(10)
    con.send('fim'.encode(padrao))


def melhorLoja(con):

    msg, nome=buscarMelhorLoja()
    if msg==None:
        msg=("Não houve melhor Loja!")
    else:
        msg=(f"[{nome}] foi a melhor Loja de toda a rede Com R$: {msg:.2f}")
    con.send(msg.encode(padrao))
    time.sleep(10)
    con.send('fim'.encode(padrao))


def tem_letra(string):
    for caractere in string:
        if caractere.isalpha():
            return True
    return False
def tem_espaco_inicio(string):
    if string[:1].isspace():
        return True
    return False

def tem_letras_ou_caracteres_especiais(string):
    for caractere in string:
        if not caractere.isalnum():
            return True
        if caractere.isalpha():
            return True
            
            
    return False
    
def testar_padrao_data(data_string):
    padrao = r'^(\d{2})-(\d{2})-(\d{4})$'
    return re.match(padrao, data_string) is not None
    
def data_maior_que_hoje(data):
    data_atual = datetime.now().date()
    return data > data_atual

def testar_cpf(cpf):
    
    # Verificar se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcular os dígitos verificadores
    cpf_lista = list(map(int, cpf))
    soma1 = sum(cpf_lista[i] * (10 - i) for i in range(9))
    digito1 = (soma1 * 10) % 11
    if digito1 == 10:
        digito1 = 0
    
    soma2 = sum(cpf_lista[i] * (11 - i) for i in range(10))
    digito2 = (soma2 * 10) % 11
    if digito2 == 10:
        digito2 = 0
    
    # Verificar se os dígitos verificadores estão corretos
    if cpf_lista[9] != digito1 or cpf_lista[10] != digito2:
        return False
    
    return True

def data_inferior_100_anos(data):
    data_atual = datetime.now().date()
    data_limite = data_atual - timedelta(days=36525)
    return data < data_limite

def verificar_data_valida(data_string):
    try:
        datetime.strptime(data_string, "%d-%m-%Y").date()
        return True
    except ValueError:
        return False

def preprarar_listasLojas(lista):
    lojas=[]
    ficha=''
    
    for i, item in enumerate(lista):
        id=item[0]
        loja=item[1]
        cep=item[2]
        numero=item[3]
        cidade=item[4]
        uf=item[5]

        ficha+=f"\n ID: {id} | Nome: {loja}  | CEP: {cep} | Num: {numero} | Cidade: {cidade} | UF: {uf}\n----------"
        lojas.append(id)
    return ficha, lojas

def consultar_cep(cep):
    url = (f"https://viacep.com.br/ws/{cep}/json/")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def preprarar_VendasLojas(lista,inicio,fim):
 
    ficha=''
    inicio=inicio.strftime("%Y-%m-%d")
    fim=fim.strftime("%Y-%m-%d ")
    
    for i, item in enumerate(lista):
        id=item[0]
        loja=item[1]
        cidade=item[4]
        uf=item[5]
        total= buscarPorPeriodo(id,inicio,fim)
        if total==None:
            total=0.00
        ficha+=f"\n Loja: {id} | {loja}  | {cidade}-{uf} | Valor Vendido: R$ {total:.2f}  \n----------"
        
    return ficha