FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    libtiff5 \
    build-essential \
    wget \
    git \
    curl

RUN mkdir -p /miniconda3 \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda3/miniconda.sh \
    && bash /miniconda3/miniconda.sh -b -u -p /miniconda3 \
    && rm -rf /miniconda3/miniconda.sh

ENV PATH="/miniconda3/bin:${PATH}"
RUN conda init bash \
    && conda init zsh

WORKDIR /chat-bot-aitana
COPY . /chat-bot-aitana

RUN conda env create -f environment-ubuntu.yml

ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["conda run --no-capture-output -n AitanaENV chainlit run chainlit-chat.py -w"]