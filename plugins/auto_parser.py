# plugins/auto_parser.py
import warnings
from typing import Union, List

from lxml import etree, html
from pydantic import BaseModel, SkipValidation
from config.logging_config import logger

warnings.filterwarnings("ignore", category=UserWarning, message=".*cyfunction Element.*")
default_ignore_elements = ['script', 'style', 'meta', 'head', 'link']
default_target_tag_attribute = ['href', 'src']


class HTMLStructureModel(BaseModel):
    tag: str
    attributes: dict
    num_text: int
    num_url: int
    children_tag: dict
    children_len: int
    xpath: str
    text: str
    element: SkipValidation[etree.Element]
    children: list  # List of TagDetails

    class Config:
        arbitrary_types_allowed = True

    def extract_all_url(self, target_tag_attribute: list = None, ignore_elements: list = None, ):
        if target_tag_attribute is None:
            target_tag_attribute = default_target_tag_attribute
        if ignore_elements is None:
            ignore_elements = default_ignore_elements

        def bfs(node: HTMLStructureModel):
            urls = []
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current.num_url == 0 and target_tag_attribute == default_target_tag_attribute:
                    continue
                for child in current.children:
                    if child.tag in ignore_elements:
                        continue
                    for attribute in child.attributes:
                        if attribute in target_tag_attribute:
                            urls.append({
                                'text': child.text,
                                'url': child.attributes[attribute],
                            })
                    queue.append(child)
            return urls

        return bfs(self)

    def extract_all_text(self, ignore_elements: list = None):
        if ignore_elements is None:
            ignore_elements = default_ignore_elements

        def dfs(node: HTMLStructureModel):
            text = []
            if node.tag not in ignore_elements:
                text.append(node.text)
            for child in node.children:
                text.extend(dfs(child))
            return text

        return dfs(self)


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
            if not isinstance(element.tag, str):
                # print(f"Unexpected element.tag type: {type(element.tag)}.")
                return "Unknown"
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

    def extract_structure(self, element: etree.Element = None, ignore_elements=None) -> HTMLStructureModel:
        """
        递归提取HTML结构
        :param ignore_elements:
        :param element:
        :return:
        """
        if ignore_elements is None:
            ignore_elements = default_ignore_elements
        check_element = lambda x: etree.iselement(x) and x.tag not in ignore_elements
        if element is None:
            element = self.tree
        tag = element.tag
        if not isinstance(tag, str):
            return HTMLStructureModel(
                tag="Unknown",
                attributes={},
                text="",
                children=[],
                children_len=0,
                children_tag={},
                num_text=0,
                element=element,
                num_url=0,
                xpath="Unknown"
            )
        attributes = element.attrib
        children = [
            self.extract_structure(child) for child in element if check_element(child)
        ]
        children_len = len(children)

        def statistics_children_tag():
            tag_count = {}
            for child in children:
                tag_count[child.tag] = tag_count.get(child.tag, 0) + 1
            return tag_count

        children_tag = statistics_children_tag()

        num_text = len(''.join(element.xpath(".//text()")))  # 当前标签及其所有子标签的文本节点数量
        num_url = len(element.xpath(".//a[@href]"))  # 当前标签及其所有子标签的链接数量
        if list(children_tag.keys()) == ['br']:
            html_content = etree.tostring(element, encoding=str, method='html')
            tree = html.fromstring(html_content)
            text = tree.xpath('string(.)').strip()
            text = text.replace('\xa0\xa0', '\n')
        else:
            text = element.text if element.text else ""

        return HTMLStructureModel(
            tag=tag,
            attributes=attributes,
            text=text,
            children=children,
            children_len=children_len,
            children_tag=children_tag,
            num_text=int(num_text),
            num_url=int(num_url),
            element=element,
            xpath=self.get_xpath(element)
        )

    def find(
            self,
            tag: str,
            tag_attributes: dict = None,
            children_tag: list = None,
            url_num_limit: list = None,
            text_num_limit: list = None,
            children_len_limit: list = None,
            # sort_func: callable = lambda x: x.num_text,
            extract_first: bool = False
    ) -> Union[HTMLStructureModel, List[HTMLStructureModel]]:
        def bfs(node: HTMLStructureModel):
            queue = [node]
            matched = []
            while queue:
                current = queue.pop(0)
                if current.tag == tag:
                    if tag_attributes:  # 如果有属性要求
                        all_matched = True
                        for key, value in tag_attributes.items():
                            if current.attributes.get(key) != value:
                                all_matched = False
                                break
                            else:
                                continue
                        if all_matched:
                            matched.append(current)
                    else:
                        matched.append(current)
                for child in current.children:
                    queue.append(child)

            # if sort_func:
            #     matched = sorted(matched, key=sort_func, reverse=True)

            if extract_first:
                return matched if isinstance(matched[0], HTMLStructureModel) else matched[0][0]

            return matched

        bfs_matched = bfs(self.structure)  # 找到所有匹配的元素
        remaining_elements = []

        for elements in bfs_matched:  # 遍历所有匹配的元素
            if children_tag:  # 子节点标签要求
                keep_element = True
                for element_tag in elements.children_tag:
                    if element_tag not in children_tag:
                        keep_element = False
                        break
                if not keep_element:
                    continue

            if url_num_limit:  # 链接数量限制
                if url_num_limit[0] <= elements.num_url <= url_num_limit[1]:
                    pass
                else:
                    continue

            if text_num_limit:  # 文本节点数量限制
                if text_num_limit[0] <= elements.num_text <= text_num_limit[1]:
                    pass
                else:
                    continue

            if children_len_limit:  # 子节点数量限制
                if children_len_limit[0] <= elements.children_len <= children_len_limit[1]:
                    pass
                else:
                    continue

            # If the element passed all the checks, add it to the new list.
            remaining_elements.append(elements)

        return remaining_elements

    def find_maximum(self, find_type='url', target_tag='dt', index_offset=0) -> HTMLStructureModel:
        """
        找到文本节点最多的标签
        :param index_offset:
        :param find_type:
        :param target_tag:

        :return:
        """

        if find_type not in ['text', 'url']:
            raise ValueError("tag_type must be 'text' or 'url'")

        def bfs(node: HTMLStructureModel) -> HTMLStructureModel:
            path_to_node = []
            queue = [node]
            while queue:
                max_text = 0
                current_max_node = None
                current = queue.pop(0)
                # print(current.model_dump_json(indent=4))
                for child in current.children:
                    if find_type == 'text':
                        if child.num_text > max_text:
                            max_text = child.num_text
                            current_max_node = child
                    elif find_type == 'url':
                        if child.num_url > max_text:
                            max_text = child.num_url
                            current_max_node = child
                if current_max_node:
                    queue.append(current_max_node)
                    path_to_node.append(current_max_node)

            path_to_node_reversed = list(reversed(path_to_node))
            for index, i in enumerate(path_to_node_reversed):
                # print(index, i)
                if target_tag in i.tag:
                    return path_to_node_reversed[index + index_offset]

        return bfs(self.structure)
