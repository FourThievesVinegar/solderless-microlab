# Microlab

The MicroLab is an open-source, DIY, automated controlled lab reactor (CLR) that people can assemble with parts available online. We hope this will do for chemistry what the 3D printer did for manufacturing: provide a DIY, hackable, low-cost method to design and produce certain needful things that otherwise would be out of reach.

<IMG ALT="MicroLab fully assembled with all units" SRC="https://fourthievesvinegar.org/wp-content/uploads/2024/07/microlab-stirring-3.gif" width="600" />

## The MicroLab Suite

For the MicroLab to be accessible to the most people, it was developed as part of a hardware/software stack called the MicroLab Suite. The different software programs help take the information about a compound you want to make and translate it into a recipe (code) that the MicroLab runs to create the compound.

You can find an introduction to the project, what the heck is a CLR, what's in the MicroLab Suite, and why we are doing this at all on the [About the MicroLab and MicroLab Suite](docs/motivation.md) page.

## Getting Started Making Your MicroLab

This section is for you if you want to build a MicroLab and start using it. We tried to make building the MicroLab friendly for folks newer to electronics, but you will need some knowledge and skills with electronics (or the patience to learn a few things).

- Learn [About the MicroLab and MicroLab Suite](docs/motivation.md) so you have an understanding of what you are building.
- **Start here for [How to build & use the MicroLab and MicroLab Suite](docs/index.md)**

## Getting Started Developing the MicroLab

<IMG ALT="MicroLab architecture diagram" SRC="./docs/media/ML_architecture.jpeg" width="1000" />

This section is for you if you want to help develop the MicroLab and will need to tinker with the code base.  

You will need to get a copy of the MicroLab software, set up your development environment either with a Docker container or locally on your computer.

### Installing the MicroLab software locally

Use the instructions below for a fresh install of the MicroLab software (backend and GUI) on your development machine.

If you intend to construct a full MicroLab, [we recommend using our pre-made disk images](https://fourthievesvinegar.org/microlab/). There are two:

- A "production" image that runs all software on startup and includes the drivers for a goodtft-compatible 3.5 inch mini-display. This is the software you need if you have assembled a MicroLab and you want to use it to run reactions.
- A "development" image designed to be used with an external HDMI monitor and a USB mouse and keyboard. This would be the software to run on a computer where the MicroLab hardware can be emulated.

If you are using the development image and running it on a computer with emulated hardware turn on, follow the instructions below.

## Dev Environment Option 1: Docker Development

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

## Dev Environment Option 2: Laptop Setup

Clone the repo:

```bash
git clone https://github.com/FourThievesVinegar/solderless-microlab.git
cd solderless-microlab
```

### API Server

#### Install dependencies:

##### Python

(for Debian / Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip python-virtualenv python3-virtualenv
```

Note: some versions of Linux have dropped support for Python2 and `python-virtualenv`.

(for macOS)

```bash
brew update
brew install python3
pip3 install virtualenv
```

Set up a Python virtual environment:
virtualenv -p python3 --system-site-packages env

```bash
cd backend
virtualenv -p python3 --system-site-packages env
source env/bin/activate
(env) $ pip install -r requirements.txt
```

##### Install needed packages

(on the Pi)

```bash
sudo apt -y install screen git python3-flask python3-pip python3-serial python3-libgpiod

```

#### Start the server

```bash
(env) $ python main.py
```

### Web GUI

#### Install dependencies

(for Debian / Ubuntu)

Follow a guide to install yarn for Debian:

https://classic.yarnpkg.com/en/docs/install/#debian-stable

In summary:

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install yarn
```

(for macOS)

```bash
brew update
brew install yarn
```

#### Run the GUI:

```bash
cd gui
yarn install
yarn start
```

The GUI will now be listening on port 3000.

## MicroLab Hardware Options

### Hardware Emulation

To run the software without a functioning hardware environment, go to the settings menu and change the "MicroLab Controller" setting to "simulation-pi" and "Lab Hardware Config" to "ftv_simulation_microlabv0.5.0"

### MicroLab Setup - Enabling SSH

If you have a MicroLab to run the software on, you may want to enable SSH on the Pi. This makes remote development easier. Instructions for doing so can be found here: https://itsfoss.com/ssh-into-raspberry/

## Start Developing
Once your environment is setup, head on over to the [Backend README](/backend)
