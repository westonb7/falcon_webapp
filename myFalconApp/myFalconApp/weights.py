import json
import falcon
from collections import defaultdict

## Define the S function described in the document:

def s_function(x, a, b):
	c = (a+b)/2.0
	if x <= a:
		return 0
	if x > a and x <= c:
		return (2.0 * ((x-a)/(b-a))**2) 
	if x > c and x <= b:
		return (1.0 - 2.0*(((x-b)/(b-a))**2))
	if x > b:
		return 1

## Define a function to calculate score, can be used for either reach or clarity

def find_score(score_list):
	avg = 0
	total = len(score_list)
	if total <= 0:
		return 0
	for val in score_list:
		avg += val
	return (avg/total)	

## Define a function to calculate confidence, can be used for reach or clarity,
##  but must be specified by passing in a 0 for reach or 1 for clarity,
##  since the a and b values differ for each

def find_confidence(conf_list, type):
	total = len(conf_list)
	if type == "reach":	## In case someone attempts to use this function with 'reach'/'clarity' as type
		type = 0
	elif type == "clarity":
		type = 1
	if total > 0 and type == 0:
		return s_function(total, 2.0, 6.0)	## Using floats to prevent python from coercing values into ints
	elif total > 0 and type == 1:
		return s_function(total, 4.0, 8.0)
	else:
		return 0

## Define function to calculate clout score

def find_clout_score(reach_s, reach_c, clarity_s, clarity_c):
	clout_s = 0.0		## Using a float to prevent integer coecion problems
	clout_s = ((reach_s*reach_c) + (clarity_s*clarity_c) / 2.0) / 10.0
	return clout_s

## This really isn't necessary, but I might as well have a function for 
##  this, so if the formula for clout confidence changes, the change 
##  can be implemented easily. 

def find_clout_confidence(reach_c, clarity_c):
	return min(reach_c, clarity_c)

## Declare dictionaries

reputee_scores = {} #defaultdict(list)
reputee_rids = {}
reputee_calculated = {}

## Define function to calculate scores and confidences for reach, clarity, and clout

def calculate_scores(reputee_scores, reputee):
	if "Reach" in reputee_scores[reputee]:
		reach_s = find_score(reputee_scores[reputee]["Reach"])
		reach_c = find_confidence(reputee_scores[reputee]["Reach"], 0) 
	else:
		reach_s = 0  ## Set these values to zero so that things don't break if there's no reach data
		reach_c = 0
	if "Clarity" in reputee_scores[reputee]:
		clarity_s = find_score(reputee_scores[reputee]["Clarity"])
		clarity_c = find_confidence(reputee_scores[reputee]["Clarity"], 1)
	else:
		clarity_s = 0 
		clarity_c = 0
	clout_s = find_clout_score(reach_s, reach_c, clarity_s, clarity_c)
	clout_c = find_clout_confidence(reach_c, clarity_c)
	return_obj = {
		'reputee':reputee,
		'clout':{ 'score':clout_s, 'confidence':clout_c },
		'reach':{ 'score':reach_s, 'confidence':reach_c },
		'clarity':{ 'score':clarity_s, 'confidence':clarity_c }
	}
	return return_obj

class Resource(object):
	## Sample GET request: 
	## http localhost:8000/weights?name=foo

	def on_get(self, req, resp):
		#print (req.get_param('name'))

		my_val = req.get_param('name')
		#print(my_val)

		#print(reputee_calculated)
		#print(reputee_calculated[my_val])
		weights_return = reputee_calculated[my_val]
		#print(weights_return)

		resp.body = json.dumps(weights_return, ensure_ascii=False)
		resp.status = falcon.HTTP_200


	def on_post(self, req, resp):	

	## Sample POST request:
	## http --json POST localhost:8000/weights test:='{"reputer":"name", "reputee":"foo", "repute":{"rid":"xyz12345", "feature":"Clarity", "value":"5"}}'

		stream_data = req.stream.read()
		stream_data = json.loads(stream_data)

		#print(stream_data['test'])

		reputee = stream_data['test']['reputee']

		rid = stream_data['test']['repute']['rid']
		feature = stream_data['test']['repute']['feature']
		value = int(stream_data['test']['repute']['value'])

		## Here I'm unlcear on how exaclty non-unique rids are supposed to be handled.
		## I'm making the assumption that if an rid has ever been used, future POST requests
		##  with that rid should be completely disregarded.
		## However, if rids can be re-used across different reputees, or for the same
		##  reputee for both clarity and reach, then I would need to rewrite part of this
		##  to account for allowing non-uniqe rids to be resued in certain contexts.
		
		if rid not in reputee_rids:
			if reputee in reputee_scores:
				if feature in reputee_scores[reputee]:
					reputee_scores[reputee][feature].append(value)
				elif feature == "Reach" or feature == "Clarity":
					reputee_scores[reputee][feature] = [value]
			else:
				reputee_d = {feature : [value]}
				reputee_scores[reputee] = reputee_d
			reputee_rids[rid] = reputee    ## Save rids in a dict with their reputee in case I need to change this
		
		## I calculate the scores and confidences here, for the sake of 
		##  time, when GET request are recieved. This is less computationally
		##  efficient and less memory efficient than only claculating scores
		##  when a GET is recieved, and if speed is low-priority, this should be 
		##  changed to only calculate values on GET request.

		reputee_calculated[reputee] = calculate_scores(reputee_scores, reputee)
		#print(reputee_calculated)

		doc_jsn = {"message":"POST recieved"}

		resp.body = json.dumps(doc_jsn, ensure_ascii=False)
		resp.status = falcon.HTTP_201

