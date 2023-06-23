import socket
import time
import random
import socket
import threading
import time
from Funcoes.funcoes import *
import re

tamanho = 1024
padrao = "utf-8"




global sinal
sinal=False
global stop
global port
port=  None



def IniciarEleicao():
    print("Iniciando eleição de servidores")
    #carregar ips
    NumPCs = 'NumPCs.txt'
    ipRede='IpRede.txt'
    try:
        with open(ipRede, 'r') as arquivo:
            ip = arquivo.read()
    except:
        ip="127.0.0.1"
        with open(ipRede, "w") as arquivo:
            arquivo.write(ip)
            
    try:
        with open(NumPCs, 'r') as arquivo:
            qtd = int(arquivo.read())
    except:
        qtd=8
        with open(NumPCs, "w") as arquivo:
            arquivo.write(str(qtd))   
    
    #gerar base do servidor
    try:
        redes = ConsultarIps()
    
        HOST=ip
        PORT =  int(redes[0][2])
    except:
        HOST=ip
        PORT=9998
    indicacao=int((random.randint(1, 100)*random.randint(1, 100))/random.randint(1, 100))
   
    HOST=modify_ip(HOST,1,1)
    global inicio
    global ProxNo 
    ProxNo=["",""]
    inicio=PORT+1
    first=True
    isHost=False
    conectado=True
    for i in range(qtd-1):
        if not conectado:
            break
      
        global msg
        
        if (PORT+1)!=inicio:
            PORT=inicio+qtd-i
            if i>1:
                HOST=modify_ip(HOST,1,2)
            else:
                HOST=modify_ip(HOST,(qtd-1),1)
        else:
            PORT+=1
            HOST=modify_ip(HOST,1,1)
        endereco_destino = (HOST, PORT)  # Endereço 
        print(endereco_destino)
       
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.bind(endereco_destino)
            servidor.listen()
            
            print('Estou ancorado')
            while conectado:
                try:
                    print('AINDA CONECTADO')
                    
                    if PORT==inicio and first:
                      
                        print('sou o primeiro vou mandar meu voto')
                        time.sleep(5)
                        first=False
                        HOST=modify_ip(HOST,1,1)
                        ProxNo=enviar_mensagem((HOST,PORT+1), indicacao,qtd,inicio,1,PORT)
                        servidor.settimeout(90)
                        
                        
                    if PORT != inicio:
                        servidor.settimeout(90)
                    if i== qtd:
                        PORT-(qtd+1)
                    
                    if ProxNo[1] == endereco_destino[1]:
                        if not ping():
                            print("[AVISO] Sou o unico na eleição")
                            ip,port=endereco_destino
                            SetarIP('secondary',ip,str(port),'ativo')
                            conectado=False
                            isHost=True
                            servidor.close()
                            break
                        else:
                            print("[AVISO] Eleição cancelada Servidor Principal no Ar")
                            conectado=False
                            servidor.close()
                            break
                    else:
                        conn, endereco = servidor.accept()
                        print(endereco)
                        msg = conn.recv(tamanho).decode(padrao)
                        conn.sendall('ok'.encode(padrao))
                    
            
                    try:
                        if  int(msg)<indicacao:
                            if ProxNo[1]=="":
                                print("meu numero é maior")
                                
                                ProxNo=enviar_mensagem((modify_ip(HOST,1,1),PORT+1), indicacao,qtd,inicio,1,PORT)
                            else:
                                print("meu numero é maior")
                                enviar_mensagem((ProxNo), indicacao,qtd,inicio,2,PORT)
                        elif int(msg)==indicacao:
                            if not ping():
                                enviar_aviso(endereco_destino,qtd,ProxNo,PORT)
                                ip,port=endereco_destino
                                SetarIP('secondary',ip,str(port),'ativo')
                                conectado=False
                                isHost=True
                                conn.close()
                                servidor.close()
                                break
                            else:
                                print("[AVISO] Eleição cancelada Servidor Principal no Ar")
                                conectado=False
                                servidor.close()
                                break
                        else:
                            if ProxNo[1]=="": 
                                print("meu numero é menor")
                                ProxNo=enviar_mensagem((modify_ip(HOST,1,1),inicio+1), msg,qtd,inicio,1,PORT)
                            
                            else:
                                print("meu numero é menor")
                                enviar_mensagem((ProxNo), msg,qtd,inicio,2,PORT)
                    except:
                        conn.close()
                        print("eleicao encerrada")
                        print('Caminho do novo servidor', msg)
                        msg = re.sub(r"[\'\(\)]", "", msg)
                        NewServer=msg.split(',')
                        print(NewServer)
                        ip,port=NewServer
                        enviar_aviso(NewServer,qtd,ProxNo,PORT)
                        servidor.close()
                        print('Conectando ao novo Servidor')
                        conectado=False
                        break
                except socket.timeout:
                    print("Tempo limite de 30 segundos atingido. Nenhuma conexão foi aceita.")
                    conectado=False
                    print("não consegui participar da eleição")
                    servidor.close()
                    
                    
        except:
            next
            time.sleep(1)
    if isHost:
        serverReserva(ip,port)
    else:
        try:
            main(ip,port)
        except:
            main()
   
