<a name="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python3-yellow?style=for-the-badge" alt="Made with Python3" />
  <a href="https://github.com/hschickdevs/Telegram-Translate-AI/stargazers"><img src="https://img.shields.io/github/stars/hschickdevs/Telegram-Translate-AI.svg?style=for-the-badge&color=219ED9" alt="Stargazers" /></a>
  <a href="https://github.com/hschickdevs/Telegram-Translate-AI/blob/main/LICENSE"><img src="https://img.shields.io/github/license/hschickdevs/Telegram-Translate-AI.svg?style=for-the-badge&color=green" alt="GPLv3 License" /></a>
</p>

<!-- 
![Madewith][madewith-shield]
[![Stargazers][stars-shield]][stars-url]
[![GPLv3 License][license-shield]][license-url] -->
<!-- [![Issues][issues-shield]][issues-url]
[![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Version][version-shield]][version-url] -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="docs/logo-oai.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">Telegram-Translate-AI</h3>

  <p align="center">
    A powerful Telegram bot that utilizes OpenAI's GPT models for contextually accurate and dialect-specific translations!
    <br />
    <a href="#about-the-project"><strong>Learn More »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">Try Demo</a>
    ·
    <a href="#bot-commands">Bot Commands</a>
    ·
    <a href="https://github.com/hschickdevs/Telegram-Translate-AI/issues">Contribute</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#deployment">Deployment</a></li>
      </ul>
    </li>
    <li><a href="#bot-commands">Bot Commands</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the Project

![PRODUCT DEMO/GIF](docs/demo.gif)

This Telegram bot leverages the power of OpenAI's GPT language models to provide advanced text translations. Unlike traditional translation services like Google Translate, this bot offers several unique advantages:

1. **Contextual and Punctual Accuracy**: Through prompt engineering, the bot is capable of understanding the context and nuances of the text, providing translations that are both contextually and punctually accurate.

2. **Specific Language Context**: The bot can be configured to understand and translate specific dialects or regional language variations, such as Spanish (Mexico Dialect).

3. **Typo Detection**: The advanced AI model automatically detects typos and corrects them, ensuring the translation is as accurate as possible.

<!-- Head to [Installation & Deployment]() to get started. -->


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get your own local instance of the Telegram AI translation bot up and running, follow these simple steps:

### Prerequisites

Before you begin, make sure you have Python 3.9+ and pip installed on your system.

Check your Python version in your command prompt using:

* **MacOS/Linux:**
  ```sh
  python3 -V
  ```

* **Windows:**
  ```sh
  python -V
  ```
  _or_
  ```sh
  py -V
  ```

If you do not have Python 3.9+ installed, you can download it [**🔗 here**](https://www.python.org/downloads/).

### Installation

To install the bot, follow these steps:

1. Clone the repo:

   ```sh
   git clone https://github.com/hschickdevs/Telegram-Translate-AI.git
   ```

3. CD into the project directory:

   ```sh
   cd Telegram-Translate-AI
   ```
   
4. Install pip packages:
   
   ```sh
   pip install -r requirements.txt
   ```

### Deployment

Once you have successfully installed the bot, you can deploy it to your preferred environment (be that local or in the cloud).

For the sake of this guide, we will be deploying the bot locally in a UNIX environment (On a MacOS or Linux machine):

1. Get an OpenAI API Key. If you don't know how to do so, use [**this guide**](https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt) for reference.

2. Create a new Telegram bot and get the _bot token_ using [**BotFather**](https://t.me/botfather). If you don't know how to do so, use [**this guide**](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) for reference.

3. Set environment variables. The following environment variables should be set:

   ```sh
   OPENAI_TOKEN=<YOUR_APIKEY>
   BOT_TOKEN=<YOUR_TOKEN>
   MODEL=<GPT-MODEL>
   ```

   > **Note:** The `MODEL` variable is optional and defaults to `gpt-3.5-turbo`. If you have the plus subscription, you can set this to `gpt-4` for better results.

   To set your environment variables, rename the file called [`.env.example`](/.env.example) in the root directory of the project, and then replace the value contents with your tokens and model.

    * `mv .env.example .env`

4. Make sure that you are in the root directory of the project (_type `pwd`_), and then run the following command to start the bot:

    ```sh
    python3 -m src
    ```

    > **Note:** If you are using Windows, you may need to use `python -m src` or `py -m src` instead.

5. Upload the bot commands to botfather for command hits.

    1. Copy the contents of [**`commands.txt`**](/commands.txt).

    2. See this guide to learn how to [**upload the commands**](docs/upload-commands.gif) to your bot.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Bot Commands

...


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- COST ESTIMATES -->
## Cost Estimates

This is how much the bot will cost to run and use:
- Hosted on Heroku (1 Dyno)
- 1,000 messages per month (each message is 1,000 tokens, about 1,000 words)
- If using GPT-4 + $20/mo

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Acknowledgements

Thanks to these awesome tools and frameworks for aiding in the development of this project!

* [PyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* [OpenAI Python Library](https://pypi.org/project/openai/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GPLv3.0 License. See `LICENSE.txt` for more information.

In summary, the GNU General Public License v3 (GPLv3) is a free software license that allows you to use, modify, and distribute the software for personal and commercial use. 

However, any changes you make must also be open-sourced under the same license. This ensures that derivative work remains free and open, promoting collaboration and transparency. Importantly, if you distribute the software or any modifications, you must make the source code available and clearly state any changes you've made.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

**Telegram:** [@hschickdevs](https://t.me/hschickdevs)

**Email:** [hschickdevs@gmail.com](mailto:hschickdevs@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/hschickdevs/Telegram-Translate-AI.svg?style=for-the-badge&color=blue
[contributors-url]: https://github.com/hschickdevs/Telegram-Translate-AI/blob/main/bot/__init__.py

[version-shield]: https://img.shields.io/badge/Version-v1.0.0-brightgreen?style=for-the-badge

[version-url]: https://github.com/hschickdevs/Telegram-Translate-AI/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members

[stars-shield]: https://img.shields.io/github/stars/hschickdevs/Telegram-Translate-AI.svg?style=for-the-badge&color=219ED9
[stars-url]: https://github.com/hschickdevs/Telegram-Translate-AI/stargazers

[madewith-shield]: https://img.shields.io/badge/Made%20with-Python3-yellow?style=for-the-badge

[issues-shield]: https://img.shields.io/github/issues/hschickdevs/Telegram-Translate-AI?style=for-the-badge&color=red
[issues-url]: https://github.com/hschickdevs/Telegram-Translate-AI/issues

[license-shield]: https://img.shields.io/github/license/hschickdevs/Telegram-Translate-AI.svg?style=for-the-badge&color=green
[license-url]: https://github.com/hschickdevs/Telegram-Translate-AI/blob/main/LICENSE

[product-screenshot]: images/screenshot.png