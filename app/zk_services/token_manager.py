from django.db.models import Manager


class TokenManager(Manager):

    def get_or_none(self, pk=None):
        from zk_services.models import ZkToken
        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except self.model.DoesNotExist:
                return None
        else:
            try:
                return ZkToken.objects.order_by('-id').first()
            except self.model.DoesNotExist:
                return None
