from django.db import models



# Registration model
class UserModel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert email to lowercase
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class FriendRequestModel(models.Model):
    sender = models.ForeignKey(UserModel, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserModel, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    
