from .base import base_renderer, _command_renderer

def chapter_renderer(self):
    if self.suppressed:
        return _command_renderer('chaptertitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('chapter', base_renderer(self).strip() ) + u'\n'

def section_renderer(self):
    if self.suppressed:
        return _command_renderer('sectiontitlesuppressed', base_renderer(self).strip() ) + u'\n'
    else:
        return _command_renderer('section', base_renderer(self).strip() ) + u'\n'

def subsection_renderer(self):
    return _command_renderer('subsection', base_renderer(self).strip() ) + u'\n'

def subsubsection_renderer(self):
    return _command_renderer('subsubsection', base_renderer(self).strip() ) + u'\n'
