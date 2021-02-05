# Parking Get Smart - Data Hub

It is a generic version of Parkkihubi (https://github.com/City-of-Helsinki/parkkihubi) datahub, which is Django-based REST API for processing parking data. There were made changes to original parkkihubi, to allow easier deployment of the hub for other cities.

## Getting Started

The whole application was dockerized and it is ready for easy deployment. Below are summarized all variables and files necessary for proper working of the hub.

### Prerequisites

For work with the hub you need to install docker (https://docs.docker.com/get-docker/) and docker-compse (https://docs.docker.com/compose/install/) before. Please check links given before for your platform installation procedures.


### Running

To run database, web application and dashboard you need to simply run command
```
docker-compose up
```
this will run three docker containers based on your environment variables.

Sample user:
```
Login: admin
Password: pass
```

If you don't want to add all variables to your environment, then create `.env` file with all the properties below and then run docker with the following command:
```
docker-compose --env-file .env up
```

#### Environment variables

Environmental variables for local deployment (via docker-compose) are stored in `.env` file.

#### Geospatial data

Below are shown how geospatial data should be formated.

##### Parking areas

```json
{
  "type": "FeatureCollection",
  "name": "parking_areas",
  "features": [
  {
    "type": "Feature",
    "properties": {
      "origin_id": INT
    },
    "geometry": {
      "type": "MultiPolygon",
      "coordinates": [ [ [ [ Longitude, Latitude ], ... ] ] ]
    }
  }, ...
  ],
}
```

##### Payment zones

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [[[[ Longitude, Latitude ], ... ] ] ]
      },
      "properties": {
        "name": "STRING",
        "number": INT
      }
    }, ...
  ]
}
```

##### Regions

```json
{
  "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "name": "STRING"
        },
        "geometry": {
          "type": "MultiPolygon",
          "coordinates": [ [ [ [ Longitude, Latitude ], ... ] ] ]
        }
      }, ...
    ]
}
```

##### Parking terminals

```json
[
  {
    "model": "parkings.parkingterminal",
    "pk": UUID,
    "fields": {
      "created_at": "2019-01-01T00:00:00.000Z",
      "modified_at": "2019-01-01T00:00:00.000Z",
      "number": INT,
      "name": "STRING",
      "location": "POINT(Longitude, Latitude)"
    }
  }, ...
]
```

### Generating API documentation

The API documentation conforms to [Swagger Specification 2.0](http://swagger.io/specification/).

Three possible ways (out of many) to generate the documentation:

- Run the documentation generating script:

      ./generate-docs

  The output will be in `docs/generated` directory by default.  If you
  want to generate to a different directory, give that directory as the
  first argument to the script.

- [bootprint-openapi](https://github.com/bootprint/bootprint-openapi)

    Probably the recommended way.

    Installation:

      npm install -g bootprint
      npm install -g bootprint-openapi

    Running (in `parkkihubi` repository root):

      bootprint openapi docs/api/enforcement.yaml </output/path/enforcement/>
      bootprint openapi docs/api/operator.yaml </output/path/operator/>

- [swagger-codegen](https://github.com/swagger-api/swagger-codegen)

    Due to [a bug in swagger-codegen](https://github.com/swagger-api/swagger-codegen/pull/4508),
    we're using an unreleased version at the moment.

    To build swagger-codegen from source, you need Apache maven installed (you'll
    need java 7 runtime at a minimum):

        # Ubuntu
        sudo apt-get install maven

    Clone swagger-codegen master branch and build it:

        git clone https://github.com/swagger-api/swagger-codegen
        cd swagger-codegen/
        mvn clean package  # Takes a few minutes

    The client will now be available at `modules/swagger-codegen-cli/target/swagger-codegen-cli.jar`.

    To build the docs, in `parkkihubi` repository root:

        cd docs/api
        java -jar /path/to/codegen/swagger-codegen-cli.jar generate \
          -i enforcement.yaml -l html2 -c config.json \
          -o /output/path/enforcement/
        java -jar /path/to/codegen/swagger-codegen-cli.jar generate \
          -i operator.yaml -l html2 -c config.json \
          -o /output/path/operator/

### Acknowledgement

In the framework of project “PARKING GETS SMART – improved & digitalised parking management as a tool to foster green and multimodal transport in the South Baltic Area” co-financed from European Regional Development Fund

![Alt text](logo.jpg)

Disclaimer: the contents of this code are the sole responsibility of the authors and can in no way be taken to reflect the views of the European Union, the Managing Authority or the Joint Secretariat of the South Baltic Cross-border cooperation programme 2014-2020
