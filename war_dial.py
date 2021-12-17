import requests
import ipaddress

# FIXME 0:
# Copy/paste the implementation of the `is_server_at_ip` function
# from the lab instructions below.

def is_server_at_ip(ip):
    '''
    returns `True` if a server exists at the input IP address;
    otherwise returns `False`
    '''
    try:
        r = requests.get('http://'+str(ip), headers={'host': 'this can be anything :)'})
        print('trying')
        return True
    except requests.exceptions.ConnectTimeout:
        return False

# FIXME 1:
# Create a list of all the IP addresses assigned to the DPRK.
# Recall that the DPRK is assigned all IP addresses in the range from `175.45.176.0` to `175.45.179.255` (1024 IPs in total).
# These IP addresses should be represented as python strings.
# It is possible to do this using either a 1-line list comprehension or a multi-line for loop.

ip_accumulator = []

for i in range(176, 180):
    for j in range (0,256):
        new_ip = '175.45.' + str(i) + '.' + str(j)
        ip_accumulator.append(new_ip)

# print(ip_accumulator)

# FIXME 2:
# Create a list of all IP addresses in dprk_ips that have a server at them.
# Print this list of IPs to the screen.


dprk_ips = []

for i in ip_accumulator:
    if is_server_at_ip(i):
        dprk_ips.append(i)

print(dprk_ips)
'''
    if is_server_at_ip(ip) == True:
        ip_server_accumulator.append(ip)
'''



# HINT:
# There are 1024 IPs that you must scan,
# and you're waiting up to 5 seconds for each.
# That means you're code will take up to 1024*5/60 = 85 minutes to run.
# If you haven't watched the WarGames movie yet,
# I recommend watching it while you're code is running :)
# In "real" war dialing code,
# all of these connections are done in parallel,
# and so the scan of all 1024 IPs can be completed in just seconds.
# An ordinary laptop and internet connection can scan the entire internet (4.2 billion IPs) in under an hour.
# Parallel programming is quite hard, however,
# so we're just doing the slow and sequential version in this lab.

# HINT:
# Depending on your computer's configurations,
# there are many other exceptions that might possibly be thrown besides `ConnectTimeout`,
# and you'll have to get creative about debugging these problems.
# For example, I would occasionaly get a `TooManyRedirects` exception,
# and there's instructions at this stackoverflow link for solving the error:
# https://stackoverflow.com/questions/42237672/python-toomanyredirects-exceeded-30-redirects
# I would also sometimes get a `ConnectionError` exception,
# and retrying the connection fixed the problem.
#
# You do not need to run your war dial of all 1024 IP addresses in a single run of your python code.
# If you have an error message on the 500th IP, for example,
# you can restart your code from that IP to finish the scan.
# In your final submission to sakai, you'll have to concatenate the found IPs from both runs together when uploading the list of IPs.

