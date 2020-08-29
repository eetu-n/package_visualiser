FROM python:3.7

RUN pip install pipenv

ENV PROJECT_DIR /srv/package_visualizer_backend

WORKDIR ${PROJECT_DIR}

COPY resources src Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]