FROM python:3.11.5

WORKDIR /var/rinha-interpreter

COPY . .

RUN pip install .[build]

RUN python cythonizer.py build_ext --inplace

CMD ["rinha-interpreter", "/var/rinha/source.rinha.json"]
