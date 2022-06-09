# Nuclio Lighting Flash

This repo builds a base image [ghcr.io/greenroom-robotics/nuclio_lighting_flash:latest](https://github.com/Greenroom-Robotics/nuclio_lighting_flash/pkgs/container/nuclio_lighting_flash) which is used to conveniently run flash ObjectDetection models in Nuclio / CVAT. It allows you to configure the model `head`, `backbone` and `checkpoint_path` from your nuclio `function.yml`

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

### Run tests

* `./scripts/build.sh && docker run ghcr.io/greenroom-robotics/nuclio_lighting_flash:latest` to build and run pytests

### Release a version

* Run the [Release](./.github/workflows/release.yml) workflow on github