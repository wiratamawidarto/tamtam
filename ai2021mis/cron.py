from django.core.management import call_command

def backup_function():
    print('heyyyy')
    call_command('dbbackup') #is like calling manage.py 
