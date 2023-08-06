# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aigremlins']
install_requires = \
['openai>=0.27.2,<0.28.0']

setup_kwargs = {
    'name': 'aigremlins',
    'version': '1.0',
    'description': 'Using GPT 3 to backstop buggy code',
    'long_description': '# AIGremlins\n\nAI Gremlin - Automatic Error Correction with OpenAI\nAI Gremlin is a Python module that leverages OpenAI\'s GPT-3 to automatically fix errors in your Python code. The module contains two main classes, GremlinTest and AIgremlin, which work together to handle exceptions and get suggestions for fixes from OpenAI\'s API.\n\nNote:\nUsing this code in real applications is a terrible idea for many reasons, including:\n- Creating the machine revolution by given an AI direct possibility to execute functions without anyone chekcing.\n- There\'s no garantuee that the AI generated function won\'t break anything else or delete something import.\n- Many other reasons.\n\nDon\'t even think about using this in production. That being said:\n\n### Features\nAutomatically detects and corrects errors in your Python functions using OpenAI\'s GPT-3.\nTries to stay as close as possible to the intent of the original function.\nDynamically adds and executes the new fixed function in the original namespace.\nCustomizable parameters to control the number of iterations, token limit, temperature settings, and verbosity of the output.\nAbility to add custom instructions for OpenAI\'s API.\n\n### How It Works\nThe AIgremlin class wraps your target function with a decorator called ai_backstop.\nWhen the target function encounters an exception, the ai_backstop decorator captures the error, function code, and parameters.\nThe ai_backstop decorator formats a prompt for OpenAI\'s API to get a suggestion for fixing the function.\nThe suggestion is received from OpenAI\'s API, and a new fixed function is generated.\nThe fixed function is added to the original namespace and executed.\nThe process continues until the fixed function executes without errors or the maximum number of iterations is reached.\n\n### Usage\n1. Import the AIgremlin class from the module.\n2. Instantiate an AIgremlin object with your OpenAI API key and other optional parameters (e.g., max_iterations, max_tokens, temperature, temperature_escalation, verbose, and instructions).\n3. Define your function and apply the ai_backstop decorator to it.\n\nCall the decorated function as you normally would. If an exception is encountered, the AI Gremlin will automatically attempt to fix it using OpenAI\'s API.\n```\nfrom AIgremlins import AIgremlin\n\n# Initialize AI Gremlin instance with your OpenAI API key\nai_gremlin = AIgremlin(api_key="your_openai_api_key", verbose=True)\n\n# Define the function with an error\n@ai_gremlin.ai_backstop\ndef buggy_function(a, b):\n    return a / b\n\n# Call the function with parameters that cause an exception\nresult = buggy_function(4, 0)\n```\n\n### Options\n1. temperature -> default temperature of the model used.\n2. temperature escalation -> the model can become increasingly creative. Should be somewhere between the range of 0.1-0.4 as the max temperature is 1.\n3. instructions -> you can give additional instructions to the AI to take into consideration.\n',
    'author': 'Ivan Thung',
    'author_email': 'ivanthung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9.10,<4.0.0',
}


setup(**setup_kwargs)
