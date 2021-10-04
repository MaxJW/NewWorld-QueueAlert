# New World Queue Alert
Plays an alert sound when the queue goes below 50 for New World, without needing New World to be in front of other applications, so you can browse /r/newworldgame while waiting.

### IMPORTANT - Be sure to select the correct resolution for your game resolution ([see here](https://github.com/MaxJW/NewWorld-QueueAlert/blob/c7ea2dd26c197284cd423bca70e8e79fe758a791/newworld_alert.py#L64-L67)). If you need another one there, create an issue with a screenshot of the queue screen attached and I'll add it in!

## Using this script
1. Run New World and hit 'Play' so the queue number is displayed
2. Run the script: `py .\newworld_alert.py`
3. Feel free to have other programs open above New World, just wait for your alert to play!

## Installation
1. Install requirements.txt:  `pip install -r requirements.txt`
2. Install Tesseract - Windows installer here: https://github.com/UB-Mannheim/tesseract/wiki
3. Place your notification sound called `alert.mp3` in the same directory as this script

## How does it work?
This script grabs a screenshot of the queue alert area, and uses OCR to detect the number of people in the queue. If this value goes below 50, an alert sound (of your choosing) will play to alert you.

## Credits
Included alert.mp3 sound from freesound.org - https://freesound.org/s/135613/