# Python built-in libraries
import os
import re
from typing import Literal
from urllib.parse import unquote

# 3rd party libraries
import requests
from bs4 import BeautifulSoup, Tag

from ..utils import join_path_parts_ignore_none

# Own code
from ..utils import create_dir_recursively


def download_html(url: str, path_save_to: str) -> None:
    response = requests.get(url)
    with open(path_save_to, 'wb') as html:
        html.write(response.content)


def get_soup(html_index_path: str) -> BeautifulSoup:
    with open(html_index_path, 'r', encoding='utf-8') as html:
        return BeautifulSoup(html.read(), 'html.parser')


def write_soup(soup: BeautifulSoup, html_index_path: str) -> None:
    with open(html_index_path, 'w', encoding='utf-8') as html:
        html.write(str(soup))


def download_fonts(site_url: str, html_index_path: str, root_folder_save_to: str, site_relative_path: str = None, force_download: bool = False, debug: bool = False):
    # @font-face {  font-family: YAE5fD6jXa8-0;  src: url(fonts/668e204ecea8e06c27fb74af58a48107.woff2);  font-weight: 900;  font-style: normal;}
    site_root_url = os.path.split(site_url)[0]
    if site_root_url == 'http:' or site_root_url == 'https:':
        site_root_url = site_url
    if site_root_url.endswith('/'):
        site_root_url = site_root_url[:-1]
    pattern = r'(?:@font-face {)(?:.*?)(?:src: url\()(?P<font_url>[a-zA-Z0-9.\/:\-_]+)(?:\);(?:.*?);})'
    with open(html_index_path, 'r', encoding='utf-8') as html_raw:
        html_doc = html_raw.read()
        matches = re.findall(pattern, html_doc)
        fonts = list(set(matches))  # Get unique values
        if debug:
            print(fonts)
    for i in range(len(fonts)):
        font: str = fonts[i]
        if font.startswith('http'):
            # We ignore these urls because they are external resources and do
            # not need to be downloaded.
            pass
        else:
            if font.startswith('/'):
                # These types of urls point to the root domain of the url.
                font_url = f'{site_root_url}/{font[1:]}'
                filepath = os.path.join(root_folder_save_to, font[1:])
            else:
                # These are relative urls. We should treat them as such, but in
                # this case we'll be just more efficient if we just have all our
                # fonts in a centralized directory, so we will store them in the
                # root folder and convert the link accordingly:
                font_url = f'{site_root_url}/{font}'
                # filepath = join_path_parts_ignore_none(
                #     [root_folder_save_to, site_relative_path, font])
                filepath = os.path.join(root_folder_save_to, font)

            if os.path.exists(filepath) == False or force_download:
                print(f'Font {i+1} of {len(fonts)}: Downloading...')
                response = requests.get(font_url)
                if response.status_code == 200:
                    folder, filename = os.path.split(filepath)
                    if folder != '':
                        create_dir_recursively(folder)
                    open(filepath, "wb").write(response.content)
                else:
                    print(
                        f'Font {i+1} of {len(fonts)}: Error. See response: {response.text}.')
            else:
                print(
                    f'Font {i+1} of {len(fonts)}: Skipped. Already downloaded.')

    # As stated before, we move all fonts stored in relative directories to the
    # root of the site.
    # if site_relative_path != None or not html_index_path.endswith('index.html'):
    with open(html_index_path, 'w', encoding='utf-8') as html_raw:
        html_doc = html_doc.replace('src: url(fonts/', 'src: url(/fonts/')
        html_raw.write(html_doc)


def remove_all_inline_scripts(soup: BeautifulSoup, html_index_path: str):
    for elem in soup.find_all('script'):
        elem.clear()
    with open(html_index_path, 'w', encoding='utf-8') as html:
        html.write(str(soup))


def remove_inline_scripts_containing_keywords(html_index_path: str, keywords: list[str]):
    soup = get_soup(html_index_path)
    for elem in soup.find_all('script'):
        for keyword in keywords:
            if keyword in elem.text:
                elem.clear()
                break
    write_soup(soup, html_index_path)


def prepare_web_folder(folder: str):
    if not os.path.exists(folder):
        create_dir_recursively(folder)


