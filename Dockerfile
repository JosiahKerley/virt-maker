FROM python:3.9 as builder

WORKDIR /app

COPY . .

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    /venv/bin/pip install build && \
    /venv/bin/python -m build

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app/dist/virt_maker-*.whl ./
COPY --from=builder /venv /venv

RUN apt-get update && \
    apt-get install -y \
        xz-utils \
        openssh-client \
        libguestfs-tools \
        qemu-kvm \
        wget \
        xz-utils \
        lz4 \
        pv \
        qemu-utils \
        coreutils \
        gzip && \
    /venv/bin/pip install virt_maker-*.whl

ENTRYPOINT ["/venv/bin/virt-maker"]