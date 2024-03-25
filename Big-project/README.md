# Big Project
# 상황에 맞는 음악 생성 플랫폼
## Create Contextual Music with AI

## 개요

> 이미지 동영상 텍스트 등 여러가지 파일들을 넣어보고 그에 맞는 BGM을 들어 볼 수 있는 사이트


## How to start

1. git clone을 통해 repository 불러오기.

 ```bash
 git clone https://github.com/yangink/BIgProject.git
 ```

2.  필요한 라이브러리들을 설치합니다.

 ```bash
 pip install -r requirements.txt
 ```

3. 만약 database가 없거나 새로 생성하고 싶다면 database를 생성합니다.
```bash
cd ccma
python manage.py migrate login
python manage.py migrate
 ```
4. 사이트를 실행시킵니다.

 ```bash
 python manage.py runserver
 ```


## License

Released under the [MIT License](./LICENSE).
