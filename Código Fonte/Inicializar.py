import subprocess
import time




def SetarOperadores():
    resposta=""
    while resposta=="":
        try:
            print("Escolha a quantidade de Gerentes:")
            resposta=input(">>> ")
            gerentes=int(resposta)
        except:
            print("Resposta inválida")
            next
            resposta=""
    resposta=""    
    while resposta=="":
        try:
            print("Escolha a quantidade de Vendedores:")
            resposta=input(">>> ")
            vendedores=int(resposta)
        except:
            print("Resposta inválida")
            next
            resposta=""
    return gerentes, vendedores

def testarEleicao(gerentes, vendedores):

    with open(NumPCs, "w") as arquivo:
            arquivo.write(str(gerentes+vendedores+2)) 

    for _ in range(gerentes):
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'Gerente.py'], shell=True)
        time.sleep(0.5)
    for _ in range(vendedores):
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'vendedor.py'], shell=True)
        time.sleep(0.5)

def InicializarSistemas(gerentes, vendedores):

    with open(NumPCs, "w") as arquivo:
            arquivo.write(str(gerentes+vendedores+2)) 
    subprocess.Popen(['start', 'cmd', '/c', 'python', 'SocketsThread.py'], shell=True)
    time.sleep(3)
    for _ in range(gerentes):
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'Gerente.py'], shell=True)
        time.sleep(0.5)
    for _ in range(vendedores):
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'vendedor.py'], shell=True)
        time.sleep(0.5)








NumPCs = 'NumPCs.txt'

resposta=""
while resposta=="":
    print("O que deseja fazer? \n 1 - Testar Eleição \n 2- Inicializar o Sistema\n")
    resposta=input("Escolha uma das Alternativas : ")
    if resposta=="1":
        gerentes, vendedores=SetarOperadores()
        testarEleicao(gerentes,vendedores)    
    elif resposta=="2":
        gerentes, vendedores=SetarOperadores()
        InicializarSistemas(gerentes,vendedores)    
    else:
        print("Resposta inválida")
        resposta=""

