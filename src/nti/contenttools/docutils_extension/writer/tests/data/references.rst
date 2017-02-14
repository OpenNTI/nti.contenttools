-------------
Inline Styles
-------------

++++++++
Emphasis
++++++++

This paragraph that will have **bold** and *italics* in it. We need to try nesting them like ** bold and *italic***, ***bold/italic***, and *italic and **bold*** (this format does not work).

Paragraph with an escaped \* in emphasis *Italics \* and a astrick*

++++++++++
References
++++++++++

This paragraph will have different styles of links that RST supports. Such as `External Hyperlink Targets`_. Also the embedded URI format, details found `here <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#embedded-uris>`_.

We will also need to test internal hyperlink targets. Like linking to the `Inline Styles`_ section. I wonder if the embedded URI format will for for this `Test Link <Emphasis>`_ (It Treats it as a URI so I guess it doesn't).

.. _External Hyperlink Targets: http://docutils.sourceforge.net/docs/user/rst/quickref.html#hyperlink-targets
