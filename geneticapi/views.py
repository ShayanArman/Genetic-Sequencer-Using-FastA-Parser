# Django Response
from django.http import HttpResponse
from rest_framework import status

import json

# FastA Parser
from pyfasta import Fasta

# Serializers
from .serializers import RefQuerySerializer, RefGenomeSerializer

# From JSON to Python Data Format
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

# From Serializer to JSON
from rest_framework.renderers import JSONRenderer

f = Fasta('geneticapi/templates/data/genbank.GRCh37.fa')
FASTA_INDEX = sorted(f.keys(), reverse=True)

class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class ChromeParseException(Error):
	"""Exception raised for errors in the input.

	Attributes:
		msg  -- explanation of the error
	"""

	def __init__(self, msg, status):
		self.ERROR_RESPONSE = json.dumps({
										'message': msg, 
										'status': status,
										})

def get_genetic_info(request):
	if request.body:
		# Parse the body into a python object
		stream = BytesIO(request.body)
		data = JSONParser().parse(stream)
	else:
		exc = ChromeParseException('Improper input format', status.HTTP_400_BAD_REQUEST)
		return HttpResponse(exc.ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

	# GET: one chromosome query
	if request.method == 'GET':
		serializer = RefQuerySerializer(data=data)

		if serializer.is_valid():
			try:
				base_pair_string = genetic_code(serializer.data)
				result = RefGenomeSerializer(data={'genetic_sequence': base_pair_string})
				if result.is_valid():
					return HttpResponse(json.dumps(result.data), status=status.HTTP_200_OK)
				else:
					return HttpResponse(result.errors(), status=status.HTTP_400_BAD_REQUEST)
			except ChromeParseException as exception:
				return HttpResponse(exception.ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

	# POST: many queries in the data object
	elif request.method == 'POST':
		serializer = RefQuerySerializer(data=data, many=True)

		if serializer.is_valid():
			try:
				result_list = []
				for query in serializer.data:
					base_pair_string = genetic_code(query)
					result_list.append({'genetic_sequence': base_pair_string})

				result = RefGenomeSerializer(data=result_list, many=True)
				if result.is_valid():
					return HttpResponse(json.dumps(result.data), status=status.HTTP_200_OK)
				else:
					return HttpResponse(result.errors(), status=status.HTTP_400_BAD_REQUEST)
			except ChromeParseException as exception:
				return HttpResponse(exception.ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
		
	exc = ChromeParseException('Improper input format', status.HTTP_400_BAD_REQUEST)
	return HttpResponse(exc.ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

def genetic_code(query_dict):
	chromosome = query_dict['chromosome']
	start = int(query_dict['start'])
	stop = int(query_dict['stop'])

	if chromosome == 'X':
		chromosome = 22
	if chromosome == 'Y':
		chromosome = 23
	else:
		try:
			chromosome = int(chromosome)
			if chromosome < 1 or chromosome > 22:
				raise ChromeParseException('Options for chromosome: [1-22] or X,Y', status.HTTP_400_BAD_REQUEST)
		except ValueError:
			raise ChromeParseException('Options for chromosome: [1-22] or X,Y', status.HTTP_400_BAD_REQUEST)
		# Fast A_INDEX is 0 based
		chromosome = int(chromosome) - 1

	chromosome_range = len(f[FASTA_INDEX[chromosome]])

	if start > 0 and stop > 0 and stop < chromosome_range and stop >= start and abs(stop-start) <= 500:
		# Subtract 1 from the start: FastA is 0 indexed
		# stop + 1 - 1 (add one to be inclusive, subtract one to be zero indexed) 
		return f[FASTA_INDEX[chromosome]][int(start)-1:int(stop)]
	else:
		message = ""
		if start <= 0 or stop <= 0:
			message += "Start and stop must be greater than 0. "
		if stop > chromosome_range:
			message += "Stop index was greater than the number of base pairs in chromosome " + query_dict['chromosome'] + " "
		if stop - start > 500:
			message += "Max range length is 500 base pairs. "
		if stop < start:
			message += "Stop must be greater than or equal start."
		raise ChromeParseException(message.strip(), status.HTTP_400_BAD_REQUEST)
