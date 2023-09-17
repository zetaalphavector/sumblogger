import re


def markdown_to_html(markdown_file):
    with open(markdown_file) as f:
        markdown = f.read()
    # Replace headers
    markdown = re.sub(r"(?m)^# (.*)$", r"<h1>\1</h1>", markdown)
    markdown = re.sub(r"(?m)^## (.*)$", r"<h2>\1</h2>", markdown)
    markdown = re.sub(r"(?m)^### (.*)$", r"<h3>\1</h3>", markdown)
    markdown = re.sub(r"(?m)^#### (.*)$", r"<h4>\1</h4>", markdown)
    markdown = re.sub(r"(?m)^##### (.*)$", r"<h5>\1</h5>", markdown)
    markdown = re.sub(r"(?m)^###### (.*)$", r"<h6>\1</h6>", markdown)

    # Replace bold and italic text
    markdown = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", markdown)
    markdown = re.sub(r"\*(.*?)\*", r"<em>\1</em>", markdown)

    # Replace links
    markdown = re.sub(
        r'\[(.*?)\]\((.*?)\s+"\[(.*?)\]\: (.*?)"\)',
        # r'<a class="tip" target=”_blank” href="\2" title="\3">\1</a>',
        r'<a class="tip" target=”_blank” href="\2">\1<span><b>\3</b><br><br>\4</span></a>',
        markdown,
    )
    # markdown = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', markdown)

    # Replace line breaks
    # markdown = re.sub(r"\n\n", r"<br><br>", markdown)
    markdown = re.sub(r"\n", r"<br>", markdown)

    # Wrap the content in a div
    html = f"<div>{markdown}</div>"
    style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            font-weight: bold;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
       h1 {
            font-size: 2em;
        }
        h2 {
            font-size: 1.5em;
        }
        h3 {
            font-size: 1.3em;
        }
        h4 {
            font-size: 1.1em;
        }
        a {
            color: #1a0dab;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        strong {
            font-weight: bold;
        }
        em {
            font-style: italic;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        iframe {
            max-width: 100%;
            height: auto;
        }
        a.tip {
            border-bottom: 1px dashed;
            text-decoration: none
        }
        a.tip:hover {
            cursor: help;
            position: relative
        }
        a.tip span {
            display: none
        }
        a.tip:hover span {
            opacity: 0.95;
            border: #c0c0c0 1px dotted;
            padding: 5px 5px 5px 5px;
            display: block;
            z-index: 100;
            background: #FAF9F6;
            left: -50px;
            margin: 10px;
            width: 300px;
            position: absolute;
            top: 10px;
            text-decoration: none;
            font-size: small;
            
        }
    </style>
    """
    html = f"<!DOCTYPE html><html><head>{style}</head><body>{html}</body></html>"

    return html


def create_html(markdown_file, output_html_file_path):
    blog_html = markdown_to_html(markdown_file)
    with open(output_html_file_path, "w") as f:
        f.write(blog_html)
