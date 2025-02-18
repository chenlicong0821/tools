import os
import sys
import requests
import time
import configparser
from bs4 import BeautifulSoup
import pdfkit


def extract_url_from_file(file_path):
    content = file_path.read()
    # print("File Content:\n", content)
    config = configparser.ConfigParser()
    config.read_string(content)  # 使用 read_string 直接读取内容
    # config.read(file_path, encoding="utf-8")  # 指定编码以防止中文路径问题
    # 检查 sections
    # print("Sections:", config.sections())
    # 提取 URL 字段的值
    url = config.get("InternetShortcut", "URL", fallback=None)
    return url


def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # 移除不需要的部分，例如广告、导航栏、页脚等
    for element in soup(["header", "footer", "aside", "nav", "script", "style"]):
        # print("Element:", element)
        element.decompose()

    return str(soup)


def url_to_pdf(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        cleaned_html = clean_html(response.text)
        # print("Cleaned HTML:\n", cleaned_html)
        # options = {
        #     "no-stop-slow-scripts": None,
        #     "javascript-delay": 1000,  # 增加延迟时间
        #     "load-error-handling": "ignore",  # 忽略加载错误
        # }
        # 将清理后的HTML内容转换为PDF格式，并保存到指定的输出路径
        pdfkit.from_string(cleaned_html, output_path)
        print(f"Saved {url} to {output_path}")
    except Exception as e:
        print(f"Failed to convert {url} to PDF: {e}")


def main(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".url"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                url = extract_url_from_file(file)
                print("Extracted URL:", url)
                output_pdf = os.path.join(
                    directory, f"{os.path.splitext(filename)[0]}.pdf"
                )
                url_to_pdf(url, output_pdf)
                time.sleep(1)


if __name__ == "__main__":
    directory_path = sys.argv[1] if len(sys.argv) > 1 else "."
    main(directory_path)
