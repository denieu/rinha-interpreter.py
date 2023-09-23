![banner](docs/assets/banner.png "Rinha de Compiler Logo")

# Introdução

Interpretador da liguagem exotica rinha escrito em 🐍 Python.

Para saber mais sobre a linguagem ou sobre a Rinha de Compiler da uma olhada [aqui](https://github.com/aripiprazole/rinha-de-compiler).

## Docker

Para buildar a imagem Docker:
```bash
docker build . -f Dockerfile -t rinha-interpreter
```

Para executar a imagem Docker:
```bash
# Substitua o caminho "$(pwd)/files/fib.json" pelo arquivo(AST json) que desejar
docker run -v $(pwd)/files/fib.json:/var/rinha/source.json rinha-interpreter
```