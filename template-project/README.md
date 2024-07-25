# template-project
Template Appian Locust project including basic configurations, project layout and cheatsheet.

Clone this project as the baseline for your Appian Locust project.

A sample Actor and Task Set are provided as examples and should run against any Appian Community Edition (ACE) site. Replace these with your own Actors and Task Sets as required.

Examples modules are provided to show how to keep the main `locustfile.py` small and simple, with specific implementation of tests kept within various app modules.



### Running the sample test

To run the included sample test:

* Follow the `Appian Locust - Quick Start Guide (Windows)` guide to get your workstation set up.
* Update `config.json`
  * Point to your own ACE site in `cluster_name`
  * Use your own ACE site credentials in `auth`
* Run `locust`



