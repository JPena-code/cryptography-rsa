
def is_prime(n):
	"""
		Primality test for number n using the trail divison
	"""
	d = 2
	while d * d <= n:
		if x % d == 0:
			return True
	return False

if __name__ == '__main__':
	pass