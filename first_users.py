from classes.user import User
import pandas as pd
import unicodedata

caminho_arquivo_entrada = 'database/livros.csv'

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def recomendarLivros(pageSize: int, userRec: User):
    lista_livros = pd.read_csv(caminho_arquivo_entrada)
    lista_livros['ano_de_publicacao'] = pd.to_numeric(lista_livros['ano_de_publicacao'], errors='coerce')
    # print(lista_livros)
    
    regra_livros = [
        lista_livros['genero'].str.lower() == userRec.generoPref,
        lista_livros['autor'].str.lower().str.contains(remover_acentos(userRec.autorPref.lower()), na=False),
        (userRec.anoPref - 5 <= lista_livros['ano_de_publicacao']) & (lista_livros['ano_de_publicacao'] <= userRec.anoPref + 5)
    ]

    valor_filtros = sum(regra.astype(int) for regra in regra_livros)

    lista_livros['tier']= valor_filtros

    lista_paginada_livros = lista_livros.sort_values(by=['tier','nome'], ascending=[False, True])

    print(f"Livros recomendados para {userRec.nome}:")
    for _, row in lista_paginada_livros.head(pageSize).iterrows():
        print(f"{row['nome']} - {row['autor']} - {row['ano_de_publicacao']} - {row['tier']}")

def criar_usuario():
    nome = input("Digite seu nome: ")
    generoPref = input("Digite seu gênero literário preferido: ").lower()
    autorPref = remover_acentos(input("Digite seu autor preferido: ")).lower()
    anoPref = int(input("Digite seu ano de publicação preferido: "))
    
    return User(nome=nome, generoPref=generoPref, autorPref=autorPref, anoPref=anoPref)

if __name__ == "__main__":
    user = criar_usuario()
    recomendarLivros(15, user)