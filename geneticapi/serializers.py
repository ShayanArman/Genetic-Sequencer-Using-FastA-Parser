from rest_framework import serializers

# ------ INPUT Serializer ----
class RefQuerySerializer(serializers.Serializer):
	chromosome = serializers.CharField(max_length=2, min_length=1)
	start = serializers.IntegerField(max_value=None, min_value=None)
	stop = serializers.IntegerField(max_value=None, min_value=None)

# ----- OUTPUT Result Serializer ----
class RefGenomeSerializer(serializers.Serializer):
	genetic_sequence = serializers.CharField(min_length=None, max_length=None)
