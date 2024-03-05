FROM python:3.10-slim as worker
WORKDIR /worker

COPY . .
ADD requirements.txt requirements.txt

RUN apt-get update
RUN apt-get install xvfb -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN playwright install && \
    playwright install-deps
RUN echo "Installed dependencies for worker"

CMD xvfb-run --server-args="-screen 0, 1600x900x24" --auto-servernum --server-num=1 python -m m_worker



#CMD sh -c "sleep 5 && python -m m_worker"

# && \
#    playwright install-deps