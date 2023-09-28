![banner](docs/assets/banner.png "Rinha de Compiler Logo")

# Introdução

Interpretador da liguagem exotica rinha escrito em 🐍 Python.

Para saber mais sobre a linguagem ou sobre a Rinha de Compiler da uma olhada [aqui](https://github.com/aripiprazole/rinha-de-compiler).

⚠️⚠️⚠️Esse código não é nem um pouco pensado para produção, problemas existem e foram mantidos propositalmente visando performance ⚠️⚠️⚠️.

## Ideia do Interpretador

Foi implementado um tree-walking interpreter que basicamente: 
1. Le a arvore sintática abstrata(AST) do JSON no path informado no primeiro parametro da CLI
2. Interpreta o nó da arvore
3. Segue para o proximo nó (se houver)
4. Volta para o passo 2

Implementei algumas otimizações no interpretador buscando deixar o código mais performantico, são essas:

* Tail Call Optimization:

    Eliminei totalmente a recursão do interpretador, contornando erros como RecursionError, comuns em Python.

* Cache das chamadas internas de função:

    Visto que a linguagem Rinha é "imutavel" sempre que uma mesma função for chamada com um mesmo parametro o resultado será o mesmo, dito isso estou cacheado os resultados das funções e os retornando diretamente.

As duas melhorias descritas acima permitiram o calculo do fib(10000) de forma quase instantanea.

## Executando Localmente

Comece instalando as dependencias:
```bash
pip install .
```

Para executar o interpretador:
```bash
rinha-interpreter {PATH_PARA_AST_JSON}
# ou
hatch run rinha-interpreter {PATH_PARA_AST_JSON}
# ou
python -m rinha_interpreter.main {PATH_PARA_AST_JSON}
```

Para mais ajuda:
```bash
rinha-interpreter --help
# ou
hatch run rinha-interpreter --help
# ou
python -m rinha_interpreter.main --help
```

## Executando Localmente Com Docker

Para buildar a imagem Docker:
```bash
docker build . -f Dockerfile -t rinha-interpreter
```

Para executar a imagem Docker:
```bash
# Substitua o caminho "$(pwd)/examples/fib.json" pelo arquivo(AST json) que desejar
docker run -v $(pwd)/examples/fib.json:/var/rinha/source.rinha.json rinha-interpreter
```
