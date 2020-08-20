from rest_framework import serializers

from enquiry.models import Enquiry


class ListEnquirySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Enquiry
        fields =    [
                    'id',
                    'user', 
                    'question', 
                    'created', 
                    'updated', 
                    'answered']

    def get_user(self, obj):
        context = self.context['request']
        return context.user.username


class CreateEnquirySerializer(ListEnquirySerializer):

    def create(self, validated_data):
        context = self.context['request']

        enq_obj = Enquiry(
            user=context.user,
            question=validated_data.get("question")
        )
        enq_obj.save()

        return enq_obj