# pico-up-and-running

A template repository with some scripts and shared functionality to get up and running with RaspberryPi Pico

## The `pico-up` command

```
python pico-up

build   minify and attempt to compile pico application to bytecodes
init    initialise a python pico project in the current directory
push    push local application code to a connected pico
wipe    remove all files from a connected pico
```

### `init`

The init command will create the following directory structure

```
.
├── app
│   └── __init__.py
├── .gitignore
├── main.py
├── README.md
└── settings.py
```
