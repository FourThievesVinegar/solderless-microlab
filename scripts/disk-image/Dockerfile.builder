FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install all tools needed for scripts/build-image.sh
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      bash \
      curl \
      ca-certificates \
      unzip \
      xz-utils \
      git \
      qemu-user-static \
      util-linux \
      parted \
      kpartx \
      e2fsprogs \
      vim-tiny \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspace
COPY . /workspace

# Ensure our scripts are executable
RUN chmod +x /workspace/scripts/*.sh

# Default to an interactive shell; override in docker run if desired
CMD ["bash"]
