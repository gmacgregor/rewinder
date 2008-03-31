from django.db import models



class StreamObject(models.Model):
	#id
	#type_id				
 	created_on			= models.DateTimeField(auto_now_add=True)
	last_modified		= models.DateTimeField(auto_now=True)