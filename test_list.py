"""测试列表渲染功能"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.renderer import TextRenderer
from core.styles import TextSegment


def test_list_render():
    """测试列表渲染"""

    # 测试文本，包含无序列表、有序列表和缩进列表
    test_text = """# 列表测试

## 无序列表
- 第一项
* 第二项
+ 第三项

## 有序列表
1. 第一项
2. 第二项
3. 第三项

## 嵌套列表
- 一级项目 1
  - 二级项目 1
  - 二级项目 2
- 一级项目 2

## 混合内容
这是一段普通文本。

- 列表项 1
- 列表项 2
- **粗体列表项**
- *斜体列表项*
- `代码列表项`

1. 有序 1
2. 有序 2

> 引用块
> - 引用中的列表"""

    config = {
        "image_width": 375,
        "image_scale": 2,
        "padding": 24,
        "font_size": 24,
        "line_height": 1.6,
        "bg_color": "#ffffff",
        "text_color": "#333333",
    }

    font_dir = Path(__file__).parent / "ziti"
    renderer = TextRenderer(config, font_dir)

    result = renderer.render(test_text)
    if result:
        print(f"图片已保存到: {result}")
        # 复制到桌面方便查看
        import shutil
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            dest = desktop / "test_list_output.jpg"
            shutil.copy(result, dest)
            print(f"图片已复制到桌面: {dest}")
    else:
        print("渲染失败")


if __name__ == "__main__":
    test_list_render()
