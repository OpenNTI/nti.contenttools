from .base import _environment_renderer

def body_renderer(self):
    return _environment_renderer(self, 'document', '')
