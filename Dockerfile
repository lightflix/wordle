FROM python:3.11-rc-buster

RUN mkdir -p ./wordle

ADD static ./wordle/static
ADD templates ./wordle/templates
ADD guess_list.txt answer_list.txt wordle.py ./wordle/

RUN pip install flask

WORKDIR /wordle/

CMD ["python","-u","wordle.py"]