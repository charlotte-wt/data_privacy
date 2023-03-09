FROM gcc

WORKDIR /usr/src

COPY pbc-0.5.14 ./pbc-0.5.14
COPY libbswabe-0.9 ./libbswabe-0.9
COPY cpabe-0.11 ./cpabe-0.11

COPY setup-cpabe.sh .

RUN sh setup-cpabe.sh

CMD ["/bin/bash"]