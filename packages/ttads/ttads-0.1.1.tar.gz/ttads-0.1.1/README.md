# Tasmota Application Development Server

This tool aims to simplify Tasmota Berry script development by doing two things:

* Starts a web app that automatically zips your project(s), and serves it as a `.tapp` file.
* Opens a tunnel to the web app, letting you deploy your Tasmota Application to any device with an internet connection.

# How to Install

`pip install ttads`

# Example Usage

To serve a project:

`$ttads --project /usr/src/my_project`

You can serve as many projects as you like, for example:

`$ttads --project /usr/src/project_a --project /usr/src/project_b ...`

If you want to give a project a name other than its directory name, you can prefix its path with `:`, e.g.

`$ttads --project project_c:/usr/src/project_c/berry_files ...`

This will serve the contents of `berry_files` as a TAPP file called `project_c.tapp`.

## Sample Output

```bash
Waiting for tunnel to initialise...
 * Serving Flask app 'TappServer'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:80
Press CTRL+C to quit
Serving project "project_a": `tasmota.urlfetch("http://c141-x-y-z-w.ngrok.io/project_a.tapp")`
Serving project "project_b": `tasmota.urlfetch("http://c141-x-y-z-w.ngrok.io/project_b.tapp")`
```

# :warning: Security Warning

Running `ttads` involves opening up your project files to the public internet, using a development server. Proceed with
caution. 