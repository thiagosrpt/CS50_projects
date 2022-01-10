import urllib.parse

urls = 'http://www.test.com/wiki/CSS/test'



url_parts = urllib.parse.urlparse(urls)
path_parts = url_parts[2].rpartition('/')
print('URL: {}\nreturns: {}\n'.format(urls, path_parts[2]))