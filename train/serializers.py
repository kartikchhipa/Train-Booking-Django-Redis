from rest_framework import serializers

from .models import Train

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ["id","train_name", "source", "destination", "train_capacity"]

    def validate(self, attrs):
        source = attrs.get("source", "")
        destination = attrs.get("destination", "")
        if source == destination:
            raise serializers.ValidationError("Source and destination must be different")
        return attrs

    def create(self, validated_data):
        train = Train.objects.create(
            train_name=validated_data["train_name"],
            source=validated_data["source"],
            destination=validated_data["destination"],
            train_capacity=validated_data["train_capacity"],
        )
        return train

