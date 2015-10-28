#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This parses out assessment questions from text blocks.
Currently it can handle multiple choice, multiple choice multiple answer, and short answer.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys

from .types import _Node, TextNode

class NAQChoice(_Node):
	pass

class NAQChoices(_Node):
	pass

class NAQSolution(_Node):
	pass

class NAQSolutions(_Node):
	pass

class NAQHint(_Node):
	pass

class NAQHints(_Node):
	pass

class NAQuestionPart(_Node):
	pass

class NAQuestion(_Node):
	pass

class _Parser(object):

	def __init__(self):
		self.state = 'IDLE'
		self._val = None
		self.handlers = {}

class NTITagParser(_Parser):

	def __init__(self):
		super(NTITagParser, self).__init__()

		self.handlers['ASSESSMENT'] = AssessmentParser()
		self.handlers['IDLE'] = IdleParser()

	def parse_line(self, line):
		s, v = self.handlers[ self.state ].parse(line)
		if s in self.handlers:
			self.state = s
			self._val = v

		return (self.state, self._val)

class IdleParser(_Parser):

	def parse(self, line):
		if len(line) > 0 and '[' == line[0]:
			if 'question' in line:
				self.state = 'ASSESSMENT'
			else:
				self.state = 'IDLE'
		else:
			self.state = 'IDLE'

		return (self.state, self._val)

class AssessmentParser(_Parser):

	def __init__(self):
		super(AssessmentParser, self).__init__()

		self._reset()

		self.handlers['IDLE'] = self._idle_handler
		self.handlers['ASSESSMENT-QUESTION'] = self._question_handler
		self.handlers['ASSESSMENT-CHOICES'] = self._choice_handler
		self.handlers['ASSESSMENT-SOLUTIONS'] = self._solution_handler
		self.handlers['ASSESSMENT-HINTS'] = self._hint_handler
		self.handlers['ASSESSMENT-FINISHED'] = self._finished_handler

	def _reset(self):
		self.question = ''
		self.choice_list = []
		self.answer_list = []
		self.choices = NAQChoices()
		self.solutions = NAQSolutions()
		self.hint = None

	def parse(self, line):

		# Determine the current parser state
		if len(line) > 0 and '[' == line[0]:
			if 'question' in line:
				self.state = 'ASSESSMENT-QUESTION'
			elif 'choices' in line:
				self.state = 'ASSESSMENT-CHOICES'
			elif 'answers' in line:
				self.state = 'ASSESSMENT-SOLUTIONS'
			elif 'hint' in line:
				self.state = 'ASSESSMENT-HINTS'
		elif line.strip() == '':
			self.state = 'ASSESSMENT-FINISHED'
			self.handlers[self.state](line)
		else:
			# State is unchanged since the last pass, so we need to parse the state's data
			if self.state in self.handlers:
				self.handlers[self.state](line)
			else:
				print('Unparsed line: %s' % line)

		return (self.state, self._val)

	def _question_handler(self, line):
		self.question = TextNode(line.strip() + u'\n')

	def _choice_handler(self, line):
		if line[0] in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
			self.choice_list.append(TextNode(' '.join(line.split()[1:]).strip()))

	def _solution_handler(self, line):
		if line.strip()[0] in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
			self.answer_list.extend(line.strip().split(','))
			for i in range(len(self.answer_list)):
				self.answer_list[i] = int(self.answer_list[i]) - 1
		else:
			if self.choice_list:
				for i in range(len(self.choice_list)):
					if line.strip() == self.choice_list[i]:
						self.answer_list.append(i)
			else:
				solution = NAQSolution()
				solution.optional = '1'
				solution.add_child(TextNode(line.strip()))
				self.solutions.add_child(solution)

	def _hint_handler(self, line):
		if self.hint is None:
			self.hint = NAQHints()

		if line.strip() is not '':
			hint = NAQHint()
			hint.add_child(TextNode(line.strip()))
			self.hint.add_child(hint)
		else:
			self.hint = None

	def _finished_handler(self, line):
		elem = NAQuestionPart()

		if self.choice_list:
			if len(self.answer_list) > 1:
				elem.type = 'MultipleChoiceMultipleAnswer'
			else:
				elem.type = 'MultipleChoice'
		else:
			elem = 'FreeResponse'

		# Add the question text child
		elem.add_child(self.question)

		# Add the choices / solutions child as applicable
		if self.choice_list:
			for i in range(len(self.choice_list)):
				if i in self.answer_list:
					choice = NAQChoice()
					choice.optional = '1'
					choice.add_child(TextNode(self.choice_list[i]))
					self.choices.add_child(choice)
				else:
					choice = NAQChoice()
					choice.add_child(TextNode(self.choice_list[i]))
					self.choices.add_child(choice)
			elem.add_child(self.choices)
		else:
			elem.add_child(self.solutions)

		# Add the hints child if any
		if self.hint is not None:
			elem.add_child(self.hint)

		# Create the naquestion element and add the question part as a child
		self._val = NAQuestion()
		self._val.add_child(elem)

		# Update parser state to IDLE and reset the parser datastructures
		self.state = 'IDLE'
		self._reset()

	def _idle_handler(self, line):
		self.state = 'ASSESSMENT-QUESTION'
		self._val = None

		# Handle the question
		self.handlers[self.state](line)

def main():
	tag_parser = NTITagParser()
	with open(sys.argv[1:][0], 'rb') as fp:
		for line in fp:
			_, val = tag_parser.parse_line(line)
			if val:
				sys.stdout.write(str(val))
				sys.stdout.write('\n')
				sys.stdout.write('\n')
				sys.stdout.flush()

if __name__ == '__main__':  # pragma: no cover
	main()
