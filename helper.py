import httpx

def call_api(url: str, bearer_token: str = None, headers: dict = None, query: dict = None, query_type: str = 'GET', body: dict = None, grocy_api_key: str = None):
    """
    Call a REST API and return the JSON response as a dictionary.

    Parameters:
        url (str): The API URL.
        bearer_token (str): The Bearer token for authorization.
        headers (dict): The request headers (optional).
        query (dict): The query parameters (for GET) or data (for DELETE).
        query_type (str): The type of HTTP request (GET, POST, PUT, DELETE).
        body (dict): The request body for POST/PUT requests (optional).

    Returns:
        dict: The API response in JSON format, or None if the response is invalid.

    Raises:
        requests.exceptions.RequestException: If the API call fails.
        ValueError: If the response is not JSON.
    """
    # Add Bearer token to the headers
    if headers is None:
        headers = {}
    if bearer_token is not None:
        headers['Authorization'] = f'Bearer {bearer_token}'
    headers['accept'] = '*/*'
    headers['Content-Type'] = 'application/json'
    if grocy_api_key is not None:
        headers['GROCY-API-KEY'] = grocy_api_key
    
    try:
        # Make the API call based on query_type and handle body for POST/PUT
        if query_type.upper() == 'GET':
            response = httpx.get(url, headers=headers, params=query)
        elif query_type.upper() == 'POST':
            response = httpx.post(url, headers=headers, json=body, params=query)
        elif query_type.upper() == 'PUT':
            response = httpx.put(url, headers=headers, json=body, params=query)
        elif query_type.upper() == 'DELETE':
            response = httpx.delete(url, headers=headers, params=query)
        else:
            raise ValueError(f"Unsupported query_type: {query_type}")

        if response.status_code != 200 and response.status_code != 204:
            # Print the response status code
            print(f"Response Code: {response.status_code}")
        
        # Raise an error for bad status codes
        response.raise_for_status()
        
        if response.status_code == 204 or not response.content:
            # print("No content returned.")
            return None
        
        # Attempt to parse the response as JSON, return None if it fails
        try:
            return response.json()
        except ValueError:
            print(f"Response is not in JSON format: {response.text}")
            return None
    except httpx.RequestError as e:
        print(f"API request failed: {e}")
        return None

def string2bool(s: str) -> bool:
    # Set of accepted affirmative responses
    affirmative_responses = {'yes', 'y', 'true', '1'}
    # Return True for affirmative responses, False otherwise
    return s.strip().lower() in affirmative_responses

def input_integer(prompt="Enter an integer: ", max_value: int=None, min_value: int=None, allowed_values: list[int]=None):
    if allowed_values is not None:
        # convert for sure to int
        allowed_values = [int(item) for item in allowed_values]
    while True:
        try:
            # Get user input and convert to an integer
            user_input = int(input(prompt))

            # Check if input is within the specified range (if provided)
            if (min_value is not None and user_input < min_value) or (max_value is not None and user_input > max_value):
                print(f"Please enter a number between {min_value} and {max_value}.")
            # Check if input is in the list of allowed values (if provided)
            elif allowed_values is not None and user_input not in allowed_values:
                print(f"Please enter one of the allowed values: {allowed_values}.")
            else:
                return user_input
        except ValueError:
            # Handle case where input is not a valid integer
            print("Invalid input. Please enter a valid integer.")