FROM nvidia/cuda:12.1.1-base-ubuntu22.04
FROM docker.io/pytorch/pytorch

ARG service_home="/home/EasyOCR"

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev python-is-python3 && \
    rm -rf /var/lib/apt/lists/*

# Configure apt and install packages
RUN apt-get update -y && \
apt-get install -y \
libglib2.0-0 \
libsm6 \
libxext6 \
libxrender-dev \
libgl1-mesa-dev \
git \
# cleanup
&& apt-get autoremove -y \
&& apt-get clean -y \
&& rm -rf /var/lib/apt/lists

# Clone EasyOCR repo
RUN mkdir "$service_home" \
    && git clone "https://github.com/JaidedAI/EasyOCR.git" "$service_home" \
    && cd "$service_home" \
    && git remote add upstream "https://github.com/JaidedAI/EasyOCR.git" \
    && git pull upstream master

# Build
RUN cd "$service_home" \
    && python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

WORKDIR /WebOCR

RUN pip3 install Flask
RUN pip3 install manga_ocr
RUN pip3 install deep_translator
RUN pip3 install pillow

COPY . .

CMD ["python", "web.py"]