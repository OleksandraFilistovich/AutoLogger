FROM python:3.10-slim as orchestrator
WORKDIR /orchestrator

COPY . .

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN echo "Installed dependencies for orchestrator"

CMD sh -c "sleep 5 && python -m m_orchestrator"
