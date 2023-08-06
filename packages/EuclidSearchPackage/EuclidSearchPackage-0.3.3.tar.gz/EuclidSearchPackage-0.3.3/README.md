# EuclidSearchPackage

this package is include some tools to get data from weibo、zhihu、guba and etc.

The project will continue to be updated and you are welcome to join us on [GitHub](https://github.com/Euclid-Jie/EuclidSearchPackage).

## Existing features

#### 0、set cookie and import package

```python
from src.EuclidSearchPackage import *
Set_cookie('cookie.txt')  # 'cookie.txt' is your local cookie file path
```

### 1、 get single weibo's data

```python
data_json = Get_single_weibo_data(mblogid='MrOtA75Fd')
print(data_json)
```
### 2、 get the weibo url list

set the url(contains keyword),  then  item in list is `"1562868034/MkXTBh9Fk"`, which is contains uid and mblogid

```python
url_list = Get_item_url_list('https://s.weibo.com/weibo?q=杭州公园')
print(url_list)
```
### 3、get user's info

```python
data_json = Get_user_info('1202150843')
print(data_json)
```
### 4、get user's all blog

```python
Get_user_all_weibo(2656274875, 100, query='主播说联播', colName='主播说联播', csv=True)
```