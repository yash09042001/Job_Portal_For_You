from rest_framework import serializers
from .models import Job


class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'qualifications',
                  'deadlines', 'status']

    def to_representation(self, instance):
        """
        Customize the serialized representation based on the view/action.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request', None)

        if request and request.resolver_match:
            # Get the view name from the resolver
            view_name = request.resolver_match.view_name

            # Exclude 'description' for the 'joblist' view  user iscandidate
            if view_name == 'JobDetailCandidateAPIView' and request.user.is_candidate:
                representation.pop('description', None)

        return representation


class JobPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['deadlines', 'status']
