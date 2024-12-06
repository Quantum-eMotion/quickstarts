import pandas as pd
import numpy as np
import seaborn as sns
import os
import requests
from dotenv import load_dotenv
load_dotenv()

#### Define Variables

sns.set_style('whitegrid')
avg = 1
std_dev = .1
num_reps = 500
num_simulations = 1000
token = os.environ.get("ACCESS_TOKEN")
size = os.environ.get("SIZE")
url = f'https://api-qxeaas.quantumemotion.com/entropy'
headers = { 'Authorization': f'Bearer {token}' }
querystring = { 'size': size }

#### Define Function to generate random numbers

def qrng_normal(loc=0.0, scale=1.0, size=1):
	"""
	Generate random numbers following a normal distribution using the QRNG API.

	Parameters:
	loc (float): Mean of the normal distribution.
	scale (float): Standard deviation of the normal distribution.
	size (int or tuple of ints): Output shape.

	Returns:
	numpy.ndarray: Array of random numbers following a normal distribution.
	"""
	response = requests.get(url, headers=headers, params=querystring)
	random_num = int(''.join(filter(str.isdigit, response.json()['random_number']))) % 10**size
	random_ints = [int(num) for num in str(random_num)]  # Convert string integers to actual integers

	# Transform the random integers to follow a normal distribution
	random_numbers = np.sqrt(-2 * np.log(random_ints / 65535)) * np.cos(2 * np.pi * random_ints / 65535)
	random_numbers = (random_numbers - np.mean(random_numbers)) / np.std(random_numbers)

	return loc + scale * random_numbers.reshape(size)

#### Define Function to generate random numbers from given list

def qrng_choice(choices, p=None, size=1):
	"""
	Generate a random choice from the given list of choices.

	Parameters:
	choices (list): The list of choices to select from.
	p (list, optional): The probabilities associated with each choice. If not provided, all choices are equally likely.
	size (int, optional): The number of choices to generate. Default is 1.

	Returns:
	list: A list of the selected choices.
	"""
	# Get the required number of random integers from the QRNG API
	response = requests.get(url, headers=headers, params=querystring)
	random_num = int(''.join(filter(str.isdigit, response.json()['random_number']))) % 10**size
	random_ints = [int(num) for num in str(random_num)]  # Convert string integers to actual integers

	# Map the random integers to the indices of the choices list
	if p is None:
		p = [1/len(choices)] * len(choices)

	chosen_indices = [i % len(choices) for i in random_ints]
	chosen_values = [choices[i] for i in chosen_indices]

	return chosen_values

#### Generate Data frame
pct_to_target = qrng_normal(avg, std_dev, num_reps)
sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
sales_target_prob = [.3, .3, .2, .1, .05, .05]
sales_target = qrng_choice(sales_target_values, num_reps, p=sales_target_prob)
df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
												   'Sales_Target': sales_target})

df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']

#### Define Function to return commission rate

def calc_commission_rate(x):
	""" Return the commission rate based on the table:
	0-90% = 2%
	91-99% = 3%
	>= 100 = 4%
	"""
	if x <= .90:
		return .02
	if x <= .99:
		return .03
	else:
		return .04
df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']
# Define a list to keep all the results from each simulation that we want to analyze
all_stats = []

####  Loop through many simulations

for i in range(num_simulations):

	# Choose random inputs for the sales targets and percent to target
	sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)
	pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)

	# Build the dataframe based on the inputs and number of reps
	df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
												   'Sales_Target': sales_target})

	# Back into the sales number using the percent to target rate
	df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']

	# Determine the commissions rate and calculate it
	df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
	df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']

	# We want to track sales,commission amounts and sales targets over all the simulations
	all_stats.append([df['Sales'].sum().round(0),
					  df['Commission_Amount'].sum().round(0),
					  df['Sales_Target'].sum().round(0)])


####  Display Result

results_df = pd.DataFrame.from_records(all_stats, columns=['Sales',
														   'Commission_Amount',
														   'Sales_Target'])
results_df.describe().style.format('{:,}')