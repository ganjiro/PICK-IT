# [PICK-IT!]
A web app to manage the champion selction of League of Legends with your smarphone! This is project for the course of Human Computer Interaction (University Of Florence - A. D. Bagdanov)
This is the repository for the web app, [here] you can find the PC app repo
This project has been done in collaboration with [Marco Mistretta]

## Prerequisites
- A Windows pc 
- League Of Legends Account
- Smartphone with at least iOS 7 or Android 8

## Project Idea
There are two application: 
- PC App that exchange information with the Riot Client through the [Riot API], such as the champion to pick or the lobby phase, and send the information to the Web App. The GUI is made with [PyQt]
- Web App that displays the lobby status, allow the user to see the team composition, to pick and to ban; this is a progressive web app so it can be installed in a smarphone. Is made using [Boostrap] and [jQuery] as frontend libraries and [Flask] for the Backend.

The sincronization is made by a code provided by the pc app that must be typed in the web app.
The comunication between the apps is managed by redis caching in order to be without slowdowns.
All the project is developed to work with possible new League of Legends updates such as new champion or new the order of the champ selection actions.


The project is fully functional, you can test it at this link [PICK-IT!]; is hosted by [Heroku] that offers a free PaaS and a small redis cluster. 

## Installation and Syncronization Tutorial
This is a video tutorial for the installation and the syncronization between the apps:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Kg2rtYsNS5E/0.jpg)](https://www.youtube.com/watch?v=Kg2rtYsNS5E)

## Some Screeshots

<!-- commento ![alt text](https://github.com/ganjiro/lol_picker_web_app/screenshots/full_page.png?raw=true)
 -->
[alt text](https://github.com/ganjiro/lol_picker_web_app/screenshots/full_page.png?raw=true) 







[Riot API]: <https://developer.riotgames.com/>
[PICK-IT!]: <https://lol-pick-it.herokuapp.com/>
[here]: <https://github.com/marcomistretta/lol_picker_pc_app>
[Marco Mistretta]: <https://github.com/marcomistretta>
[Heroku]: <https://www.heroku.com>
[Flask]: <https://flask.palletsprojects.com/>
[Boostrap]: <https://getbootstrap.com/>
[PyQt]: <https://doc.qt.io/qtforpython/>
[jQuery]: <https://jquery.com/>
