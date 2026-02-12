"""测试标题自动换行功能"""

from pathlib import Path
from core.renderer import TextRenderer

def test_heading_wrap():
    """测试标题自动换行"""
    # 配置
    config = {
        "image_width": 375,
        "image_scale": 2,
        "padding": 24,
        "font_size": 24,
        "line_height": 1.6,
        "bg_color": "#ffffff",
        "text_color": "#333333",
    }

    font_dir = Path(__file__).parent / "fonts"
    renderer = TextRenderer(config, font_dir)

    # 测试用例
    test_cases = [
        # 1. 超长标题
        "# 这是一个非常非常非常非常非常非常非常非常非常非常长的标题，应该会自动换行",

        # 2. 中等长度标题
        "## 这是一个中等长度的标题，测试自动换行功能是否正常工作",

        # 3. 短标题
        "### 短标题",

        # 4. 普通文本
        "这是一段普通的文本，不包含标题，用来测试回归功能是否正常。",

        # 5. 混合样式
        "# **加粗**的*标题*，`代码`测试",

        # 6. 标题后跟正文
        "# 长标题自动换行测试\n这是正文内容，应该在标题下方正常显示。",

        # 7. 多级标题
        "# 一级标题\n## 二级标题\n### 三级标题",

        # 8. 标题与引用混合
        "# 标题\n> 引用内容\n继续正文",
    ]

    for i, test_text in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}:")
        print(f"{'='*60}")
        print(test_text)
        print(f"{'='*60}")

        result = renderer.render(test_text)
        if result:
            print(f"✓ 渲染成功: {result}")
        else:
            print(f"✗ 渲染失败")

if __name__ == "__main__":
    test_heading_wrap()
