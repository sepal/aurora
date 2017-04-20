from django.db import models


class ReviewAnswer(models.Model):
    review = models.ForeignKey('Review.Review', on_delete=models.CASCADE)
    review_question = models.ForeignKey('ReviewQuestion.ReviewQuestion', on_delete=models.CASCADE)
    text = models.TextField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