def enviar_mensagem(no_destino, mensagem,pcs,PortIinicial,operacao, myPort):
    
    contador=0
    reset=False
    if operacao==1:
        
        PORT=myPort+1
        no_destino=no_destino[0], PORT
        for i in range (pcs-1):
            if myPort==(inicio+pcs-1) and not reset:
                no_destino=modify_ip(no_destino[0], (pcs),2), inicio
                reset=True
                PORT=inicio
            if PORT==myPort:
                if i== (pcs-2):
                    no_destino=modify_ip(no_destino[0], (pcs-1),2), inicio
                    PORT=inicio
                else:
                    PORT=no_destino[1]
                    PORT+=1
                    HOST=modify_ip(HOST,1,1)
                    no_destino=HOST, PORT
           
            while contador<3:
                try:
                    endereco_destino = (no_destino)  # Endereço do próximo nó
                    mensagem_serializada = str(mensagem)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print(f"[Conectando] Tentando Ancoragem no Caminho {no_destino}")
                        s.connect(endereco_destino)
                        
                        print('[Conectado] Ancorado, vou enviar meu voto')
                        s.sendall(mensagem_serializada.encode(padrao))
                        print('[Enviado] Voto enviado com sucesso!')
                        resposta=s.recv(tamanho).decode(padrao)
                        if resposta=="ok":
                            print("Confirmação de voto recebida")
                            return no_destino
                except:
                   
                    print(f"[ERRO] Caminho {no_destino} sem resposta, tentando Novamente")

                    contador+=1
            
        
            
            if PORT==(PortIinicial+(pcs-1)):
                print(f'[SEM CONEXÃO] no Caminho {no_destino} sem Retorno, tentando em outro Caminho')
                PORT=no_destino[1]
                PORT-=(pcs-1)
                HOST=modify_ip(no_destino[0],(pcs-1),1)
                no_destino=no_destino[0], PORT
                contador=0
            
            else:
                contador=0
                print(f'[SEM CONEXÃO] no Caminho {no_destino} sem Retorno, tentando em outro Caminho')
                PORT=no_destino[1]
                PORT+=1
                no_destino=modify_ip(no_destino[0],1,1), PORT
     
    else:
        
        while contador<3:
                try:
                    endereco_destino = (no_destino)  # Endereço do próximo nó
                    mensagem_serializada = str(mensagem)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print(f"[Conectando] Tentando Ancoragem  na porta {no_destino[1]}")
                        s.connect(endereco_destino)
                        print('[Conectado] Ancorado, vou enviar meu voto')
                        s.sendall(mensagem_serializada.encode(padrao))
                        print('[Enviado] Voto enviado com sucesso!')
                        resposta=s.recv(tamanho).decode(padrao)
                        if resposta=="ok":
                            print("Confirmação de voto recebida")
                            return None
                except:
                    time.sleep(1)
                    print(f"[ERRO] Porta {no_destino[1]} sem resposta, tentando Novamente")

                    contador+=1    
        print("[Erro] Sem retorno, voltaremos a varredura ")
        enviar_mensagem(no_destino, mensagem,pcs,1,)   
    
    return no_destino

