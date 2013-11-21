from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from application.models import Story

from xml.dom.minidom import parse, parseString

register = template.Library()

def fractal(value, autoescape=True):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	def _makeEmpty(elementid):
		return "<div id='%s' class='fractal_empty'></div>" %esc(elementid)

	def _makeRootText(value, elementid):
		return _makeTextHelper(value, "fractal_root", elementid)

	def _makeText(value, elementid):
		return _makeTextHelper(value, "", elementid)

	def _makeTextHelper(value, rootElement, elementid):
		if value.firstChild is not None:
			return "<div id='%s' class='fractal_element %s'>%s</div>" % (esc(elementid), esc(rootElement), esc(value.firstChild.data))
		else:
			return "<div id='%s' class='fractal_missing %s'></div>" % (esc(elementid), esc(rootElement))

	def _helper(value, elementid):
		output = ""
		output += "<div class='fractal_indent'>"
		if value.childNodes.length == 3:
			output += _helper(value.childNodes[0], elementid+"1")
			output += _makeText(value.childNodes[1], elementid)
			output += _helper(value.childNodes[2], elementid+"2")
		elif value.childNodes.length == 2:
			if value.childNodes[0].tagName == "fractal" and value.childNodes[1].tagName == "text":
				output += _helper(value.childNodes[0], elementid+"1")
				output += _makeText(value.childNodes[1], elementid)
				output += _makeEmpty(elementid+"2")
			elif value.childNodes[0].tagName == "text" and value.childNodes[1].tagName == "fractal":
				output += _makeEmpty(elementid+"1")
				output += _makeText(value.childNodes[0], elementid)
				output += _helper(value.childNodes[1], elementid+"2")
		elif value.childNodes.length == 1:				
				output += _makeEmpty(elementid+"1")
				output += _makeText(value.childNodes[0], elementid)
				output += _makeEmpty(elementid+"2")
			
		output += "</div>"
		return output
 
	def _helperStart(value):
		output = ""
		if value.childNodes.length == 3:
			output += _makeRootText(value.childNodes[0],"Start")
			output += _helper(value.childNodes[1],"0")
			output += _makeRootText(value.childNodes[2], "End")
		elif value.childNodes.length == 2:
			output += _makeRootText(value.childNodes[0], "Start")
			output += _makeEmpty("0")
			output += _makeRootText(value.childNodes[1], "End")
		return output


	return mark_safe(_helperStart(parseString(value).documentElement))

def process(value, autoescape=True):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x

	def _processHelper(value, depth):
		output = ""
		for node in value.childNodes:
			if node.tagName == "text":
				if node.firstChild is not None:
					data = str(node.firstChild.data)
					length = len(data)
					output += "[" +str(depth) +"," +str(length) +"] "
			elif node.tagName == "fractal": 
				output += _processHelper(node, depth+1)
		return output

	return mark_safe(_processHelper(parseString(value).documentElement, 0))

fractal.needs_autoescape = True
register.filter('fractal', fractal)


process.needs_autoescape = True
register.filter('process', process)

