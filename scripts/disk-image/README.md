# microlab-image

**microlab-image** provides everything needed to build a Raspberry Pi OS image pre-configured for the solderless-microlab.

## Repository layout

- **.github/workflows** – CI to build & publish nightly Pi images  
- **config/** – bootloader and kernel-args overrides  
- **overlays/** – rootfs overlay (scripts, notebooks, configs)  
- **scripts/** – image assembly and provisioning scripts  

## Prerequisites

- *nix 
- Docker (Rancher Desktop, Docker Desktop, etc)

## Quick start

```bash
# 1. Clone
git clone https://github.com/FourThievesVinegar/microlab-image.git
cd microlab-image

# 2. Build
#  Follow `BUILD.md`

# 3. Flash
#    resulting image lives in build/raspios-microlab.img
```

## Raspberry Pi default credentials

* User: thief
* Password: vinegard
