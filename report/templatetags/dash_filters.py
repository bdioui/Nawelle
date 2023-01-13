from django import template

register = template.Library()

@register.filter(name='divide')
def divide(value, arg):
	try:
		if int(arg)!=0: 
			return round(((float(value) / float(arg))* 100))
		else: 
			return 0

	except (ValueError, ZeroDivisionError):
		return None

@register.filter(name='substract')
def substract(value, arg):
	try:
		if int(arg)!=0: 
			return round(float(value) - float(arg))
		else: 
			return 0

	except (ValueError, ZeroDivisionError):
		return None

@register.filter(name='add')
def add(value, *args):
	try:
		if int(args)!=0:
			sum = float(value)
			for elem in args : 
				sum += float(elem)
			return round(sum)
		else: 
			return 0

	except (ValueError, ZeroDivisionError):
		return None

@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, basestring):
        return text.startswith(starts)
    return False

@register.filter('month')
def mont(value):
	if value==1:
		return 'janvier'
	if value==2:
		return 'fevrier'
	if value==3:
		return 'mars'
	if value==4:
		return 'avril'
	if value==5:
		return 'mai'
	if value==6:
		return 'juin'
	if value==7:
		return 'juillet'
	if value==8:
		return 'août'
	if value==9:
		return 'septembre'
	if value==10:
		return 'octobre'
	if value==11:
		return 'novembre'
	if value==12:
		return 'decembre'
	else :
		return value