def download_local_resources(site_url: str, html_index_path: str, root_folder_save_to: str, site_relative_path: str = None, force_download: bool = False, force_media_files_to_root: bool = False):
    soup = get_soup(html_index_path)
    root_url = os.path.split(site_url)[0]
    if root_url.endswith('/'):
        root_url = root_url[:-1]

    media_tags = ["img", "video", "image"]

    resources = {
        "link": "href",  # head
        "img": "src",
        "video": "src",
        "image": "href",  # images inside svg vectors
        "script": "src",
        "a": "href"
    }
    for tag, attribute in resources.items():
        elements = soup.find_all(tag)
        for i in range(len(elements)):
            base_msg = f'<{tag}> {i+1} of {len(elements)}'
            elem = elements[i]
            try:
                resource_path: str = elem[attribute]
                if tag != 'a':
                    # We only care about resources that are local to the website we
                    # are downloading.
                    if not resource_path.startswith('http'):
                        if resource_path.startswith('/'):
                            # Path relative to root
                            resource_url = root_url + resource_path
                            filepath = os.path.join(
                                root_folder_save_to, resource_path[1:])
                        else:
                            # Relative path
                            mid_part = '' if site_url.endswith('/') else '/'
                            resource_url = f'{site_url}{mid_part}{resource_path}'
                            if tag in media_tags and force_media_files_to_root == True:
                                filepath = join_path_parts_ignore_none(
                                    [root_folder_save_to, resource_path])
                                elem[attribute] = '/' + elem[attribute]
                            else:
                                filepath = join_path_parts_ignore_none(
                                    [root_folder_save_to, site_relative_path, resource_path])
                        if os.path.exists(filepath) == False or force_download:
                            print(f'{base_msg}: Downloading...')
                            response = requests.get(resource_url)
                            if response.status_code == 200:
                                folder, filename = os.path.split(filepath)
                                if folder != '':
                                    create_dir_recursively(folder)
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                            else:
                                print(
                                    f'{base_msg}: Download error. See response: {response.text}')
                        else:
                            print(
                                f'{base_msg}: Skipped. It is already downloaded. File: {filepath}')
                    else:
                        print(f'{base_msg}: Ignored. It is an external resource.')
                else:
                    print(f'{base_msg}: Ignored. Crawling not implemented yet.')
            except KeyError:
                print(f"{base_msg}: Ignored. It has no '{attribute}' attribute.")
    write_soup(soup, html_index_path)


def fix_links(html_index_path: str):
    soup = get_soup(html_index_path)
    pattern = r'^(?:.+?)?(?:\/_link\/\?link=)(?P<link>.+?)(?:&(?:amp;)?target=.*)$'
    compiled_pattern = re.compile(pattern)
    a_elements = soup.find_all('a')
    for elem in a_elements:
        try:
            link: str = elem["href"]
            match = re.match(compiled_pattern, link)
            if match != None:
                new_link = unquote(match.groupdict()["link"])
                match = re.match(compiled_pattern, new_link)
                if match != None:
                    new_link = unquote(match.groupdict()["link"])
                elem["href"] = new_link
        except KeyError:
            # Nothing to fix in link because it has no href attribute.
            pass
    write_soup(soup, html_index_path)


