<?xml version='1.0'?>
<!--#############################################################################
 |	$Id: test.xsl,v 1.4 2004/01/05 06:09:57 j-devenish Exp $
 |- #############################################################################
 |	$Author: j-devenish $
 |
 + ############################################################################## -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

<xsl:import href="file:///opt/local/share/dblatex/xsl/latex_book.xsl" />

<xsl:output method="text" encoding="utf-8" indent="yes"/>
<xsl:variable name="imagedata.file.check">0</xsl:variable>
<xsl:variable name="imagedata.default.scale">width=400px</xsl:variable>
<xsl:variable name="latex.inputenc">utf-8</xsl:variable>

<xsl:variable name="latex.biblio.output">all</xsl:variable>
<xsl:variable name="latex.document.font">default</xsl:variable>

<xsl:variable name="insert.xref.page.number">0</xsl:variable>
<xsl:variable name="latex.use.varioref">1</xsl:variable>

<xsl:variable name="latex.use.babel">1</xsl:variable>
<xsl:variable name="latex.use.hyperref">1</xsl:variable>
<xsl:variable name="latex.use.fancyvrb">1</xsl:variable>
<xsl:variable name="latex.use.fancybox">1</xsl:variable>
<xsl:variable name="latex.use.fancyhdr">1</xsl:variable>
<xsl:variable name="latex.use.subfigure">1</xsl:variable>
<xsl:variable name="latex.use.rotating">1</xsl:variable>
<xsl:variable name="latex.use.makeidx">0</xsl:variable>
<xsl:variable name="latex.pdf.support">0</xsl:variable>
<xsl:variable name="latex.math.support">1</xsl:variable>
<xsl:variable name="xref.hypermarkup">1</xsl:variable>
<!--
<xsl:template match="xlink">
	<xsl:text>\ref{</xsl:text>
	<xsl:value-of select="@linkend" />
	<xsl:text>}</xsl:text>
</xsl:template>
-->
<!-- The default is to render all notes in a DBKadmonition.
We throw them into an 'important' because it was already styled. -->
<xsl:template match="note|important|warning|caution|tip">
  <xsl:text>\begin{important}</xsl:text>
  <xsl:choose>
      <xsl:when test="title">
		  <xsl:text>\textbf{</xsl:text>
		  <xsl:call-template name="normalize-scape">
			  <xsl:with-param name="string" select="title"/>
		  </xsl:call-template>
		  <xsl:text>} </xsl:text>
      </xsl:when>
      <xsl:otherwise>
		  <xsl:call-template name="gentext.element.name"/>
      </xsl:otherwise>
  </xsl:choose>

  <xsl:apply-templates/>
  <xsl:text>\end{important}&#10;</xsl:text>
</xsl:template>
<!-- Drop the glossary text that we can't display right now -->
<xsl:template match="note[@role='margin_term']">
	<xsl:value-of select="title" />
</xsl:template>

<xsl:template match="glosslist" />


<!--
Figure captions and titles: DocBook uses both. Sometimes the author
will use one or the other or even both. The stylesheets output a
caption as an "\slshape" and the title as the \caption{} element. This
leads to empty \caption{} elements, which render as "Figure 1.1:" with
a trailing colon, which is not pretty. I think the difference is
supposed to be that the caption is longer than the title, but I'm not sure.
It is when processing the title that the stylesheet outputs the \label
info, via calling labels.id.
A cleanup action is to remove empty \caption{} nodes and replace
'{\slshape' with '\caption{'
-->
<!--
<xsl:template match="figure/title">
	<xsl:apply-templates select="caption"/>
</xsl:template>
<xsl:template match="figure/caption">
	<xsl:text>\caption{</xsl:text>
	<xsl:value-of select="." />
	<xsl:text>}</xsl:text>
</xsl:template>
-->

<!--
 We have to override mediaobject to be able to process videoobject
children?
 -->

<xsl:template match="mediaobject2|inlinemediaobject">
  <xsl:variable name="figcount"
                select="count(ancestor::figure/mediaobject[imageobject])"/>
  <!--
  within a figure don't put each mediaobject into a separate paragraph,
  to let the subfigures correctly displayed.
  -->
  <xsl:if test="self::mediaobject and not(parent::figure)">
    <xsl:text>&#10;</xsl:text>
    <xsl:text>\begin{minipage}[c]{\linewidth}&#10;</xsl:text>
    <xsl:text>\begin{center}&#10;</xsl:text>
  </xsl:if>
  <xsl:choose>
<!-- NTI Additions -->
<!--
Order matters; by putting this ahead of the next test,
we are unconditionally choosing video objects over other types;
apparently a mediaobject is meant to be a choice of alternatives,
and dblatex chooses one based on the 'role' attribute (or the first).
 -->
    <xsl:when test="videoobject">
		<xsl:apply-templates select="videoobject" />
    </xsl:when>
<!-- End NTI Additions -->
    <xsl:when test="imageobject|imageobjectco">
      <xsl:variable name="idx">
        <xsl:call-template name="mediaobject.select.idx"/>
      </xsl:variable>
      <xsl:variable name="img"
                    select="(imageobject|imageobjectco)[position()=$idx]"/>

      <xsl:if test="$imagedata.file.check='1'">
        <xsl:text>\imgexists{</xsl:text>
        <xsl:apply-templates
            select="$img/descendant::imagedata"
            mode="filename.get"/>
        <xsl:text>}{</xsl:text>
      </xsl:if>
      <xsl:apply-templates select="$img"/>
      <xsl:if test="$imagedata.file.check='1'">
        <xsl:text>}{</xsl:text>
        <xsl:apply-templates select="textobject[1]"/>
        <xsl:text>}</xsl:text>
      </xsl:if>
    </xsl:when>

    <xsl:otherwise>
      <xsl:apply-templates select="textobject[1]"/>
    </xsl:otherwise>
  </xsl:choose>
  <!-- print the caption if not in a float, or is single -->
  <xsl:if test="caption and ($figcount &lt;= 1)">
    <xsl:text>\begin{center}&#10;</xsl:text>
    <xsl:apply-templates select="caption"/>
    <xsl:text>\end{center}&#10;</xsl:text>
  </xsl:if>
  <xsl:if test="self::mediaobject and not(parent::figure)">
    <xsl:text>\end{center}&#10;</xsl:text>
    <xsl:text>\end{minipage}&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template match="videoobject">
  <xsl:apply-templates select="videodata"/>
</xsl:template>

<!-- Based on the imagedata tag -->
<xsl:template match="videodata">
  <xsl:variable name="graphic.begin">
    <xsl:call-template name="graphic.begin.get"/>
  </xsl:variable>
  <xsl:variable name="graphic.end">
    <xsl:call-template name="graphic.end.get"/>
  </xsl:variable>
  <xsl:variable name="piangle">
    <xsl:call-template name="pi-attribute">
      <xsl:with-param name="pis" select="../processing-instruction('dblatex')"/>
      <xsl:with-param name="attribute" select="'angle'"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="filename">
	  <!--
		   The source and fileref are different and not equivalent in
		   this content. The source points to the youtube page for
		   the video; we have code to change that into the embedded
		   link. The fileref uses a CK12 API key; not sure what it
		   actually does.
	  -->
	  <!--
	  <xsl:apply-templates select="." mode="filename.get"/>
	  -->

	  <xsl:value-of select="@source" />

  </xsl:variable>

  <xsl:text>\ntiincludevideo{</xsl:text>
  <xsl:value-of select="$filename"/>
  <xsl:text>}</xsl:text>
</xsl:template>

</xsl:stylesheet>