def enviar_aviso(servidor,pcs,proxNo,myport):
    
    HOST,PORT=servidor
    PORT=int(PORT)
    time.sleep(1)
    Vencedor=HOST,PORT
    reset=False
    servidor= proxNo
    for i in range (pcs-1):
        
         
    
        if servidor[1]==myport and not reset:
            if i== (pcs-2):
                HOST=modify_ip(servidor[0], (pcs),1)
                reset=True
                servidor= HOST,inicio
            else:
                HOST=modify_ip(servidor[0],1,1)
                servidor= HOST,(inicio+1)
        if PORT==servidor[1]:
            HOST=modify_ip(servidor[0],1,1)
            servidor= HOST,(inicio+1)
        
        try:
            endereco_destino = (servidor)  # Endereço do próximo nó
            mensagem_serializada = str(Vencedor)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(endereco_destino)
                print('Conectei para enviar o aviso')
                s.sendall(mensagem_serializada.encode(padrao))
                print('Enviei o aviso')
                resposta=s.recv(tamanho).decode(padrao)
                if resposta=="ok":
                    print("aviso enviado")
                    break
        except:
            print(F'erro sem retorno no Caminho {servidor}')
            if servidor[1]==(inicio+pcs-1):
                HOST=modify_ip(servidor[0],(pcs-1),2)
                servidor= HOST,inicio
                
            else:
               port=servidor[1]
               HOST=modify_ip(servidor[0],1,1)
               servidor= HOST,(port+1) 
                    
            
            next




def conexao( conexao, enderecoCliente):
    print(f"[NOVO USUARIO CONECTADO] {enderecoCliente} conectou.")
    conectado=True
    opcao=""
    global sinal

    while conectado and not sinal:
        try:
            msg = conexao.recv(tamanho).decode(padrao)
            if msg == "voltei":

                conectado = False
                conexao.close()

                sinal = True

                break
            if msg == "gerente" and not sinal:
                conexao.sendall(
                    """[Painel de Gerencia] \n Escolha uma das Funções Abaixo:
                      \n 1 - Cadastrar Vendedores 
                      \n 2 - Cadastrar Lojas
                      \n 3 - Vendas de uma Loja
                      \n 4 - Vendas Por Periodo
                      \n 5 - Melhor Vendedor
                      \n 6 - Melhor Loja """.encode(padrao))
            
                opcao = conexao.recv(tamanho).decode(padrao)
                if opcao == '1' and not sinal:
                    CadastrarVendedor(conexao)
                elif opcao == '2' and not sinal:
                    cadastroDeLoja(conexao)
                elif opcao == '3' and not sinal:
                    vendasDeUmaLoja(conexao)
                elif opcao == "4" and not sinal:
                    vendasPorPeriodo(conexao)
                elif opcao == "5" and not sinal:
                    melhorVendedor(conexao)
                elif opcao == "6" and not sinal:
                    melhorLoja(conexao)
                else:
                    conexao.send('opcao invalida'.encode(padrao))
            elif msg == "vendedor" and not sinal:
                conexao.send("""[Painel de Vendas] \n Escolha uma das Funções Abaixo: 
                \n 1 - Registrar Venda """.encode(padrao))
                status = msg
                opcao = conexao.recv(tamanho).decode(padrao)
                if opcao == '1' and not sinal:
                    Vendedor_CadastrarVenda(conexao)

                else:
                    conexao.send('opcao invalida'.encode(padrao))

        except:
            next
            conectado = False
            conexao.close()

        if stop:
            break
    conexao.close()
    
def serverReserva(ip,port):
    global sinal
    global stop
    sinal=False
    ativo=True
    stop = False
    print("[INICIANDO] O Servidor está Iniciando...")
    print(f'IP Local: {ip}')
    print('seu ip local será usado para ancoragem do servidor atual')
    SetarIP('primary','0.0.0.0','9998','inativo')
    print(ConsultarIps())
    HOST = ip        # Endereco IP do Servidor
    PORT = port          # Porta que o Servidor esta
    servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    a=0
    while a==0: 
        try:
            servidor.bind((HOST,PORT))
            servidor.listen()
            print(f"[ATIVO] O Servidor está Ativo no: {ip}:{PORT}")
            
            a=1
        except:
            next
    while ativo:
        if  sinal:
            SetarIP('secondary', '0.0.0.0','0000', 'inativo')
            ativo=False
            stop=True
            servidor.close()
            parar_todas_as_threads()
            break
        conn, endereco=servidor.accept()
        thread=threading.Thread(target=conexao, args=( conn, endereco) )
        thread.start()
        print(thread)
        
        print(f"usuarios ativos {threading.active_count()-1} ")
        
        if  sinal:
            ativo=False
            SetarIP('secondary', '0.0.0.0','0000', 'inativo')
            print("[AVISO] O servidor principal está no ar")
            print("Entrando em modo cliente")
            stop=True
            thread.join()
            servidor.close()
            parar_todas_as_threads()
            break
