FROM python:3.7.6

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
  libpq-dev \
  postgresql \
  postgis \
  binutils \
  libproj-dev \
  gdal-bin
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN ["chmod", "+x", "run_app.sh"]

CMD ["run_app.sh"]