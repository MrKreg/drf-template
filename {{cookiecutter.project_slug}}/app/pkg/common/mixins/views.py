from rest_framework.response import Response


class ActionMixin:

    def detail_action(self, request, *args, **kwargs):
        instance = self.get_object()
        sz = self.get_serializer(instance=instance, data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(sz.data, **kwargs)

    def list_action(self, request, *args, **kwargs):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(sz.data, **kwargs)
