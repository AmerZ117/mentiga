from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from KPI.models import Employee, EmployeeProfile, Department
from datetime import date

class Command(BaseCommand):
    help = 'Create user accounts for employees who do not have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=str,
            help='Create account for specific employee ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Create accounts for all employees without user accounts'
        )
        parser.add_argument(
            '--department',
            type=str,
            help='Create accounts for employees in specific department'
        )
        parser.add_argument(
            '--password-length',
            type=int,
            default=12,
            help='Length of generated passwords (default: 12)'
        )

    def handle(self, *args, **options):
        if options['employee_id']:
            # Create account for specific employee
            self.create_account_for_employee(options['employee_id'], options['password_length'])
        elif options['all']:
            # Create accounts for all employees without user accounts
            self.create_accounts_for_all(options['password_length'])
        elif options['department']:
            # Create accounts for employees in specific department
            self.create_accounts_for_department(options['department'], options['password_length'])
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Please specify --employee-id, --all, or --department'
                )
            )

    def create_account_for_employee(self, employee_id, password_length):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if employee.user:
                self.stdout.write(
                    self.style.WARNING(
                        f'Employee {employee.full_name} already has a user account'
                    )
                )
                return
            
            # Create user account
            username = employee.employee_id.lower()
            password = get_random_string(password_length)
            
            user = User.objects.create_user(
                username=username,
                email=employee.email,
                password=password,
                first_name=employee.first_name,
                last_name=employee.last_name
            )
            
            # Link user to employee
            employee.user = user
            employee.save()
            
            # Create employee profile
            EmployeeProfile.objects.get_or_create(employee=employee)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'User account created for {employee.full_name}:\n'
                    f'Username: {username}\n'
                    f'Password: {password}\n'
                    f'Login URL: /employee/login/'
                )
            )
            
        except Employee.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Employee with ID {employee_id} not found')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating account: {str(e)}')
            )

    def create_accounts_for_all(self, password_length):
        employees_without_accounts = Employee.objects.filter(user__isnull=True)
        
        if not employees_without_accounts.exists():
            self.stdout.write(
                self.style.SUCCESS('All employees already have user accounts')
            )
            return
        
        self.stdout.write(f'Creating accounts for {employees_without_accounts.count()} employees...')
        
        created_count = 0
        for employee in employees_without_accounts:
            try:
                # Create user account
                username = employee.employee_id.lower()
                password = get_random_string(password_length)
                
                user = User.objects.create_user(
                    username=username,
                    email=employee.email,
                    password=password,
                    first_name=employee.first_name,
                    last_name=employee.last_name
                )
                
                # Link user to employee
                employee.user = user
                employee.save()
                
                # Create employee profile
                EmployeeProfile.objects.get_or_create(employee=employee)
                
                created_count += 1
                
                self.stdout.write(
                    f'✓ {employee.full_name}: {username} / {password}'
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ {employee.full_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} user accounts!'
            )
        )

    def create_accounts_for_department(self, department_name, password_length):
        try:
            department = Department.objects.get(name__iexact=department_name)
            employees_without_accounts = Employee.objects.filter(
                department=department,
                user__isnull=True
            )
            
            if not employees_without_accounts.exists():
                self.stdout.write(
                    self.style.SUCCESS(
                        f'All employees in {department.name} already have user accounts'
                    )
                )
                return
            
            self.stdout.write(
                f'Creating accounts for {employees_without_accounts.count()} employees in {department.name}...'
            )
            
            created_count = 0
            for employee in employees_without_accounts:
                try:
                    # Create user account
                    username = employee.employee_id.lower()
                    password = get_random_string(password_length)
                    
                    user = User.objects.create_user(
                        username=username,
                        email=employee.email,
                        password=password,
                        first_name=employee.first_name,
                        last_name=employee.last_name
                    )
                    
                    # Link user to employee
                    employee.user = user
                    employee.save()
                    
                    # Create employee profile
                    EmployeeProfile.objects.get_or_create(employee=employee)
                    
                    created_count += 1
                    
                    self.stdout.write(
                        f'✓ {employee.full_name}: {username} / {password}'
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {employee.full_name}: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully created {created_count} user accounts in {department.name}!'
                )
            )
            
        except Department.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Department "{department_name}" not found')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )

