# plugins/auto_parser.py
import httpx
from lxml import etree
from pydantic import BaseModel
from config.logging_config import logger


class TagDetails(BaseModel):
    tag: str
    attributes: dict
    text: str
    children: list  # List of TagDetails
    num_text: str
    num_url: str
    xpath: str


class AutoParser:
    def __init__(self, html: str):
        try:
            self.tree = etree.HTML(html)
            self.structure = self.extract_structure()
        except:
            logger.error(f"could not parse response as HTML or JSON, response text: {html}")
            raise ValueError("could not parse response as HTML or JSON")

    @staticmethod
    def get_xpath(element: etree.Element):
        """
        获取元素的xpath路径
        :param element:
        :return:
        """
        components = []
        for parent in element.iterancestors():
            siblings = parent.xpath(f"./{element.tag}")
            if 'id' in element.attrib:
                components.append(f"{element.tag}[@id='{element.attrib['id']}']")
            elif 'class' in element.attrib:
                components.append(f"{element.tag}[@class='{element.attrib['class']}']")
            elif len(siblings) == 1:
                components.append(element.tag)
            else:
                pos = siblings.index(element) + 1
                components.append(f"{element.tag}[{pos}]")
            element = parent
        components.reverse()
        return f"/{'/'.join(components)}"

    def extract_structure(self, element: etree.Element = None) -> TagDetails:
        """
        递归提取HTML结构
        :param element:
        :return:
        """
        if element is None:
            element = self.tree
        tag = element.tag
        attributes = element.attrib
        children = [self.extract_structure(child) for child in element if etree.iselement(child)]

        num_text = len(element.xpath(".//text()"))  # 当前标签及其所有子标签的文本节点数量
        num_url = len(element.xpath(".//a[@href]"))  # 当前标签及其所有子标签的链接数量
        text = element.text if element.text else ""

        return TagDetails(
            tag=tag,
            attributes=attributes,
            text=text,
            children=children,
            num_text=str(num_text),
            num_url=str(num_url),
            xpath=self.get_xpath(element)
        )

    def find_maximum_text_node(self):
        """
        找到文本节点最多的标签
        :param element:
        :return:
        """
        pass
