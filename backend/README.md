# Solderless Microlab Backend

This project is a python service that provides an API to control and read data from various hardware connected to the Raspberry Pi. The Microlab gui is the main consumer of this API.

## Starting up

See README.md in the root directory for instructions on running the service.

## API

The Microlab backend API includes several endpoints described below. For more details, see `solderless-microlab/backend/api/routes.py`

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

### List

`/list` - Returns an array of the currently available recipes

Example response:

```
["aspirin"]
```

### Start

`/start/<name>` - Starts the recipe with corresponding name

Example responses:

```
{"response":"ok"}
```

or, if you try to start a recipe when one is running:

```
{"message":"Recipe aspirin is running. Stop it first.","response":"error"}
```

### Stop

`/stop` - Stops the current recipe

## Recipes

The microlab by default loads recipes from files located in `solderless-microlab/backend/recipes/files/`. See `solderless-microlab/backend/recipes/base.py` for information on the format required for recipe files.
