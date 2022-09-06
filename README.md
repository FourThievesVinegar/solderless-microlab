# FTVC Solderless Microlab

An open source jacketed lab reactor made from off-the-shelf components you can buy online.

Read the motivation behind the project here: [docs/motivation.md](docs/motivation.md)

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
docker-compose up --build gui
```

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

(for macOS)

```text
$ brew update
$ brew install python3
$ pip3 install virtualenv
```

Set up a Python virtual environment:
virtualenv -p python3 env

```text
$ cd backend
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

##### Redis

(on the Pi)

```text
sudo apt -y install screen git redis-server python-celery-common python3-flask python3-pip python3-rpi.gpio python3-serial

```

(for Debian / Ubuntu)

```text
sudo apt update
sudo apt install redis-server
```

To run Redis as a service,

```text
sudo nano /etc/redis/redis.conf
```

and change the option for `supervised` from `no` to `systemd`

#### Startup celery worker:

```text
(env) $ celery -A recipes worker --loglevel=INFO
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

To run the software without a functioning hardware environment, set the following configs:

In `/solderless-microlab/backend/config.py`:

```
hardwarePackage = 'simulation'
```

The hardwareSpeedup option can be modified to make steps that take a long time execute quicker for testing purposes.

## API Spec

API spec is very flexible and will change as development goes on.

### Hardware Tests

#### GET /test/relays

Test the relay shield. All four relays are turned on and off.

## Acknowledgements

### Volunteers

Thanks to the whole 4TV crew whose efforts both tired and tireless have brought the project this far!

### Works used

Thanks to The Noun Project for icons: Temperature by Megan Chown, Syringe by shashank singh, looking by Lewis K-T, Jar by Marie Larking, Chemistry by Victoruler
