#!/usr/bin/env python

"""
This parses out assessment questions from text blocks.  Currently it can handle multiple choice, multiple choice multiple answer, and short answer.

"""



import os
import sys

from .types import *

class _Parser( object ):

    def __init__( self ):
        self.state = 'IDLE'
        self._val = None
        self.handlers = {}

class NTITagParser( _Parser ):

    def __init__(self):
        super( NTITagParser, self ).__init__()

        self.handlers['ASSESSMENT'] = AssessmentParser()
        self.handlers['IDLE'] = IdleParser()

    def parse_line(self, line):
        s, v = self.handlers[ self.state ].parse( line )
        if s in self.handlers:
            self.state = s
            self._val = v

        return (self.state, self._val)

class IdleParser( _Parser ):

    def parse( self, line ):
        if '[' == line[0]:
            if 'question' in line:
                self.state = 'ASSESSMENT'
            else:
                self.state = 'IDLE'

        return ( self.state, self._val )

class AssessmentParser( _Parser ):

    def __init__( self ):
        super( AssessmentParser, self ).__init__()

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
        self.hint = NAQHints()

    def parse( self, line ):
        # Determine the current parser state
        if '[' == line[0]:
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
            self.handlers[self.state]( line )
        else:
            # State is unchanged since the last pass, so we need to parse the state's data
            if self.state in self.handlers:
                self.handlers[self.state]( line )
            else:
                print('Unparsed line: %s' % line)

        return (self.state, self._val)

    def _question_handler( self, line ):
        self.question = TextNode( line.strip() )

    def _choice_handler( self, line ):
        if line[0] in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
            self.choice_list.append( TextNode( ' '.join(line.split()[1:]).strip() ))

    def _solution_handler( self, line ):
        if line.strip()[0] in [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
            self.answer_list.extend( line.strip().split(',') )
            for i in range(len(self.answer_list)):
                self.answer_list[i] = int(self.answer_list[i])-1
        else:
            if self.choice_list:
                for i in range(len(self.choice_list)):
                    if line.strip() == self.choice_list[i]:
                        self.answer_list.append(i)
            else:
                self.solutions.add_child( NAQSolution( line.strip(), '1' ) )

    def _hint_handler( self, line ):
        self.hint.add_child( NAQHint( line.strip() ) )

    def _finished_handler( self, line ):
        # Determine which question type we are
        elem = None
        if self.choice_list:
            if len(self.answer_list) > 1:
                elem = NAQMultipleChoiceMultipleAnswerPart()
            else:
                elem = NAQMultipleChoicePart()
        else:
            elem = NAQFreeResponsePart()

        # Add the question text child
        elem.add_child( self.question )

        # Add the choices / solutions child as applicable
        if self.choice_list:
            for i in range(len(self.choice_list)):
                if i in self.answer_list:
                    self.choices.add_child( NAQChoice(self.choice_list[i], '1') )
                else:
                    self.choices.add_child( NAQChoice(self.choice_list[i]) )
            elem.add_child(self.choices)
        else:
            elem.add_child(self.solutions)

        # Add the hints child
        elem.add_child(self.hint)

        # Create the naquestion element and add the question part as a child
        self._val = NAQuestion()
        self._val.add_child( elem )
 
        # Update parser state to IDLE and reset the parser datastructures
        self.state = 'IDLE'
        self._reset()

    def _idle_handler( self, line ):
        self.state = 'ASSESSMENT-QUESTION'
        self._val = None

        # Handle the question
        self.handlers[self.state]( line )

def main():
    data = []
    tag_parser = NTITagParser()
    # Get the input
    with open( sys.argv[1:][0], 'rb' ) as input:
        for line in input:
            state, val = tag_parser.parse_line(line)

            if val:
                sys.stdout.write( str( val ) )
                sys.stdout.write('\n')
                sys.stdout.write('\n')
                sys.stdout.flush()

if __name__ == '__main__': # pragma: no cover
    main()
