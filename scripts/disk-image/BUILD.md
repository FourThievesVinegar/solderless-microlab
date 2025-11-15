### Building the Image on macOS via Docker

> These steps assume you have Docker toolchain installed on your Mac and that you have already cloned the repository into `microlab-image/`.

1. **Build the "builder" image**  
   From the project root (where `Dockerfile.builder` lives), run:
   ```bash
   docker build -f Dockerfile.builder -t microlab-image-builder .
   ```

2. **Register ARM translator**
   ```bash
   docker run --rm --privileged tonistiigi/binfmt --install all
   ```

3. **Run the build inside Docker**
   This will mount your workspace into the container, create loop devices, mount partitions, and invoke the standard build script. The `--privileged` flag is required so the container can manage loopback devices and mounts.

   ```bash
   # This will build the latest from the main branch
   docker run --rm --privileged -v "$(pwd)":/workspace microlab-image-builder \
        bash -lc "cd /workspace && bash scripts/build-image.sh"   
   ```
   
   To target a particular release tag, add it after the `build-image.sh` script

   ```bash
   # This will build from the v1.0.0 tag
   docker run --rm --privileged -v "$(pwd)":/workspace microlab-image-builder \
        bash -lc "cd /workspace && bash scripts/build-image.sh v1.0.0"   
   ```

4. **Retrieve your image**
   When the container finishes, you’ll find:

   ```
   microlab-image/build/raspios-microlab.img
   ```

   ready to flash to an SD card.

5. **(OPTIONAL) Troubleshoot the `microlab-image-builder` Docker Image**
   ```shell
   docker run --rm -it \ 
     --privileged \   
     -v "$(pwd)/build:/build:ro" \   
     --entrypoint /bin/bash \   
     microlab-image-builder
   ```

6. **(OPTIONAL) Inspect your image**
   ```bash
   docker run --rm -it \
     --privileged \
     -v "$(pwd)/build:/build:ro" \
     microlab-image-builder \
     /workspace/scripts/inspect-raspios-microlab.sh /build/raspios-microlab.img
   ```
