FROM pytorchlightning/pytorch_lightning:1.6.4-py3.9-torch1.9
LABEL org.opencontainers.image.source=https://github.com/Greenroom-Robotics/nuclio_lighting_flash

# Remote nvidia lists as they have a borked GPG
RUN rm /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/cuda.list

# Install opencv deps
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Install lighting flash and it's deps
RUN pip install lightning-flash icevision 'lightning-flash[image]'

COPY ./nuclio_lighting_flash /opt/nuclio

WORKDIR /opt/nuclio

# Run the tests
# Nuclio will overwrite this CMD when it is deployed
CMD pytest . -vv