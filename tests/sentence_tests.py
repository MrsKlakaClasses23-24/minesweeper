from unittest import TestCase

from mine_sweeper_ai import KnowledgeSentence

class SentenceTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_basic_sentence(self):
        sentence = KnowledgeSentence({(0,1), (1,1), (1,2), (0,0),(0,2)}, 3)
        sentence.mark_mine((1,1))
        sentence.mark_safe((1,2))
        self.assertEqual({(0,1), (0,0), (0,2)}, sentence.cells)
        self.assertEqual(2, sentence.mine_count)
