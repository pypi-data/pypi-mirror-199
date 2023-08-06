# 🌐 WTTI 
Webpage Text Transformation Interface(WTTI)，將網頁文章內容以結構化方式儲存，以方便後續分析應用。

[![Python Build and Test](https://github.com/Keycatowo/WTTI/actions/workflows/python_test.yml/badge.svg)](https://github.com/Keycatowo/WTTI/actions/workflows/python_test.yml) [![pypi version](https://img.shields.io/pypi/v/WTTI)](https://pypi.org/project/WTTI/) ![GitHub repo size](https://img.shields.io/github/repo-size/Keycatowo/WTTI) ![GitHub](https://img.shields.io/github/license/Keycatowo/WTTI) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/WTTI) ![GitHub issues](https://img.shields.io/github/issues/Keycatowo/WTTI)

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
    text="你可以去醫院看看",
    author="醫生",
    likes=33,
    published_time="2021-01-01 12:05:00",
)
post.add_comment(
    text="我也不知道",
    # 如果沒有作者或是按讚數，可以不填
    published_time="2021-01-01 12:05:20",
)
post.add_comment(
    text="或者你可以試試用磁鐵把它吸出來！",
    author="DIY達人",
    likes=134,
    published_time="2021-01-01 12:20:00",
)
post.add_comment(
    text="AirPods 是由蘋果公司開發的，如果您使用的是 iPhone 或 iPad，您可以試著與 Siri 聯繫，看看她是否有什麼神奇的解決方法。",
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


## 🤝 貢獻
如果你發現了一個 bug，或者有任何改進的建議，歡迎提交 issue 或者 pull request。

## 📜 授權
本套件使用 MIT 授權。詳細的授權條款請參閱 [LICENSE](LICENSE) 檔案。  
This package is licensed under the [MIT License](LICENSE).

