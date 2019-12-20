from bs4 import BeautifulSoup


def get_tag_id(text, node, exp):
    """解析标签 xpath为id"""
    try:
        soup = BeautifulSoup(text, 'html.parser')
        result = soup.find_all('{0}'.format(node), id='{0}'.format(exp))
        return str(result[0])
    except Exception as e:
        print(e)


def get_tag_class(text, node, expression):
    """解析标签 xpath为class"""
    try:
        soup = BeautifulSoup(text, 'html.parser')
        result = soup.find_all('{0}'.format(node), class_='{0}'.format(expression))
        return str(result[0])
    except Exception as e:
        print(e)
