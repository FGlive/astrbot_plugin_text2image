"""调试表格单元格解析"""
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from astrbot_plugin_text2image.core.markdown import _parse_inline_styles, TableCell, TableRow, LineContext, _serialize_table

def test_cell_parsing():
    """测试单元格内容解析"""
    cell_text = "张三"
    segments = _parse_inline_styles(cell_text)

    print(f"单元格文本: '{cell_text}'")
    print(f"解析后的片段数: {len(segments)}")
    for seg in segments:
        print(f"  text='{seg.text}', is_emoji={seg.is_emoji}")

def test_table_serialize():
    """测试表格序列化"""
    ctx = LineContext()

    # 模拟表格行
    header = TableRow(cells=[
        TableCell(text="姓名", segments=_parse_inline_styles("姓名")),
        TableCell(text="年龄", segments=_parse_inline_styles("年龄")),
    ], is_header=True)

    row = TableRow(cells=[
        TableCell(text="张三", segments=_parse_inline_styles("张三")),
        TableCell(text="25", segments=_parse_inline_styles("25")),
    ], is_header=False)

    ctx.table_rows = [header, row]

    result = _serialize_table(ctx)
    print(f"\n序列化结果片段数: {len(result)}")
    for i, seg in enumerate(result):
        print(f"{i+1}. text='{seg.text}', list_item={seg.list_item}")

if __name__ == "__main__":
    test_cell_parsing()
    test_table_serialize()
