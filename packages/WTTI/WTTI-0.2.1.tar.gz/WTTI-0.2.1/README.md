# 🌐 WTTI 
Webpage Text Transformation Interface(WTTI)，將網頁文章內容以結構化方式儲存，以方便後續分析應用。

[![Python Build and Test](https://github.com/Keycatowo/WTTI/actions/workflows/python_test.yml/badge.svg)](https://github.com/Keycatowo/WTTI/actions/workflows/python_test.yml) [![pypi version](https://img.shields.io/pypi/v/WTTI)](https://pypi.org/project/WTTI/) ![GitHub repo size](https://img.shields.io/github/repo-size/Keycatowo/WTTI) ![GitHub](https://img.shields.io/github/license/Keycatowo/WTTI) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/WTTI) ![GitHub issues](https://img.shields.io/github/issues/Keycatowo/WTTI) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1-sGol2AhOhpeDGHb_7muGNAo2dvJasgb?usp=sharing)

## 🚀 安裝
使用 pip 安裝
```bash
# 更新pip
pip install --upgrade pip
pip install WTTI
```

## 📦 功能
+ [x] 提供網頁**文章**與**留言**結構化儲存的介面
+ [x] 支援儲存的內容輸出成不同的格式
    + [x] DataFrame
    + [ ] Database
## ✍️ 如何使用
```python
from wtti import Post
from wtti.output import posts_to_dataframe

# 建立一個Post物件
post = Post(
    text="如題，我不小心吞下了我的 AirPods，怎麼辦？",
    url="https://www.google.com",
    author="notChatGPT",
    platform="匹踢踢",
    likes=10,
    published_time="2021-01-01 12:00:00",
    title="不小心吞下了我的 AirPods 怎麼辦？",
    category="發問板",
)

# 添加底下的留言
post.add_comment(
    comment_text="你可以去醫院看看",
    author="醫生",
    likes=33,
    published_time="2021-01-01 12:05:00",
)
post.add_comment(
    comment_text="我也不知道",
    # 如果沒有作者或是按讚數，可以不填
    published_time="2021-01-01 12:05:20",
)
post.add_comment(
    comment_text="或者你可以試試用磁鐵把它吸出來！",
    author="DIY達人",
    likes=134,
    published_time="2021-01-01 12:20:00",
)
post.add_comment(
    comment_text="AirPods 是由蘋果公司開發的，如果您使用的是 iPhone 或 iPad，您可以試著與 Siri 聯繫，看看她是否有什麼神奇的解決方法。",
    author="我愛蘋果",
    likes=9487,
    published_time="2021-01-01 12:30:45",
)


# 建立一個Post物件
post2 = Post(
    text="只是發文測試",
    url="https://www.google.com",
    author="developer",
    platform="匹踢踢",
    likes=0,
    published_time="2021-01-01 13:00:00",
    title="測試測試",
    category="測試板",
)


# 輸出成DataFrame
posts_list = [post, post2] # 將所有的Post物件放入list
posts_df, comments_df = posts_to_dataframe(posts_list, merge=False)

# 再將DataFrame輸出成csv檔
posts_df.to_csv("posts.csv", index=False)
comments_df.to_csv("comments.csv", index=False)
```

## 📚 類別說明
+ [Post](#post)：用來儲存文章的類別
+ [Comment](#comment)：用來儲存留言的類別
### Post
#### 自動產生的屬性
以下屬性會在建立物件時自動產生，不可手動修改
+ `uuid`：文章的唯一識別碼
+ `created_timestamp`：文章物件建立的時間戳記
+ `modified_timestamp`：文章物件最後一次修改的時間戳記

#### 預設屬性
以下屬性在建立物件時可以指定，如無對應值也可以不指定，不指定時會自動產生預設值
+ `text`(str)：文章內容
+ `url`(str)：文章網址
+ `author`(str)：文章作者
+ `platform`(str)：文章來源平台
+ `likes`(int)：文章按讚數
+ `title`(str)：文章標題
+ `published_time`：文章發布時間，可以是以下三種格式
    + 1. timestamp
    + 2. "%Y-%m-%d %H:%M:%S"
    + 3. datetime.datetime
+ `category`(str)：文章分類

#### 額外屬性
+ 可以透過`Post["new_attribute"] = "new_value"`的方式新增屬性

### Comment

### 添加留言方法
預設留言物件會跟著文章物件一起建立
```python
post.add_comment(
    comment_text="你好",
    author="路人",
    likes=1,
    published_time="2021-01-01 12:05:00",
)
```

#### 預設屬性
以下屬性在建立物件時可以指定，如無對應值也可以不指定，不指定時會自動產生預設值
+ `comment_text`(str)：留言內容
+ `author`(str)：留言作者
+ `likes`(int)：留言按讚數

#### 自動產生的屬性
以下屬性會在建立物件時自動產生，不可手動修改
+ `uuid`：留言的唯一識別碼
+ `created_timestamp`：留言物件建立的時間戳記
+ `modified_timestamp`：留言物件最後一次修改的時間戳記

## 🤝 貢獻
如果你發現了一個 bug，或者有任何改進的建議，歡迎提交 issue 或者 pull request。

## 📜 授權
本套件使用 MIT 授權。詳細的授權條款請參閱 [LICENSE](LICENSE) 檔案。  
This package is licensed under the [MIT License](LICENSE).

