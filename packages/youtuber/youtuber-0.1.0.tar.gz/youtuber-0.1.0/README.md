# Python Package: YouTuber
Contains several useful features that can be used for youtube related projects.
This package is intended to provide useful features for video editing, including crawling through the YouTube Data API v3 and Selenium.

<br>

# Installation
```
pip install youtuber
```

<br>

# Tutorial
1. Main tutorial: https://github.com/DSDanielPark/youtuber/blob/main/doc/tutorial.ipynb
2. Sub tutorial folder: Tutorials for each function can be found in [this folder](https://github.com/DSDanielPark/youtuber/tree/main/doc). 


<br>

# Features
### 1. `YoutubeAPI`
Retrieve YouTube search results. <br>
You can get your 'Youtube Data API v3' key in [here](https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials?project=sincere-canyon-278402), and you can find some guide in [here.](https://developers.google.com/youtube/v3/getting-started?hl=ko)


```python
from youtuber import YoutubeAPI

DEVELOPER_KEY = "enter_your_api_key"
youtuber_v3 = YoutubeAPI(DEVELOPER_KEY)
links = youtuber_v3.get_links('chatGPT', 3) # if you enter 3, you can get 3 video links.

links
['https://www.youtube.com/watch?v=mpnh1YTT66w',
 'https://www.youtube.com/watch?v=ykuDB3xpTTo',
 'https://www.youtube.com/watch?v=GXm7WRtRbhA']
```

### 2. `YoutubeCrawler`
Retrieve comment data.
```python
from youtuber import YoutubeCrawler

chrome_driver = r'C:\Program Files\chromedriver.exe'
youtuber_crawl = YoutubeCrawler(chrome_driver)
df = youtuber_crawl.get_comment_df(links, 1) # if you enter 1, only 1 page of comments will be searched.

df
```



<br>

# References
[1] YouTube Data API v3: https://developers.google.com/youtube/v3/getting-started?hl=ko
 <br>
[2] Selenium python: https://selenium-python.readthedocs.io/

<br><br>


### `Important Warning:` All legal responsibilities associated with the use of the package lie with the user.
The Python package "youtuber" provides code for Python users to easily access data through the YouTube Data API v3 and Selenium. All licenses follow those of the API and dependent packages, and all responsibility for handling data and using the package lies with the user. There is no monetary compensation received for the use of this code, and it should be noted that there is no liability for the use of the code.