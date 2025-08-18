"""
Authentication and environment validation utilities
"""

import os
from dotenv import load_dotenv

def check_environment_variables():
    """
    Check if all required environment variables are set
    
    Returns:
        dict: Status of environment variables
    """
    load_dotenv()
    
    required_vars = {
        'ALPHA_VANTAGE_API_KEY': os.getenv('ALPHA_VANTAGE_API_KEY'),
        'supabaseURL': os.getenv('supabaseURL'),
        'supabaseKey': os.getenv('supabaseKey'),
        'supabaseServiceKey': os.getenv('supabaseServiceKey'),
        'SUPABASE_DB_URL': os.getenv('SUPABASE_DB_URL')
    }
    
    missing = {}
    all_set = True
    
    for var, value in required_vars.items():
        is_set = value is not None and value != "" and not value.startswith("your_")
        missing[var] = is_set
        if not is_set:
            all_set = False
    
    return {
        'all_set': all_set,
        'missing': missing,
        'vars': required_vars
    }

