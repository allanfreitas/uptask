<p align="center">
<a href="https://github.com/allanfreitas/uptask">
<img src="https://raw.githubusercontent.com/allanfreitas/uptask/master/uptask-logo-small.png"></a></p>

<p align="center">

<a href="https://github.com/allanfreitas/uptask">
    <img src="https://img.shields.io/pypi/v/uptask.svg?style=flat-square" 
    alt="PyPI version">
    </a>

<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" 
    alt=""></a>

<a href="https://pypi.python.org/pypi/uptask/">
    <img src="https://img.shields.io/pypi/status/uptask.svg" 
    alt="PyPI status"></a>


<a href="https://pypi.python.org/pypi/uptask/">
    <img src="https://img.shields.io/pypi/pyversions/uptask.svg" 
    alt="PyPI pyversions"></a>
    
</p>

<p align="center">

<a href="https://github.com/allanfreitas/uptask/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/allanfreitas/uptask.svg?style=flat-square" 
    alt=""></a>


<a href="https://github.com/allanfreitas/uptask/stargazers">
    <img src="https://img.shields.io/github/stars/allanfreitas/uptask.svg?style=flat-square" 
    alt=""></a>


<a href="https://github.com/allanfreitas/uptask/issues">
    <img src="https://img.shields.io/github/issues/allanfreitas/uptask.svg?style=flat-square" 
    alt=""></a>
</p>



Task Runner(SSH, *soon will run local tasks too*) made in Python

# WIP

It's a Work in Progress :)

# For the Community and Beginners Like Me :)

The branch [basepackage](https://github.com/allanfreitas/uptask/tree/basepackage)
has a base TEMPLATE for you create your own package in python with and without command line scripts

# Some words about it :)

It's a tool to run tasks easily on Linux Servers using SSH,
or on local mode(It's on my next features list)

Like Fabric or Capistrano, It's for my needs to start,
but I hope it will serve to others :)

<hr />

# Quick Start

## Install
```shell
$ pip install uptask
```
It's only tested on python 3.6 for now :)

## Basic Usage
After install, you must create a folder where you want to keep your files with commands to execute.

Ex.: I use ```$HOME/code/scripts```

**Tip: You can organize in subfolders your files** 

After install/update run the following command on your scripts folder to check what commands are available on your version of **UpTask**

```shell
$ uptask

UpTask 0.2.1

Available Commands:
    init    : Create the .env and tasks.uptask file if doesnt exists
    runfile : Read a Simple Text File With Linux Commands to execute
    tasks   : Read tasks file and list the available tasks to execute
    run     : Read tasks file and execute the requested task

How run a command?
    updtask runfile mytxtfile

# INFO: Each command has it's own params ##
```


```shell
$ cd to_your_desired_path
$ uptask init
```
The command ```uptask init``` will create two files on the current folder:

**.env**

```shell
# UpTask Env
# Any Other Vars in the future will be using the "UPTASK_" Prefix
UPTASK_HOST=127.0.0.1
UPTASK_USER=
UPTASK_PASS=
```

**tasks.uptask**

```shell
# Uptask Tasks File
@story(checks)
    currentdir
    checkpython
@endstory

@task(currentdir)
    pwd
@endtask

@task(checkpython)
    python3 --version
@endtask

# You can configure .halt tasks for a task, 
# and will be triggered if the task name returned a error
@task(checkpython.halt)
    echo 'Task checkpython Fail :/'
@endtask
```

**Tip: Anything outsite a @"tag" > @end"tag" tag will be ignored.**


Now let's imagine that you have a file with the following contents.

*Filename:* ```check_home_list.txt ```

```shell
# Any Line starting with a "#" will be ignored
#sudo yum update -y

# You can use many "one-line" bash format like the line below
pwd && ls -lah

#this line will trigger a error since "instal" it's not a valid "yum" command
sudo yum instal nano
# but for now the line above will not stop the execution, it's on my next features checklist.
sudo lid -g wheel
```

```shell
$ uptask runfile check_home_list.txt
```
It will output all commands output like if you are running them on the server.


## #Version 0.2.1

For now you have 4 commands only


- **init** command > creates the .env with default vars and creates the tasks.uptask file with a example list of tasks

```shell
$ uptask init
```

- **runfile** command > needs a file name relative to the path it's been called

```shell 
$ uptask runfile your_file_to_run.txt
```

- **tasks** command > will read the tasks.uptask file and list the Available 

```shell
$ uptask tasks

#Output
UpTask 0.2.1

Available stories:
    checks
Available tasks:
    currentdir
    checkpython
    checkpython.halt
```

The **.halt** tasks are called upon the command before the **.** returns **ExitCode > 0** (Fails/Halts)

- **run** command > will read the tasks.uptask file for a **story** or a **task** matching the name passed 

```shell
#checkpython is a task(contains one or multiline bash commands)
	
$ uptask run checkpython

#Output
UpTask 0.2.1

Running Task: checkpython
Python 3.6.5
```


```shell
#checks is a story(contains multiple tasks)
$ uptask run checks 

#Output
UpTask 0.2.1

Running Story: checks
Running Task: currentdir
/Users/allan/code/python/mytasks
Running Task: checkpython
Python 3.6.5
```

## A Example GIF :)

**On the image is 0.2.0, but it's the same of 0.2.1**

![UpTask Example GIF](https://i.imgur.com/EqYjyvJ.gif)


## Disclaimer
I'm not a native English speaker, 
if you find any grammar mistakes in the documentation or in the code, 
make a pull request, open a issue or please let me know by any contact way :)


## Contributing

Considering contributing to the **Uptask**?

**Thank you!**

You can contribute doing some of theese:
- send pull requests
- report bugs 
- asking for new features :)

## License

**Uptask** project is open-source under the [MIT license](https://opensource.org/licenses/MIT).