import pandas as pd
import string
import unidecode
import time
import os

df = pd.read_csv(r"br-capes-bolsistas-uab.csv", sep=';', encoding='latin-1')



def media_ano(ano_informado):

    coluna_ano_solicitado = df.loc[ df['AN_REFERENCIA'] == ano_informado, 'VL_BOLSISTA_PAGAMENTO']  # Separando  os valores pelo ano informado
    print(f'A Média dos valores das bolsas do ano de {ano_informado} é aproximadamente R$ {coluna_ano_solicitado.mean():.2f}')



def editar_texto(nome):
    
    nome = nome.upper() # Transformando para Maiúsculo
    nome = unidecode.unidecode(nome) # Retirando Acentos
    
    for letra in nome:
        if letra.isalnum() == False: # verificando se há caracter especial
             nome = nome.replace(letra, "") # Trocando o  caracter especial por "nada"
        
    return(nome)  



def codificador(nome): 
    nome_junto = []
    vet_nome = []
    alfabeto = string.ascii_uppercase #Criando um vetor com o alfabeto MAIUSCULO
        
    for nome in nome.split():
        
        nome = nome[-1:] + nome[1:-1] + nome[:1]  # Fazendo o swap da primeira com a última letra
        if len(nome) >= 4:                       # Se a palavra tiver menos de 4 letras só o swap é necessário, senao, temos que inverter
            nome = nome[::-1]                   # Invertendo a string
        # For´s para mudar letra por letra
        for j in range(len(nome)):
            for i in range(len(alfabeto)):
                if nome[j] == alfabeto[i]:
                    if nome[j] == 'Z':      #Z é especial pois é o ultimo do vetor, então não existira um próximo
                        letra_new = nome[j].replace('Z', 'A')
                        vet_nome.append(letra_new)
                    else:   
                        letra_new = nome[j].replace(nome[j], alfabeto[i+1])  # Mudando para o próximo carácter
                        vet_nome.append(letra_new)

                                                                          #vet_nome = ['a','b','c']  -> .join -> vet_nome = ['abc']
        nome_junto.append("".join(vet_nome)) 
        vet_nome.clear() 
        

    aux = " ".join(nome_junto)  
    return(aux)



