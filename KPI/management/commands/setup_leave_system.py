from django.core.management.base import BaseCommand
from django.db import transaction
from KPI.models import LeaveType, LeaveApprovalLevel, Department

class Command(BaseCommand):
    help = 'Set up initial leave types and approval levels for the leave management system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up leave management system...')
        
        with transaction.atomic():
            # Create default leave types
            leave_types = [
                {
                    'name': 'Annual Leave',
                    'description': 'Regular annual vacation leave for employees',
                    'default_allocation': 21.0,
                    'requires_approval': True,
                    'color': '#28a745'
                },
                {
                    'name': 'Sick Leave',
                    'description': 'Medical leave for illness or health-related issues',
                    'default_allocation': 14.0,
                    'requires_approval': False,
                    'color': '#dc3545'
                },
                {
                    'name': 'Personal Leave',
                    'description': 'Personal time off for various personal reasons',
                    'default_allocation': 5.0,
                    'requires_approval': True,
                    'color': '#ffc107'
                },
                {
                    'name': 'Maternity Leave',
                    'description': 'Leave for expecting mothers',
                    'default_allocation': 90.0,
                    'requires_approval': True,
                    'color': '#e83e8c'
                },
                {
                    'name': 'Paternity Leave',
                    'description': 'Leave for new fathers',
                    'default_allocation': 14.0,
                    'requires_approval': True,
                    'color': '#17a2b8'
                },
                {
                    'name': 'Bereavement Leave',
                    'description': 'Leave for family bereavement',
                    'default_allocation': 5.0,
                    'requires_approval': False,
                    'color': '#6c757d'
                },
                {
                    'name': 'Study Leave',
                    'description': 'Leave for educational purposes and training',
                    'default_allocation': 10.0,
                    'requires_approval': True,
                    'color': '#6f42c1'
                },
                {
                    'name': 'Other',
                    'description': 'Other types of leave not covered above',
                    'default_allocation': 0.0,
                    'requires_approval': True,
                    'color': '#fd7e14'
                }
            ]
            
            for leave_type_data in leave_types:
                leave_type, created = LeaveType.objects.get_or_create(
                    name=leave_type_data['name'],
                    defaults=leave_type_data
                )
                if created:
                    self.stdout.write(f'Created leave type: {leave_type.name}')
                else:
                    self.stdout.write(f'Leave type already exists: {leave_type.name}')
            
            # Create approval levels for each department
            departments = Department.objects.all()
            
            for department in departments:
                # First level approval (usually department manager)
                level1, created = LeaveApprovalLevel.objects.get_or_create(
                    level=1,
                    department=department,
                    defaults={
                        'approver_role': 'Department Manager',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'Created Level 1 approval for {department.name}')
                
                # Second level approval (usually HR or senior management)
                level2, created = LeaveApprovalLevel.objects.get_or_create(
                    level=2,
                    department=department,
                    defaults={
                        'approver_role': 'HR Manager',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'Created Level 2 approval for {department.name}')
            
            self.stdout.write(
                self.style.SUCCESS('Successfully set up leave management system!')
            )
            
            # Display summary
            self.stdout.write('\nSummary:')
            self.stdout.write(f'- Created {LeaveType.objects.count()} leave types')
            self.stdout.write(f'- Created {LeaveApprovalLevel.objects.count()} approval levels')
            self.stdout.write(f'- Applied to {departments.count()} departments')
            
            self.stdout.write('\nNext steps:')
            self.stdout.write('1. Review and customize leave types as needed')
            self.stdout.write('2. Set up leave balances for employees')
            self.stdout.write('3. Configure approval workflows')
            self.stdout.write('4. Train managers and HR staff on the system')
