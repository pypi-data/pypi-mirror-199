from PyInquirer import prompt

from lemay_hire_me.utils.const import style
from lemay_hire_me.validators.email import EmailValidator
from lemay_hire_me.validators.empty import EmptyValidator
from lemay_hire_me.validators.weblinks import LinkedInValidator


def ask_personal_info():
    questions = [
        {
            'type': 'input',
            'name': 'author',
            'message': 'Enter your full name',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'linkedin_url',
            'message': 'Enter your LinkedIn profile URL',
            'validate': LinkedInValidator
        },
        {
            'type': 'input',
            'name': 'email',
            'message': 'Enter your email address',
            'validate': EmailValidator
        },
        {
            'type': 'input',
            'name': 'salary_expectation',
            'message': 'Enter your desired salary range (in CAD)',
            'validate': EmptyValidator
        },
        {
            'type': 'confirm',
            'name': 'send',
            'message': 'Would you like to save the data and start the task?'
        }
    ]

    answers = prompt(questions, style=style)
    return answers
