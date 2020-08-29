FROM python:3.7

RUN pip install pipenv

ENV PROJECT_DIR /srv/package_visualizer_backend

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
COPY resources ${PROJECT_DIR}/resources
COPY src ${PROJECT_DIR}/src

EXPOSE 80/udp
EXPOSE 80/tcp

RUN pipenv install --system --deploy

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]