def parar_todas_as_threads():
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()
def main(ip=None,port=0):
    erro= False
    contador = 0
    while True:
        
        try:
            if not ip ==None and  not erro :
                ip.replace("(", "").replace(")", "")
                HOST=ip.replace("'", "").replace(")", "")
                PORT=int(port)
            else:
                redes = ConsultarIps()
               
                HOST = redes[0][1]
                PORT = int(redes[0][2])
                
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))
            mensagem = ""
            primeira = True
      
            timeout = 5  # Timeout de 5 segundos
            cliente.settimeout(timeout)

        
            while mensagem != "fim":
                
                
                if primeira:
                    print("...Iniciando interação com o Servidor")
                    cliente.sendall("gerente".encode(padrao))
                    primeira = False
                    try:
                        resposta = cliente.recv(tamanho)
                        contador = 0
                    except socket.timeout:
                        print("Tempo de espera excedido. Nenhum dado recebido.")
                    
                else:
                    if resposta.decode(padrao)[-3:] == "" or resposta.decode(padrao)[-3:] == "fim" :
                        print("... >>> O servidor me respondeu:", resposta.decode(padrao)[:-3])
                        time.sleep(3)
                        mensagem = "fim"
                    elif resposta.decode(padrao) == 'Opção inválida':
                        print("... >>> O servidor me respondeu:", resposta.decode(padrao))
                        cliente.sendall("vendedor".encode(padrao))
                        primeira = False
                        try:
                            contador = 0
                            resposta = cliente.recv(tamanho)
                        except socket.timeout:
                            print("Tempo de espera excedido. Nenhum dado recebido.")
                    else:
                        
                        print("... >>> O servidor me respondeu:", resposta.decode(padrao))
                        mensagem = input("Mensagem > ")
                        if mensagem=="":
                            mensagem="invalido"
                        cliente.sendall(mensagem.encode(padrao))
                        primeira = False
                        try:
                            contador = 0
                            resposta = cliente.recv(tamanho)
                        except socket.timeout:
                            print("Tempo de espera excedido. Nenhum dado recebido.")
                  
                
            print("Encerrando o cliente")
            cliente.close()
        except:
            erro= True
            print('Servidor indisponível')
            print('Tentando novamente em alguns segundos')
            time.sleep(1.5)
            contador += 1
       
            
        if contador > 2:
            erro=False
            print("Servidor indisponível, iniciando eleição")
            IniciarEleicao()
            if sinal:
                contador=0

def ping():
    try:
        redes = ConsultarIps()
       
        HOST = redes[0][1]
        PORT = int(redes[0][2])
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultado=cliente.connect((HOST, PORT))
        return True
    except:
        return False

def modify_ip(ip, value, operation):
    ip_parts = ip.split('.')
    last_part = int(ip_parts[-1])
    
    if operation == 1:  # Incremento
        modified_last_part = last_part + value
    elif operation == 2:  # Decremento
        modified_last_part = last_part - value
    else:
        raise ValueError("Operação inválida. Use 1 para incremento e 2 para decremento.")
    
    # Verifica se o último componente excede 255
    if modified_last_part > 255:
        carry = modified_last_part // 256  # Valor a ser "carregado" para o próximo conjunto
        modified_last_part %= 256  # Restante dentro do intervalo 0-255
        
        # Incrementa ou decrementa o valor "carregado" para o próximo conjunto
        if operation == 1:
            ip_parts[-2] = str(int(ip_parts[-2]) + carry)
        elif operation == 2:
            ip_parts[-2] = str(int(ip_parts[-2]) - carry)
        
    ip_parts[-1] = str(modified_last_part)
    modified_ip = '.'.join(ip_parts)
    return modified_ip




if __name__ == "__main__":
    main()





