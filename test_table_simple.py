"""简单测试表格渲染"""
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from astrbot_plugin_text2image.core.markdown import parse_markdown, LineContext

def test_table():
    """测试表格转换为列表"""
    test_lines = [
        "| 姓名 | 年龄 | 城市 |",
        "|------|------|------|",
        "| 张三 | 25 | 北京 |",
        "| 李四 | 30 | 上海 |",
        "",  # 空行触发表格结束
        "表格后面的文本"
    ]

    ctx = LineContext()
    all_segments = []

    print("=== 表格行解析过程 ===")
    for line in test_lines:
        segments = parse_markdown(line, ctx)
        print(f"行: '{line}'")
        print(f"  上下文: in_table={ctx.in_table}, rows={len(ctx.table_rows)}")
        print(f"  返回片段数: {len(segments)}")
        if segments:
            for seg in segments:
                print(f"    - text='{seg.text[:30]}...', list_item={seg.list_item}, no_wrap={seg.no_wrap}")
        all_segments.extend(segments)
        print()

    print("=== 最终结果 ===")
    print(f"总片段数: {len(all_segments)}")
    for i, seg in enumerate(all_segments):
        print(f"{i+1}. text='{seg.text[:40]}...', list_item={seg.list_item}, code={seg.code}, no_wrap={seg.no_wrap}")

if __name__ == "__main__":
    test_table()
