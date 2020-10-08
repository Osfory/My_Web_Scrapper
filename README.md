###MAJOR UPDATE OF PROJECT. - 07.10.2020

###This is the first steps snake project.

Example shows how to build and develop artifact using standard python ecosystem:
- `pip`: for dependencies management
- `venv`: for project isolation. By default python installs user or system wide dependencies
- `dependencies.txt` contains pip dependencies and version for reproducible builds
- `src` contains source code

Getting started:

- Install venv for python project isolation: `python -m venv .`
- Activate venv for shell: `source bin/activate`
- Install manual declared dependencies: `pip install -r dependencies.txt`
- Download chrome driver: `https://sites.google.com/a/chromium.org/chromedriver/`
- You may open chrome with remote address: `chromium --remote-debugging-port=9222 --user-data-dir=/tmp/chrometmp` and connect to it using `connect $PORT` command: `python src/headhunterScrapper.py /home/aleksey/PycharmProjects/Web_driver/chromedriver_linux64/chromedriver /home/aleksey/PycharmProjects/My_Web_Scrapper/dataset connect 9222`
- Either use `open` command and just open new browser: `python src/headhunterScrapper.py /home/aleksey/PycharmProjects/Web_driver/chromedriver_linux64/chromedriver /home/aleksey/PycharmProjects/My_Web_Scrapper/dataset open`