def add_google_analytics(html_index_path: str, google_analytics_id: str):
    soup = get_soup(html_index_path)
    script = BeautifulSoup(f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={google_analytics_id}"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){"{dataLayer.push(arguments);}"}
    gtag('js', new Date());

    gtag('config', '{google_analytics_id}');
    </script>
    """, 'html.parser')

    soup.head.insert(0, script)

    write_soup(soup, html_index_path)


def copy_meta_from_html(html_index_path: str, head_html_path=str):
    soup = get_soup(html_index_path)
    soup_head = get_soup(head_html_path)

    meta_elems = soup_head.head.find_all('meta')
    for meta in meta_elems:
        new_meta: Tag = meta
        attrs = {}
        for key in ["name", "property"]:
            try:
                attrs[key] = new_meta.attrs[key]
            except KeyError:
                pass
        print(attrs)
        if len(attrs.keys()) > 0:
            existing_meta = soup.head.find('meta', attrs)
            if existing_meta != None:
                existing_meta.decompose()
        soup.head.append(new_meta)

    new_tite = soup_head.head.title
    if new_tite != None:
        existing_title = soup.head.title
        if existing_title != None:
            existing_title.decompose()
        soup.head.append(new_tite)

    write_soup(soup, html_index_path)


def make_sure_links_open_in_current_tab(html_index_path: str, links: list[str]):
    soup = get_soup(html_index_path)
    for link in links:
        elems = soup.find_all('a', {"href": link, "target": "_blank"})
        for elem in elems:
            del elem["target"]
            del elem["rel"]
    write_soup(soup, html_index_path)


def inject_html_as_child_of_element(html_index_path: str, element_tag_name: str, element_attrs: dict[str, str], html_to_inject: str, inject_as: Literal['first_child', 'last_child', 'before', 'after'] = 'last_child'):
    soup = get_soup(html_index_path)
    elems = soup.find_all(element_tag_name, element_attrs)
    soup_to_inject = BeautifulSoup(html_to_inject, 'html.parser')
    for elem in elems:
        if inject_as == 'first_child':
            elem.insert(0, soup_to_inject)
        elif inject_as == 'last_child':
            elem.append(soup_to_inject)
        if inject_as == 'before':
            elem.insert_before(soup_to_inject)
        if inject_as == 'after':
            elem.insert_after(soup_to_inject)

    write_soup(soup, html_index_path)


class InjectDirective():
    def __init__(self, element_tag_name: str, element_attrs: dict[str, str], html_to_inject: str, inject_as: Literal['first_child', 'last_child', 'before', 'after'] = 'last_child') -> None:
        self.element_tag_name = element_tag_name
        self.element_attrs = element_attrs
        self.html_to_inject = html_to_inject
        self.inject_as = inject_as


def adjust_base_href(html_index_path: str, site_relative_path: str = None):
    soup = get_soup(html_index_path)
    elems = soup.find_all('base')
    for elem in elems:
        elem.decompose()
    if site_relative_path != None:
        new_base = soup.new_tag('base', attrs={'href': site_relative_path})
        soup.head.append(new_base)
    write_soup(soup, html_index_path)


def download_full_site(url: str, project_root_folder: str = None, site_relative_path: str = None, force_download: bool = False, google_analytics_id: str = None, links_to_force_open_in_current_tab: list[str] = [], save_html_as: str = 'index.html', inject_directives: list[InjectDirective] = [], force_media_files_to_root: bool = False, html_copy_meta_from: os.PathLike = None):

    download_root_folder = os.path.join('sites', project_root_folder)
    download_site_folder = join_path_parts_ignore_none(
        [download_root_folder, site_relative_path])
    index_path = os.path.join(download_site_folder, save_html_as)

    # Make sure the folders exist. If they don't, create them.
    prepare_web_folder(download_root_folder)
    prepare_web_folder(download_site_folder)
    # -------------------------------------------------

    download_html(url, index_path)
    adjust_base_href(index_path, site_relative_path)
    download_fonts(
        site_url=url,
        html_index_path=index_path,
        root_folder_save_to=download_root_folder,
        site_relative_path=site_relative_path,
        force_download=force_download,
    )
    download_local_resources(
        site_url=url,
        html_index_path=index_path,
        root_folder_save_to=download_root_folder,
        site_relative_path=site_relative_path,
        force_download=force_download,
        force_media_files_to_root=force_media_files_to_root
    )
    fix_links(index_path)
    remove_inline_scripts_containing_keywords(
        index_path,
        keywords=["modal_backdrop"])
    make_sure_links_open_in_current_tab(
        index_path,
        links_to_force_open_in_current_tab
    )
    for inject_directive in inject_directives:
        inject_html_as_child_of_element(
            html_index_path=index_path,
            element_tag_name=inject_directive.element_tag_name,
            element_attrs=inject_directive.element_attrs,
            html_to_inject=inject_directive.html_to_inject,
            inject_as=inject_directive.inject_as
        )
    if google_analytics_id != None:
        add_google_analytics(
            html_index_path=index_path,
            google_analytics_id=google_analytics_id)
    if html_copy_meta_from != None:
        copy_meta_from_html(
            html_index_path=index_path,
            head_html_path=html_copy_meta_from,
        )
