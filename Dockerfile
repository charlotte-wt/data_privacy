FROM gcc

WORKDIR /usr/src

COPY pbc-0.5.14 ./pbc-0.5.14
COPY libbswabe-0.9 ./libbswabe-0.9
COPY cpabe-0.11 ./cpabe-0.11

COPY data ./data

COPY . .

RUN sh setup-cpabe.sh

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

CMD ["/bin/bash"]