# Nuclio Lighting Flash

This repo builds a base image "GreenroomRobotics/nuclio_lighting_flash" which can be used to run flash ObjectDetection models in Nuclio / CVAT


## Usage

* Use [lightningflash-efficientdet-d0](./example/lightningflash-efficientdet-d0) as a reference example
* Modify/create your own as you see fit
* Deploy it:
```bash
nuctl deploy --project-name cvat \
  --path example/lightningflash-efficientdet-d0 \
  --platform local
```


## Development

### Get started

In order to develop you'll want a nuclio instance running on your local machine... 

* `docker-compose up` to start nuclio.
* `./scripts/build.sh` to build `ghcr.io/greenroom-robotics/nuclio_lighting_flash:latest`
* Deploy the example to your nuclio instance:

```bash
nuctl deploy --project-name cvat \
  --path example/lightningflash-efficientdet-d0 \
  --platform local
```

### Release a version

* Run the [Release](./.github/workflows/release.yml) workflow on github