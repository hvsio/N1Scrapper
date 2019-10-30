FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8001
ENV PYTHONPATH="$PYTHONPATH:/app"
CMD python ./scrapper_service.py