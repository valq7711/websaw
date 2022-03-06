# websaw
The next generation in rapid development applicartion framework designed to offer maximum flexiblity coupled with comprehensive functionality 'out of the box' to allow you to create fully functional professional applications with minimal code.

## Getting Started
These instructions will get you a copy of the framework up and running on your local machine for development and testing purposes. See the relevant deployment documentaion for notes on how to deploy the project on a live system. Installation and setup will vary depending on your operating system and preferred installation method.

### Prerequisites

* Python 3 >= 3.7

### Installing

Depending on your requirements and OS installation will vary. We reccomend you install into a virtual environment for testing and developemnt purposes.
The following comands from bash / powershell will get you up and running in no time.
Example:
To set up a development environment on a Linux-like system or a Windows 10 machine with WSL2 follow these steps: 
Open your wsl terminal
```
$home/Development
```
Set up a virtual enviroments
```
$ python3 -m venv websaw 
$ cd websaw
websw $ source ./bin/activate
(websaw)$ python3 -m pip install websaw
(websaw)$ python3 -m websaw run apps
```
Hint: If python3 doesnt work try using just pyhon instead.

Once websaw is running you can access a specific app at the following urls from your browser:
```
http://localhost:8000/{yourappname}/index
```
In order to stop web server, you need to hit Control-C on the window where you run it.
Please refer to the user documentation if you need to change the configs or wish to use different ports etc.

## License

This project is licensed under the MIT License

