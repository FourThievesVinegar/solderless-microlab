# FTVC Solderless Microlab

An open source jacketed lab reactor made from off-the-shelf components you can buy online.

## Setup

Clone the repo:

```text
$ git clone https://github.com/FourThievesVinegar/solderless-microlab.git
$ cd solderless-microlab
```

### API Server

Add dependencies:

```text
$ sudo apt update
$ sudo apt install python3 python3-pip python-virtualenv python3-virtualenv
```

Set up a Python virtual environment:

```text
$ cd backend
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

Start the server:

```text
(env) $ python main.py
```

### Web GUI

Follow a guide to install yarn for Debian:

https://classic.yarnpkg.com/en/docs/install/#debian-stable

In summary:

```text
$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
$ sudo apt update
$ sudo apt install yarn
```

Run the GUI:

```text
$ cd gui
$ yarn install
$ yarn start
```

The GUI will now be listening on port 3000.

## API Spec

API spec is very flexible and will change as development goes on.

### Hardware Tests

#### GET /test/relays

Test the relay shield. All four relays are turned on and off.
