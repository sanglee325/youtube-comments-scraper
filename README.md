# youtube-comments-scraper

## 사용법

1. 컴퓨터에서 사용중인 chorme의 버전과 일치하는 chormedriver를 [여기서](https://chromedriver.chromium.org/downloads) 다운 받습니다.

2. 다운받은 `chromedriver.exe`을 `main.py` 파일과 같은 위치에 두거나, `--exe_path=[chormedriver path]`에 경로를 입력합니다.

3. 실행에 필요한 package 설치를 위해 아래의 명령어를 입력합니다.

    ```sh
    pip install -r requirements
    ```

4. package중 [demoji](https://github.com/bsolomon1124/demoji) 사용을 위해서 python 실행 후 demoji를 import 한 다음 `download_codes()`를 불러옵니다.

    ```sh
    $ python
    Python 3.6.9 |Anaconda, Inc.| (default, Jul 30 2019, 14:00:49) [MSC v.1915 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import demoji
    >>> demoji.download_codes()
    Downloading emoji data ...
    ... OK (Got response in 0.45 seconds)
    Writing emoji data to C:\Users\sanglee\.demoji\codes.json ...
    ... OK
    >>> exit()
    ```

5. 아래의 명령어를 통해 main.py를 실행시킵니다.

    ```sh
    python main.py --link="[댓글을 수집하고자 하는 링크]" --filename="[저장하고자 하는 파일 이름]"
    ```

6. 수집된 댓글을 저장한 파일은 생성된 outputs directory에 저장됩니다.
