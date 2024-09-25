# Book Recomendation Algorithm

## Index
- [Starting Application](#starting-application)
- [Code Structure](#code-structure)
  - [Prerequisite](#prerequisite)
  - [Classes and Data Types](#classes-and-data-types)
    - [1. Users](#1-users)
    - [2. Book](#2-book)
    - [3. Database](#3-database)
    - [4. Datatype](#4-datatype)
  - [Algorithm](#algorithm)
    - [Functions](#functions)
    - [Execution](#execution)
    - [Example](#example)

## Starting Application
Clone o repositório para um diretório pelo comando:

```shell
git clone <URL_REPOSITORY> <DIRECTORY_OF_DESTINY>
```

Primeiramente será necessárioa realizar a instalação da biblioteca `panda` através do seguinte comando:

```shell
pip install pandas
```

Para executarmos os código precisamos apenas executar o arquivo `recomendation_algorithm.py` com o comando, dentro do diretório do projeto:

```shell
python recomendation_algorithm.py
```

## Code Structure

### Prerequisite
- Python >= 3.12

### Classes and Data Types
#### 1. Users

Classe utilizada para criação do objeto utilizado como dados do usuário

```python
class User:
    def __init__(self, nome: str, generoPref: str, autorPref: str, anoPref: int) -> None:
        self.nome = nome
        self.generoPref = generoPref
        self.autorPref = autorPref
        self.anoPref = anoPref
```

#### 2. Book

Classe inexistente no código, mas sua estrutura é utilizado nas tabelas de dados e como parâmetros de avaliação dos gostos do usuário

```python
# Exemplo de classe
class Book:
    def __init__(self, nome: str, genero: str, autor: str, ano: int) -> None:
        self.nome = nome
        self.genero = genero
        self.autor = autor
        self.ano_de_publicacao = ano_de_publicacao
```

#### 3. Database
Foi utilizado como fonte de dados um arquivo CVS com 150 livros reais com a estrutura mostrada acima;

- Locale: `@/database/livros.csv`

#### 4. Datatype
Dentro da estrutura do código, além das classes pré-definidas e os tipos padrão, foi utilizada o tipo `DataFrame`

### Algorithm
#### Functions
O sistem possui apenas 3 funcções principais apenas, além da função `__main__` para inicialização do código.

- `remover_acentos(text)`: Funçõa para limpeza das Strings da aplicação, para uma melhor utilização das Strings dentro do sistema;

- `criar_usuario()`: Função de Inicialização do objeto dos dados do usuário;

- `recomendarLivros(pageSize: int, userRec: User)`: Função principal a qual armazena toda a lógica de validação dos livros com base nos gostos do usuário e retorna uma lista recomendada dos mais compatíveis com o usuário.

#### Execution

O sistema Inicia instânciado a classe User solicitando alguns dados para o usuário e executa a função de validação com o parâmetro de quantidade de livros recomendado como 15

```python
user = criar_usuario()
recomendarLivros(15, user)
# ...
```

Dentro da função `recomendarLivros` instanciamos em memória os dados do arquivo CSV para a variável ``. Logo em seguida, devido ao formato inicial da coluna `ano` vir como string foi executado uma conversão para inteiro.

```python
# ...
lista_livros = pd.read_csv(caminho_arquivo_entrada) # Instancia, lendo o CSV

lista_livros['ano_de_publicacao'] = pd.to_numeric(lista_livros['ano_de_publicacao'], errors='coerce') # Converte os dados da coluna ano_de_publicacao de string para inteiro
# ...
```

Após os preparos iniciais dos dados, setamos os parâmetros de validação dos livros. Comparando os seguintes critérios:
- Se o generos dos livros é o mesmo da preferência do usuário;
- Se o autor é o mesmo que o usuário tem preferência;
- se a data de publicação dos livros estão dentro de uma margem de 5 anos para mais ou para menos com base no ano de preferência do usuário;

```python
# ...
regra_livros = [
    lista_livros['genero'].str.lower() == userRec.generoPref, # Comparação do gênero do livro com a preferência do usuário

    lista_livros['autor'].str.lower().str.contains(remover_acentos(userRec.autorPref.lower()), na=False), # Comparação do autor do livro com o autor de preferência do usuário

    (userRec.anoPref - 5 <= lista_livros['ano_de_publicacao']) & (lista_livros['ano_de_publicacao'] <= userRec.anoPref + 5) # Comparação do ano de publicação do livro para dentro da margem de 5 anos com base no ano de preferência do usuário
]
# ...
```

Essas comparações quando executadas retornam um valor booleano, ou seja, verdadeiro ou falso.

A execução da mesma ocorre dentro de um laço de repetição no qual cada livro passa pelas 3 comparações, sendo realizado uma função de soma do retorno dos valores comparados. Devido a serem valores booleanos, a função da soma nesse caso faz a conversão automática para 1 em caso verdadeiro e 0 em caso falso.

Esses valores serão adicionados a uma coluna em outra variável do tipo `dataframe` para depois serem adicionadas a tabela original dos livros

```python
# ...
valor_filtros = sum(regra.astype(int) for regra in regra_livros) # Iteração em todos os livros, comparado valores, somado e salvo em uma variavel.

lista_livros['tier']= valor_filtros # Adicionado coluna a variavel original dos livros.
# ...
```

Com base nessa soma, essa coluna nova adicionada chamada `tier`, possui um valor variando de 0 a 3 o qual mostra quais livros, batem mais com os gostos dos usuário, sendo agora um valor de referência para quais livros tem melhor chance de ser uma boa escolha.

E no processo final de execução da função ordenamos a lista de livros com base em 2 critérios, sendo eles:

- Tier: Principal valor de referência em questão de proximidade com os gostos do usuário;
- Ordem Alfabética: Para uma ordenação imparcial, dentro dos grupos de Tiers, será ordenado por ordem alfabética do nome dos livros;

```python
# ...
lista_paginada_livros = lista_livros.sort_values(by=['tier','nome'], ascending=[False, True]) # Ordenação da lista com base primeiro em Tier e depois por ordem alfabética
# ...
```

Para finalização, é retornado estilizado no console a lista dos 15 livros mais recomendados em relação aos gostos do usuário

```python
#...
print(f"Livros recomendados para {userRec.nome}:")
print(f"{'Livro':<40} - {'Autor':<30} - {'Gênero':<15} - {'Ano':<5} - {'Tier'}")
print("=" * 100)  # Linha de separação
for _, row in lista_paginada_livros.head(pageSize).iterrows():
    ano_publicacao = int(row['ano_de_publicacao']) if not pd.isna(row['ano_de_publicacao']) else 'N/A'
    print(f"{row['nome']:<40} - {row['autor']:<30} - {row['genero']:<15} - {ano_publicacao:<5} - {row['tier']}")
```

#### Example
```
Digite seu nome: Usuário 1
Digite seu gênero literário preferido: Terror
Digite seu autor preferido: Stephen King
Digite seu ano de publicação preferido: 2000
Livros recomendados para Usuário 1:
Livro                                    - Autor                          - Gênero          - Ano   - Tier
====================================================================================================
À Espera de um Milagre                   - Stephen King                   - Terror          - 1996  - 3
Carrie, a Estranha                       - Stephen King                   - Terror          - 1974  - 2
IT - A Coisa                             - Stephen King                   - Terror          - 1986  - 2
Misery                                   - Stephen King                   - Terror          - 1987  - 2
O Iluminado                              - Stephen King                   - Terror          - 1977  - 2
Sobre a Escrita                          - Stephen King                   - Literatura      - 2000  - 2
À Espera de um Milagre                   - Stephen King                   - Drama           - 1996  - 2
A Caverna                                - José Saramago                  - Ficção          - 2002  - 1
A Guerra dos Tronos                      - George R.R. Martin             - Fantasia        - 1996  - 1
A Menina que Roubava Livros              - Markus Zusak                   - Histórico       - 2005  - 1
A Tenda Vermelha                         - Anita Diamant                  - Histórico       - 1997  - 1
Anatomia do Medo                         - S.L. Grey                      - Terror          - 2014  - 1
Artemis Fowl                             - Eoin Colfer                    - Fantasia        - 2001  - 1
Caçadores de Dragões                     - Eoin Colfer                    - Fantasia        - 2004  - 1
Crepúsculo                               - Stephenie Meyer                - Fantasia        - 2005  - 1
```