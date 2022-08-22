<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">NAS eMail Archiver</h3>

  <p align="center">
    An simple but awesome python script to check, download and store email attachments on your local storage!
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Here's why:
It all started when i bought a NAS device and noticed i was still using gmail as a storage device especialy for documents received via email.

Python libraries used

### Prerequisites

NAS device or any computer, Windows or Unix. The next steps were used on a Terramaster TOS 5.0 NAS machine where it's possible to setup a Scheduled Task to run a script similar to a windows machine

### Installation

NAS installation instructions:

1. Create a folder where to store the .py script and upload the file there
2. Create a folder where to store the email attachments 
3. Create a scheduled task to run the script similarly to the following:
    cd /
    ./home/sorin/home/MailArchiver/NASEmailArchiver.py

<!-- USAGE EXAMPLES -->
## Usage

The script will regularly check for emails, download the email attachments and store them at the specified location in a folder with the email subject name. A top level folder name will be created with the current year

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sorin Murarasu - sorin@murarasu.com

Project Link: [https://github.com/sorinmurarasu-hash/NAS-eMail-Archiver](https://github.com/sorinmurarasu-hash/NAS-eMail-Archiver)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

