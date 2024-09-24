FROM python:3.12.4
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["poetry", "run", "streamlit", "run", "pdi_rickandmorty/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["poetry", "run", "python", "pdi_rickandmorty/main.py"]