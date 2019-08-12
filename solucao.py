import requests
import time
import json
import hashlib


def requisicao(token):
    r = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data', params = token)
    
    if r.status_code == 200:
        return json.loads(r.content.decode('utf-8'))
    else:
        return None


def descriptografia_de_cesar(resposta):
    decifrado = ''  

    for i in resposta["cifrado"]:
        if ord(i) > 96 and ord(i) < 123:
            decifrado += chr(ord(i) - resposta["numero_casas"])
        else:
            decifrado += i

    return decifrado


def algoritmo_sha1(decifrado):
    h = hashlib.sha1()
    h.update(decifrado.encode('utf-8'))

    return h.hexdigest()    


def escrevendo_arquivo(resposta):
    j = json.dumps(resposta)
    arquivo = open('answer.json', 'w')
    arquivo.write(j)
    arquivo.close()


def submeter(token):
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution'
    files = {'answer': open('answer.json', 'rb')}
    r = requests.post(url, params=token, files=files)

    print(r.status_code)
    print(r.content.decode('utf-8'))


def main():
    inicio = time.time()
    
    token = {'token': 'f00f60d2e05de20d1bb7ea6ea3db3d00a6c820c1'}  

    resposta = requisicao(token)                # Faz requisição http get

    decifrado = descriptografia_de_cesar(resposta)          # Decifra a frase conforme o criptografia de césar
    
    resposta["decifrado"] = decifrado           # Atualiza a frase decifrada

    resumo = algoritmo_sha1(decifrado)          # Algoritmo sha1 para criptografar a frase decifrada

    resposta['resumo_criptografico'] = resumo   # Atualizar o resumo conforme o algoritmo sha1

    escrevendo_arquivo(resposta)                # Escreve tudo em um arquivo json
    
    submeter(token)                             # Faz requisição http post

    fim = time.time()
    print(fim - inicio)

    return 0


if __name__ == "__main__":
    main()