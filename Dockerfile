# wispysvr Dockerfile

FROM python:3.6.2-jessie
ADD . /wispysvr
WORKDIR /wispysvr
RUN pip install -U pytest && \
    pip install pytest-cov && \
	pip install -r requirements.txt
ENV APP_CONFIG=config.cfg
CMD python wispysvr.py
