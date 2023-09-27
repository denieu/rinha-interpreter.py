FROM python:3.11.5-alpine3.18

WORKDIR /var/rinha-interpreter

COPY . .

RUN pip install .

CMD ["rinha-interpreter", "/var/rinha/source.rinha.json"]
