from .base import base_renderer, _command_renderer, _environment_renderer

def question_renderer( self ):
    return _environment_renderer(self, 'naquestion', '')

def question_part_renderer( self ):
    result = u''
    if self.type == 'MultipleChoiceMultipleAnswer':
        result = _environment_renderer(self, 'naqmultiplechoicemultipleanswerpart', '')
    elif self.type == 'MultipleChoice':
        result = _environment_renderer(self, 'naqmultiplechoicepart', '')
    else:
        result = _environment_renderer(self, 'naqfreeresponsepart', '')
    return result

def choices_renderer( self ):
    return _environment_renderer(self, 'naqchoices', '')

def choice_renderer( self ):
    optional = u''
    if hasattr(self, 'optional') and self.optional:
        optional = u'[%s]' % self.optional
    return u'\\naqchoice%s %s\n' % (optional, base_renderer(self))

def solutions_renderer( self ):
    return _environment_renderer(self, 'naqsolutions', '')

def solution_renderer( self ):
    optional = u''
    if hasattr(self, 'optional') and self.optional:
        optional = u'[%s]' % self.optional
    return u'\\naqsolution%s %s\n' % (optional, base_renderer(self))

def hints_renderer( self ):
    return _environment_renderer(self, 'naqhints', '')

def hint_renderer( self ):
    return u'\\naqhint %s\n' % base_renderer(self)

def explanation_renderer( self ):
    return _environment_renderer(self, 'naqexplanation', '')

