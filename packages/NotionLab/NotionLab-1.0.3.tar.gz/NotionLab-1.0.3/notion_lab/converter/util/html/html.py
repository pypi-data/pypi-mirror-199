from typing import Dict

text_mapping: Dict = {
    "heading_1": "h1",
    "heading_2": "h2",
    "heading_3": "h3",
    "paragraph": "p",
    "quote": "blockquote"
}


def div(child: Dict):
    """
    <div> 元素生成器
    """
    style = f"""
        style="display: inline; {style_parser(child["annotations"])}"
    """
    return f"""
        {f'<a href="{child["href"]}">' if child["href"] else ""}
            {f'<code>' if child["annotations"]["code"] else ""}
                <div {style}>
                    {child["text"]["content"]}
                </div>
            {f'</code>' if child["annotations"]["code"] else ""}
        {'</a>' if child["href"] else ""}
    """


def style_parser(annotations):
    """
    样式组合器
    """
    style = ""
    if annotations["bold"]:
        # 加粗
        style += 'font-weight: bold;'
    if annotations["italic"]:
        # 斜体
        style += 'font-style: italic;'
    if annotations["underline"] or annotations["strikethrough"]:
        # 下划线和删除线
        style += f"""
        text-decoration: {"underline" if annotations["underline"] else ""} 
        {"line-through" if annotations["strikethrough"] else ""};
        """
    if annotations["color"] and annotations["color"] != "default":
        # 字体颜色和背景颜色（二选一）
        if "_background" in annotations["color"]:
            style += f'background: {annotations["color"][:-11:1]};'
        else:
            style += f'color: {annotations["color"]};'
    return style
