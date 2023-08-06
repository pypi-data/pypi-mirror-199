import itertools
import logging


import cv2
from docstruct.paragraph_detection.paragraph_extractor import ParagraphExtractor

from docstruct.visual_detection.bordered_table_extraction import BorderedTableExtractor
from docstruct.visual_detection.vis_line_detection import (
    VisLineDetector,
)
from .paragraph_detection.paragraph_sorter import sort_areas
from .textract_parser import TextractParser
from .text_block import Word, Line, Paragraph, Page, TextBlock, Table
import cv2
import logging
import math


class PageCreator:
    def __init__(
        self,
        image_path: str,
        textract_response: dict = None,
        debug: bool = False,
    ):
        self.image_path = image_path
        self.textract_response = textract_response
        self.debug = debug
        self.image = cv2.imread(image_path)

        self.image_height, self.image_width = self.image.shape[:2]

    def sort_lines(self, lines: list[Line]) -> list[Line]:
        """
        Sort the lines
        """
        sorted_line_indexes = TextBlock.sort(lines, return_indexes=True)
        sorted_lines = [lines[i] for i in sorted_line_indexes]
        return sorted_lines

    def extract_paragraphs(
        self, lines: list[Line], lines_segments: bool = False, height_offset: float = 0
    ) -> list[Paragraph]:
        """
        Parse the paragraphs
        """

        paragraphs_extractor = ParagraphExtractor(
            lines=lines, height_offset=height_offset, lines_segments=lines_segments
        )
        paragraphs = paragraphs_extractor.extract_paragraphs()
        return paragraphs

    def remove_words_from_lines(
        self, lines: list[Line], words: set[Word]
    ) -> list[Line]:
        """
        Remove the given words from the lines
        """
        # sorted_words = TextBlock.sort(list(words))
        non_empty_lines = []
        for line in lines:
            table_words = []
            for word in line.children:
                if word in words:
                    table_words.append(word)
            if not table_words:
                non_empty_lines.append(line)
                continue

            if len(table_words) == len(line.children):
                continue
            non_table_words = [
                word for word in line.children if word not in table_words
            ]
            line.children = non_table_words
            line.set_length()
            line.set_bounding_box()
            non_empty_lines.append(line)
        return non_empty_lines

    def get_tables(self, words: list[Word]) -> list[Table]:
        try:
            avg_word_size_ver = self.get_average_word_height(words)
            avg_word_size_hor = avg_word_size_ver * self.image_height / self.image_width
            image_length_threshold = int(avg_word_size_ver * self.image_height)

            ver_threshold = avg_word_size_ver
            hor_threshold = avg_word_size_hor
            vis_line_detector = VisLineDetector(image_path=self.image_path, words=words)
            hor_lines, ver_lines = vis_line_detector.detect_lines(
                hor_threshold, ver_threshold, image_length_threshold
            )

            table_detector = BorderedTableExtractor(
                words,
                hor_lines,
                ver_lines,
                hor_threshold,
                ver_threshold,
            )

            tables = table_detector.detect_tables()
            return tables
        except Exception as e:
            logging.error(f"Error: {e}")
            return []

    def create_page(self) -> Page:

        parser = TextractParser(self.textract_response)
        lines = parser.parse_response()
        lines = self.sort_lines(lines)
        words = [word for line in lines for word in line.children]
        if not words:
            return Page()

        tables = self.get_tables(words)
        table_words = list(itertools.chain(*(table.get_all(Word) for table in tables)))
        lines = self.remove_words_from_lines(lines, set(table_words))
        lines_paragraphs = self.extract_paragraphs(lines=lines, lines_segments=True)
        height_offset = self.space_distribution(lines_paragraphs)
        paragraphs = self.extract_paragraphs(lines=lines, height_offset=height_offset)
        areas = paragraphs + tables
        areas = sort_areas(areas)
        page = Page(children=areas)
        page.set_bounding_box()
        page.set_length()
        return page

    @staticmethod
    def round_up(n: float, decimals: float = 0) -> float:
        multiplier = 10**decimals
        return math.ceil(n * multiplier) / multiplier

    @staticmethod
    def space_distribution(lines: list[Paragraph]) -> float:
        """
        Get the space distribution of the document
        """
        space_distribution = []
        paragraphs = list(lines)
        for i, paragraph in enumerate(paragraphs[:-1]):
            space = abs(
                paragraph.get_bounding_box().get_center().get_y()
                - paragraphs[i + 1].get_bounding_box().get_center().get_y()
            )
            space_distribution.append(space)

        space_distribution = sorted(space_distribution)
        total = sum(space_distribution)
        running_sum = 0
        for space in space_distribution:
            running_sum += space
            if running_sum / total >= 0.05:
                return PageCreator.round_up(space, 3)
        return 0

    def get_average_word_height(self, words: list[Word]) -> float:
        """Get the average size of a list of words."""
        heights = [word.bounding_box.get_height() for word in words]
        if not heights:
            return 0
        return sum(heights) / len(heights)
