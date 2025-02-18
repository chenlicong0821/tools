### 说明：

1. **读取URL文件**：脚本会遍历指定目录下的所有`.url`文件，读取其中的URL。

2. **获取网页内容**：使用`requests`库获取网页的HTML内容。

3. **清理网页内容**：使用`BeautifulSoup`解析HTML，并去除指定的HTML元素（如`header`、`footer`、`aside`等），以去掉网页的头部和侧边栏。

4. **转换为PDF**：使用`pdfkit`将清理后的HTML内容转换为PDF文件。

5. **保存PDF文件**：将生成的PDF文件保存到与URL文件相同的目录下。

### 依赖安装：

你需要安装以下Python库：

```bash
pip install requests beautifulsoup4 pdfkit
```

此外，`pdfkit`依赖于`wkhtmltopdf`，你需要在系统中安装它。可以通过以下命令安装：

- **Ubuntu**: `sudo apt-get install wkhtmltopdf`
- **MacOS**: `brew install wkhtmltopdf`
- **Windows**: 下载并安装 [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)。

请根据你的需求调整`clean_html`函数，以去除不需要的网页部分。
