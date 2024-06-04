# FTVC Solderless Microlab

An open source jacketed lab reactor made from off-the-shelf components you can buy online.

<IMG ALT="Microlab fully assembled with all units" SRC="./docs/media/microlab-v0.6.0-assembled.jpg" width="600" />

An introduction to the project is here: [docs/index.md](docs/index.md)

Read the motivation behind the project here: [docs/motivation.md](docs/motivation.md)

The full replication and assembly instructions here: [docs/assembly.md](docs/assembly.md)

PLEASE NOTE: These docs are in pre-release for v0.6. They are not considered complete and we are still finalizing some hardware recommendations. That said, if tinkering is your thing, you should be fine.

## Production vs Development

The instructions below are for a fresh install of the Microlab software (backend and GUI) on your development machine. If you intend to construct a full Microlab, [we recommend using our pre-made disk images](https://fourthievesvinegar.org/microlab/). There are two: 
- A "production" image that runs all software on startup and includes the drivers for a goodtft-compatible 3.5 inch mini-display. 
- A "development" image designed to be used with an external HDMI monitor and a USB mouse and keyboard.

If you wish to develop on a regular computer with emulated hardware, follow the instructions below.

## Docker Development

For ease of setup/experimentation we added docker containers for both the GUI and the API.
If you don't have docker-compose installed on your system you can install docker desktop following [these docs](https://docs.docker.com/compose/install/)

```bash
git clone https://github.com/FourThievesVinegar/solderless-microlab.git
cd solderless-microlab

## To run API & GUI
docker-compose up --build gui

## Alternatively
## To run just the API
docker-compose up --build api
```

If you're running docker with a hardware setup you'll need to edit docker-compose.yml and uncomment the lines specified in the file.

## Setup

Clone the repo:

```text
$ git clone https://github.com/FourThievesVinegar/solderless-microlab.git
$ cd solderless-microlab
```

### API Server

#### Install dependencies:

##### Python

(for Debian / Ubuntu)

```text
$ sudo apt update
$ sudo apt install python3 python3-pip python-virtualenv python3-virtualenv
```
Note: some versions of Linux have dropped support for Python2 and `python-virtualenv`.

(for macOS)

```text
$ brew update
$ brew install python3
$ pip3 install virtualenv
```

Set up a Python virtual environment:
virtualenv -p python3 --system-site-packages env

```text
$ cd backend
$ virtualenv -p python3 --system-site-packages env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

##### Install needed packages

(on the Pi)

```text
sudo apt -y install screen git python3-flask python3-pip python3-serial python3-libgpiod

```

#### Start the server:

```text
(env) $ python main.py
```

### Web GUI

#### Install dependencies:

(for Debian / Ubuntu)

Follow a guide to install yarn for Debian:

https://classic.yarnpkg.com/en/docs/install/#debian-stable

In summary:

```text
$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
$ sudo apt update
$ sudo apt install yarn
```

(for macOS)

```text
$ brew update
$ brew install yarn
```

#### Run the GUI:

```text
$ cd gui
$ yarn install
$ yarn start
```

The GUI will now be listening on port 3000.

## Hardware Emulation

To run the software without a functioning hardware environment, go to the settings menu and change the "Microlab Controller" setting to "simulation-pi" and "Lab Hardware Config" to "ftv_simulation_microlabv0.5.0"

## Enabling SSH

For ease of remote development, you may want to enable SSH on the Pi. Instructions for doing so can be found here: https://itsfoss.com/ssh-into-raspberry/
