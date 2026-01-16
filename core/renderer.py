"""文本渲染器"""

import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from .styles import TextSegment
from .emoji import EmojiHandler

# 不能出现在行首的标点符号（避头标点）
NO_LINE_START = set('，。、；：？！）】》」』"\',.;:?!)>]}·…—～')


class TextRenderer:
    """文本渲染器"""
    
    def __init__(self, config: Dict[str, Any], font_dir: Path):
        self.config = config
        self.font_dir = font_dir
        self.emoji_handler = EmojiHandler(font_dir)
        self._font_cache: Dict[str, ImageFont.FreeTypeFont] = {}
    
    def _get_config(self, key: str, default: Any) -> Any:
        return self.config.get(key, default)
    
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """加载字体"""
        cache_key = f"{size}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        font_path = self.font_dir / "Source_Han_Serif_SC_Light_Light.otf"
        try:
            font = ImageFont.truetype(str(font_path), size=size)
            self._font_cache[cache_key] = font
            return font
        except Exception:
            return ImageFont.load_default()
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """十六进制转 RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def render(self, text: str) -> Optional[str]:
        """渲染文本为图片"""
        # 配置
        width = int(self._get_config("image_width", 375))
        scale = int(self._get_config("image_scale", 2))
        padding = int(self._get_config("padding", 24))
        font_size = int(self._get_config("font_size", 24))
        line_height = float(self._get_config("line_height", 1.6))
        bg_color = str(self._get_config("bg_color", "#ffffff"))
        text_color = str(self._get_config("text_color", "#333333"))
        
        real_width = width * scale
        real_padding = padding * scale
        real_font_size = font_size * scale
        emoji_size = int(real_font_size * 1.1)
        text_area_width = real_width - real_padding * 2
        
        font = self._load_font(real_font_size)
        ascent, descent = font.getmetrics()
        font_height = ascent + descent
        line_pixel_height = int(real_font_size * line_height)
        
        # 按行分割并处理
        lines = text.split('\n')
        render_lines = []  # [(segments, is_empty), ...]
        
        for line in lines:
            if not line.strip():
                render_lines.append(([], True))
                continue
            
            segments = self.emoji_handler.split_text(line)
            line_segments = []  # [(segment, width), ...]
            current_x = 0
            
            for seg in segments:
                if seg.is_emoji:
                    if current_x + emoji_size > text_area_width and current_x > 0:
                        render_lines.append((line_segments, False))
                        line_segments = []
                        current_x = 0
                    line_segments.append((seg, emoji_size))
                    current_x += emoji_size
                elif seg.no_wrap:
                    seg_width = int(font.getlength(seg.text))
                    line_segments.append((seg, seg_width))
                    current_x += seg_width
                else:
                    chars = list(seg.text)
                    for i, char in enumerate(chars):
                        char_width = int(font.getlength(char))
                        # 检查是否需要换行
                        need_wrap = current_x + char_width > text_area_width and current_x > 0
                        # 如果当前字符是避头标点，不换行（让它跟在上一行末尾）
                        if need_wrap and char in NO_LINE_START:
                            need_wrap = False
                        
                        # 检查是否会导致下一行只有一个字符
                        # 如果当前是倒数第二个字符，且换行后下一个字符会独占一行，则提前换行
                        if not need_wrap and i == len(chars) - 2 and line_segments:
                            next_char = chars[i + 1]
                            next_width = int(font.getlength(next_char))
                            # 如果当前字符放下后，下一个字符放不下，会导致单字符独占一行
                            if current_x + char_width + next_width > text_area_width:
                                # 提前换行，把当前字符和下一个字符都放到新行
                                render_lines.append((line_segments, False))
                                line_segments = []
                                current_x = 0
                                need_wrap = False  # 已经换行了
                        
                        if need_wrap:
                            render_lines.append((line_segments, False))
                            line_segments = []
                            current_x = 0
                        line_segments.append((TextSegment(text=char), char_width))
                        current_x += char_width
            
            if line_segments:
                render_lines.append((line_segments, False))
        
        # 后处理：避免单个字符独占一行
        # 如果某行只有一个普通字符（非emoji、非分隔符），把它合并到上一行
        merged_lines = []
        for i, (segments, is_empty) in enumerate(render_lines):
            if is_empty:
                merged_lines.append((segments, is_empty))
                continue
            
            # 统计内容：排除分隔符(no_wrap)
            normal_chars = sum(1 for seg, _ in segments if not seg.is_emoji and not seg.no_wrap and seg.text.strip())
            emoji_count = sum(1 for seg, _ in segments if seg.is_emoji)
            separator_count = sum(1 for seg, _ in segments if seg.no_wrap)
            
            total_items = normal_chars + emoji_count
            
            # 如果只有1个普通字符（没有emoji和分隔符）且有上一行可以合并
            if total_items == 1 and separator_count == 0 and merged_lines and not merged_lines[-1][1]:
                # 合并到上一行
                prev_segments, _ = merged_lines[-1]
                prev_segments.extend(segments)
            else:
                merged_lines.append((segments, is_empty))
        
        render_lines = merged_lines
        
        # 计算画布高度
        total_height = 0
        for segments, is_empty in render_lines:
            total_height += int(line_pixel_height * 0.5) if is_empty else line_pixel_height
        canvas_height = total_height + real_padding * 2
        
        # 创建画布
        bg_rgb = self._hex_to_rgb(bg_color)
        text_rgb = self._hex_to_rgb(text_color)
        canvas = Image.new("RGBA", (real_width, canvas_height), (*bg_rgb, 255))
        draw = ImageDraw.Draw(canvas)
        
        # 绘制
        y = real_padding
        for segments, is_empty in render_lines:
            if is_empty:
                y += int(line_pixel_height * 0.5)
                continue
            
            x = real_padding
            for seg, w in segments:
                if seg.is_emoji:
                    emoji_img = self.emoji_handler.render_emoji(seg.text, emoji_size)
                    if emoji_img:
                        emoji_y = y + (line_pixel_height - emoji_size) // 2
                        canvas.paste(emoji_img, (x, emoji_y), emoji_img)
                        x += w
                    # emoji 渲染失败时跳过，不占用空间
                else:
                    text_y = y + (line_pixel_height - font_height) // 2
                    draw.text((x, text_y), seg.text, font=font, fill=text_rgb)
                    x += w
            y += line_pixel_height
        
        # 保存
        return self._save_image(canvas, bg_rgb)
    
    def _save_image(self, canvas, bg_rgb) -> str:
        """保存图片（JPEG 格式）"""
        tmp = tempfile.NamedTemporaryFile(prefix="text2img_", suffix=".jpg", delete=False)
        canvas_rgb = Image.new("RGB", canvas.size, bg_rgb)
        canvas_rgb.paste(canvas, mask=canvas.split()[3] if canvas.mode == 'RGBA' else None)
        canvas_rgb.save(tmp.name, format="JPEG", quality=80)
        return tmp.name
