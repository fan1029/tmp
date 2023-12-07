from urllib.parse import urlparse



def filter_url(url):
    try:
        if "://" not in url:
            url = "http://" + url
        result = urlparse(url)
        hostname = result.hostname
        if ":" in hostname:
            hostname = hostname.split(":")[0]
        return hostname
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




print(filter_url("http://www.baidu.com"))
print(filter_url("https://www.baidu.com/"))
print(filter_url("www.baidu.com"))
print(filter_url("www.baidu.com:80"))
print(filter_url("www.baidu.com:80/"))
print(filter_url("www.baidu.com:80/123"))
print(filter_url("www.baidu.com:80/123/"))
print(filter_url("a.c.e.www.baidu.com:80/123/"))
print(filter_url("http://1.2.3.4:8000/"))
print(filter_url("http://3.3.4.5/"))
print(filter_url("23.4.4.5"))
print(filter_url("2.3.4.2:8081"))