while True:
    time.sleep(1.5)

    print(''' 
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    
    Bem Vindo, escolha uma opção abaixo!
      
    [1] Consulta Bolsa Zero/Ano
    [2] Codificar Nomes
    [3] Consultar Média Anual
    [4] Ranking Valores de Bolsa
    [5] Terminar Programa
    
    ''')
    try:
     # Try para garantir que o que for digitado sera válido para inteiro
        opcao_escolhida = int(input("Escolha uma opção: "))
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

        if opcao_escolhida == 1: 

            try:
                ano = int(input("Informe o ano para consultar a primeira bolsa: "))

                if ano <= df['AN_REFERENCIA'].max() and ano >= df['AN_REFERENCIA'].min():
                    localiza = df.loc[df['AN_REFERENCIA'] == ano]   # Localizando e separando somente as linhas que tem o ano correspondente ao informado.
                    #iloc[linhas, coluna]
                    print(f''' \n O bolsista 0 em {ano}:
                    
                    Nome = {localiza.iloc[0, 0]}                
                    CPF  = {localiza.iloc[0, 1]}
                    Nome da Entidade de Ensino = {localiza.iloc[0, 2]}
                    Valor da Bolsa = {localiza.iloc[0, -1]} 
                    
                    ''')
                else:
                    print('Err... Não encontramos nenhum bolsista no ano digitado.') 
            except:
                print('Oops, parece que você não digitou um ano em formato numérico.')



        if opcao_escolhida == 2:

            try:
                nome_completo = input(str("Digite o nome do bolsista que deseja procurar: "))
                nome_completo = nome_completo.split() # Separando cada nome digitado como se fosse um item do vetor, para facilitar o tratamento

                nomes_codificados_vetor = []
                nome_editado = []

                for nome in nome_completo:
                    nome_editado.append(editar_texto(nome)) # Exemplo nome_editado = ['JOAO', 'VITOR']


                # For que acha o bolsista mesmo se a pessoa não digitar o nome dele em ordem ou completo.
                nome_bolsistas_completo = []
                for nome_bolsista in df['NM_BOLSISTA']:  
                    iguais = set(nome_editado).intersection(nome_bolsista.split())  # Verifica quais itens dos vetores são iguais.
                    if len(iguais) == len(nome_editado):          # Se todos itens forem iguais, então os vetores tem tamanho iguais,
                        nome_bolsistas_completo.append(nome_bolsista)   # isso signififca que encontramos as pessoas procurada.
                        
                         
                for nome in nome_bolsistas_completo: # Codificando os nomes
                    nomes_codificados_vetor.append(codificador(nome)) 

                vet = []                      
                nome_bolsistas_completo = sorted(set(nome_bolsistas_completo)) #Removendo nomes duplicados.
                for nome in nome_bolsistas_completo:       # Achando os valores que iremos exibir para o respectivo nome
                    a = df.loc[df['NM_BOLSISTA'] == nome, ['AN_REFERENCIA', 'NM_ENTIDADE_ENSINO', 'VL_BOLSISTA_PAGAMENTO']]
                    vet.append(a)
                    
                df_infos_bolsistas_completos = pd.concat(vet)  # Transoformando em data frame
                
                for i, nome in enumerate(nomes_codificados_vetor):
                    print(f''' 
                    Nome Codificado: {nome}
                    Ano: {df_infos_bolsistas_completos.iloc[i,0]}                                
                    Entidade de Ensino: {df_infos_bolsistas_completos.iloc[i,1]}         
                    Valor da Bolsa: {df_infos_bolsistas_completos.iloc[i,2]}
                    ''') 

                
                                          
            except:
                print("Não encontramos o nome informado na nossa base de dados. Por favor, tente novamente!")
                
              

        if opcao_escolhida == 3: 

            try:     
                ano_informado = int(input('Informe o ano que deseja para saber a média das bolsas: '))
                if ano_informado <= df['AN_REFERENCIA'].max() and ano_informado >= df['AN_REFERENCIA'].min():  #Verifica se o ano informado está entre limites da tabela
                    media_ano(ano_informado)
                else:
                    print('Err... Não foi encontrado nenhum registro no ano solicitado.')    
            except: 
                print('Oops, parece que você não digitou um ano em formato numérico válido para Ano.')
            


        if opcao_escolhida == 4:

            bolsas_maiores = df.sort_values(by='VL_BOLSISTA_PAGAMENTO', ascending = False).head(3)   # Cria e ordena um novo Data Frame com as bolsas 3 bolsas na ordem desejada.
            bolsas_menores = df.sort_values(by='VL_BOLSISTA_PAGAMENTO', ascending = True).head(3)

            print('Bolsas Mais Baixas: ')
            for i in range(len(bolsas_menores)):
                print(f'''
                Nome: {bolsas_menores.iloc[i,0]}                    
                Valor da Bolsa: {bolsas_menores.iloc[i,-1]}   ''') #iloc[linha, coluna] "procurar na linha o valor correspondente na coluna tal."
                
            print('\n Bolsas Mais Altas: ')
            for i in range(len(bolsas_maiores)):
                print(f'''
                Nome: {bolsas_maiores.iloc[i,0]} 
                Valor da Bolsa: {bolsas_maiores.iloc[i,-1]} 
                ''') 


        if opcao_escolhida == 5:
            print("-=-=-=-=-=-=-==--=-==-=-=-=-=-=-=-=")
            print("\n Programa Finalizado, Hasta la Vista Muchachos! \n")
            print("-=-=-=-=-=-=-==--=-==-=-=-=-=-=-=-=")
            os._exit(0)     #Encerrar programa

        if opcao_escolhida > 5 :
            print("Por favor, insira um número de 1 a 5") 
            

    except:
        print("\n Por favor, digite um número válido") 