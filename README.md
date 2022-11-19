# Rerun
A small python script for rerunning applications with any kind of arguments
- It just copies whatever you wanted to run, and runs it in a "REPL" of sorts

```sh
rerun "very_long_command -p with -l lots -f of -a arguments"
```

Then, it'll look something like this:
```
[ very_long_command -p with -l lots -f of -a arguments ] >>> *Type something here!!!*
```

- Type "help" to get a list of built in (sub)commands! 

## Installation
Run:
```sh
git clone "git://gitlab.com/tuliliblossom/Rerun.git"
poetry install ./Rerun/
```
- Depends on Python 3.8+
