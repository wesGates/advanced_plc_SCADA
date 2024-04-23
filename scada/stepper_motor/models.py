from django.db import models

class StepperMotorDataPoint(models.Model):
	# Tag Name
	tag_name = models.CharField(max_length=256)
	# Tag Value/ Status
	tag_value = models.IntegerField()
	# Timestamp
	timestamp = models.DateTimeField()


    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
