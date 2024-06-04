# Solderless Microlab Backend

This project is a python service split into two different units. One controls the microlab hardware, and the other provides an API for getting the state of the microlab and for running recipes on it. The Microlab gui is the main consumer of this API.

## Starting up

See README.md in the root directory for instructions on running the service.

## Configuration

Some general configuration for the microlab can be found at `/etc/microlab` after running the backend for the first time.

## Microlab Controller

### Hardware Device Files

To make it simpler to extend support to new devices or alternate lab setups the microlab makes use of yaml files describing the hardware available on the SBC and connected to it. This is split up into two different files, one for the SBC called controller hardware, and the other for lab hardware.

Both of these file types can be selected, downloaded and uploaded from the settings menu of the microlab.

#### Hardware Devices Reference

A reference for the possible hardware devices and the settings used can be seen in the following two files.

[controller_hardware_reference](backend/data/controller_hardware_reference.yaml)

[lab_hardware_reference](backend/data/lab_hardware_reference.yaml)

#### Expanding support to other SBCs

If you want to use something other than a pi or the potato, you can do so by creating a custom controller hardware file. [backend/data/controllerhardware/](backend/data/controllerhardware/) contains the hardware device description for the two currently supported boards which you can reference.

Only a device named `gpio-primary` using some kind of `gpiochip` describing the available gpio ports is needed at the moment.

## Recipes

The microlab by default loads recipes from files located in `/var/lib/microlab/recipes/`. Recipe files can be uploaded to the microlab from the recipes page. See `solderless-microlab/backend/recipes/base.py` for information on the format required for recipe files.

## API

The Microlab backend API includes several endpoints described below. This list is incomplete, for more details, see the implementation at
[/backend/api/routes.py](backend/api/routes.py)

### List

`/list` - Returns an array of the currently available recipe names

Example response:

```
["aspirin"]
```

### Get Recipe

`/recipe/<name>` - Returns the full details for a recipe

### Status

`/status` - Returns an object containing the status of the microlab hardware. It provides a human-readable status message, and information on the current recipe's progress.

Example response:

```
{
    "message":"Place 2.0 g salicylic acid in chamber",
    "options":["Done"],
    "recipe":"aspirin",
    "icon":"reaction_chamber",
    "status":"user_input",
    "step":0
}
```

### Start

`/start/<name>` POST - Starts the recipe with corresponding name

Example responses:

```
{"response":"ok"}
```

or, if you try to start a recipe when one is running:

```
{"message":"Recipe aspirin is running. Stop it first.","response":"error"}
```

### Stop

`/stop` POST - Stops the current recipe

### selectOption

`/selectOption` POST - When in a recipe in a user_input step, select an option

### uploadRecipe

`/uploadRecipe` POST - Upload a JSON file to the microlab.

File must be valid JSON.

### controllerHardware

`/controllerHardware` - Gets the currently configured controller hardware name

### controllerHardware/list

`/controllerHardware/list` - Lists possible controller hardware name
