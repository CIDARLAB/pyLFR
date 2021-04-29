# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.166.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}
# FROM ubuntu:20.04

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0


# [Optional] Uncomment this section to install additional OS packages.
RUN export DEBIAN_FRONTEND=noninteractive \
  && sudo apt-get update \  
  && apt-get -y install --no-install-recommends build-essential curl software-properties-common \
  python3-pip  git make build-essential python-dev libssl-dev zlib1g-dev \ 
  libbz2-dev libreadline-dev libsqlite3-dev curl libffi-dev \
  graphviz libgraphviz-dev \
  libcairo2-dev pkg-config python3-dev

# Things that didn't install -  make python3-dev

# Install and setup pyenv 
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.8.0
RUN pyenv global 3.8.0

RUN pip install pygraphviz

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false