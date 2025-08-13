from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from KPI.models import (
    Department, Employee, KPICategory, KPI, EvaluationPeriod, 
    Competency, Evaluation, EvaluationDetail, CompetencyAssessment,
    Goal, GoalProgress, Training, PerformanceImprovementPlan
)
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the KPI system with comprehensive sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive sample data...')
        
        # Create departments
        departments_data = [
            {'name': 'Human Resources', 'description': 'HR and personnel management'},
            {'name': 'Information Technology', 'description': 'IT infrastructure and development'},
            {'name': 'Finance', 'description': 'Financial management and accounting'},
            {'name': 'Marketing', 'description': 'Marketing and sales operations'},
            {'name': 'Operations', 'description': 'Business operations and logistics'},
            {'name': 'Research & Development', 'description': 'R&D and innovation'},
        ]
        
        departments = []
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create competencies
        competencies_data = [
            # Technical Competencies
            {'name': 'Programming Skills', 'category': 'Technical', 'weight': 15.0},
            {'name': 'Database Management', 'category': 'Technical', 'weight': 10.0},
            {'name': 'System Administration', 'category': 'Technical', 'weight': 12.0},
            {'name': 'Network Security', 'category': 'Technical', 'weight': 8.0},
            
            # Soft Skills
            {'name': 'Communication', 'category': 'Soft Skills', 'weight': 20.0},
            {'name': 'Leadership', 'category': 'Soft Skills', 'weight': 15.0},
            {'name': 'Problem Solving', 'category': 'Soft Skills', 'weight': 18.0},
            {'name': 'Teamwork', 'category': 'Soft Skills', 'weight': 12.0},
            
            # Leadership Competencies
            {'name': 'Strategic Thinking', 'category': 'Leadership', 'weight': 25.0},
            {'name': 'Decision Making', 'category': 'Leadership', 'weight': 20.0},
            {'name': 'Change Management', 'category': 'Leadership', 'weight': 15.0},
            {'name': 'Mentoring', 'category': 'Leadership', 'weight': 10.0},
        ]
        
        competencies = []
        for comp_data in competencies_data:
            comp, created = Competency.objects.get_or_create(
                name=comp_data['name'],
                defaults={
                    'category': comp_data['category'],
                    'weight': comp_data['weight'],
                    'description': f'{comp_data["name"]} competency for {comp_data["category"]} category'
                }
            )
            competencies.append(comp)
            if created:
                self.stdout.write(f'Created competency: {comp.name}')
        
        # Create KPI categories
        kpi_categories_data = [
            {'name': 'Productivity', 'description': 'Work output and efficiency metrics', 'weight': 30.0},
            {'name': 'Quality', 'description': 'Quality of work and deliverables', 'weight': 25.0},
            {'name': 'Innovation', 'description': 'Creativity and process improvement', 'weight': 20.0},
            {'name': 'Collaboration', 'description': 'Teamwork and cross-functional cooperation', 'weight': 15.0},
            {'name': 'Professional Development', 'description': 'Learning and skill development', 'weight': 10.0},
        ]
        
        kpi_categories = []
        for cat_data in kpi_categories_data:
            cat, created = KPICategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'weight': cat_data['weight']
                }
            )
            kpi_categories.append(cat)
            if created:
                self.stdout.write(f'Created KPI category: {cat.name}')
        
        # Create KPIs
        kpis_data = [
            # Productivity KPIs
            {'category': 'Productivity', 'name': 'Tasks Completed', 'description': 'Number of tasks completed on time', 'target': 95.0, 'unit': '%', 'weight': 40.0},
            {'category': 'Productivity', 'name': 'Project Delivery', 'description': 'Projects delivered within deadline', 'target': 90.0, 'unit': '%', 'weight': 35.0},
            {'category': 'Productivity', 'name': 'Work Hours', 'description': 'Effective utilization of work hours', 'target': 85.0, 'unit': '%', 'weight': 25.0},
            
            # Quality KPIs
            {'category': 'Quality', 'name': 'Error Rate', 'description': 'Reduction in error rate', 'target': 5.0, 'unit': '%', 'weight': 45.0},
            {'category': 'Quality', 'name': 'Customer Satisfaction', 'description': 'Customer satisfaction scores', 'target': 4.5, 'unit': 'Rating', 'weight': 35.0},
            {'category': 'Quality', 'name': 'Code Quality', 'description': 'Code review scores', 'target': 4.0, 'unit': 'Rating', 'weight': 20.0},
            
            # Innovation KPIs
            {'category': 'Innovation', 'name': 'Process Improvements', 'description': 'Number of process improvements suggested', 'target': 3.0, 'unit': 'Count', 'weight': 40.0},
            {'category': 'Innovation', 'name': 'New Ideas', 'description': 'Innovative ideas implemented', 'target': 2.0, 'unit': 'Count', 'weight': 35.0},
            {'category': 'Innovation', 'name': 'Technology Adoption', 'description': 'New technologies learned', 'target': 1.0, 'unit': 'Count', 'weight': 25.0},
            
            # Collaboration KPIs
            {'category': 'Collaboration', 'name': 'Cross-functional Projects', 'description': 'Participation in cross-functional projects', 'target': 2.0, 'unit': 'Count', 'weight': 40.0},
            {'category': 'Collaboration', 'name': 'Knowledge Sharing', 'description': 'Knowledge sharing sessions conducted', 'target': 4.0, 'unit': 'Count', 'weight': 35.0},
            {'category': 'Collaboration', 'name': 'Team Support', 'description': 'Support provided to team members', 'target': 85.0, 'unit': '%', 'weight': 25.0},
            
            # Professional Development KPIs
            {'category': 'Professional Development', 'name': 'Training Completed', 'description': 'Training programs completed', 'target': 3.0, 'unit': 'Count', 'weight': 40.0},
            {'category': 'Professional Development', 'name': 'Certifications', 'description': 'Professional certifications obtained', 'target': 1.0, 'unit': 'Count', 'weight': 35.0},
            {'category': 'Professional Development', 'name': 'Skill Development', 'description': 'New skills acquired', 'target': 2.0, 'unit': 'Count', 'weight': 25.0},
        ]
        
        kpis = []
        for kpi_data in kpis_data:
            category = next(cat for cat in kpi_categories if cat.name == kpi_data['category'])
            kpi, created = KPI.objects.get_or_create(
                name=kpi_data['name'],
                category=category,
                defaults={
                    'description': kpi_data['description'],
                    'target': kpi_data['target'],
                    'unit': kpi_data['unit'],
                    'weight': kpi_data['weight']
                }
            )
            kpis.append(kpi)
            if created:
                self.stdout.write(f'Created KPI: {kpi.name}')
        
        # Create evaluation periods
        periods_data = [
            {'name': 'Q1 2024', 'period_type': 'quarterly', 'start_date': date(2024, 1, 1), 'end_date': date(2024, 3, 31)},
            {'name': 'Q2 2024', 'period_type': 'quarterly', 'start_date': date(2024, 4, 1), 'end_date': date(2024, 6, 30)},
            {'name': 'Q3 2024', 'period_type': 'quarterly', 'start_date': date(2024, 7, 1), 'end_date': date(2024, 9, 30)},
            {'name': 'Q4 2024', 'period_type': 'quarterly', 'start_date': date(2024, 10, 1), 'end_date': date(2024, 12, 31)},
            {'name': 'Mid-Year 2024', 'period_type': 'mid_year', 'start_date': date(2024, 1, 1), 'end_date': date(2024, 6, 30)},
            {'name': 'Annual 2024', 'period_type': 'yearly', 'start_date': date(2024, 1, 1), 'end_date': date(2024, 12, 31)},
        ]
        
        periods = []
        for period_data in periods_data:
            period, created = EvaluationPeriod.objects.get_or_create(
                name=period_data['name'],
                defaults={
                    'period_type': period_data['period_type'],
                    'start_date': period_data['start_date'],
                    'end_date': period_data['end_date']
                }
            )
            periods.append(period)
            if created:
                self.stdout.write(f'Created evaluation period: {period.name}')
        
        # Create sample employees
        employees_data = [
            {
                'employee_id': 'EMP001', 'first_name': 'Ahmad', 'last_name': 'Hassan', 'email': 'ahmad.hassan@mentiga.com',
                'phone': '+60123456789', 'department': 'Information Technology', 'position': 'Senior Software Engineer',
                'hire_date': date(2020, 3, 15), 'status': 'active', 'gender': 'M', 'salary': 8500.00
            },
            {
                'employee_id': 'EMP002', 'first_name': 'Siti', 'last_name': 'Rahman', 'email': 'siti.rahman@mentiga.com',
                'phone': '+60123456790', 'department': 'Human Resources', 'position': 'HR Manager',
                'hire_date': date(2019, 6, 10), 'status': 'active', 'gender': 'F', 'salary': 7500.00
            },
            {
                'employee_id': 'EMP003', 'first_name': 'Mohammed', 'last_name': 'Ali', 'email': 'mohammed.ali@mentiga.com',
                'phone': '+60123456791', 'department': 'Finance', 'position': 'Financial Analyst',
                'hire_date': date(2021, 1, 20), 'status': 'active', 'gender': 'M', 'salary': 6500.00
            },
            {
                'employee_id': 'EMP004', 'first_name': 'Nurul', 'last_name': 'Aini', 'email': 'nurul.aini@mentiga.com',
                'phone': '+60123456792', 'department': 'Marketing', 'position': 'Marketing Specialist',
                'hire_date': date(2022, 8, 5), 'status': 'active', 'gender': 'F', 'salary': 5500.00
            },
            {
                'employee_id': 'EMP005', 'first_name': 'Raj', 'last_name': 'Kumar', 'email': 'raj.kumar@mentiga.com',
                'phone': '+60123456793', 'department': 'Operations', 'position': 'Operations Manager',
                'hire_date': date(2018, 11, 12), 'status': 'active', 'gender': 'M', 'salary': 8000.00
            },
            {
                'employee_id': 'EMP006', 'first_name': 'Li', 'last_name': 'Wei', 'email': 'li.wei@mentiga.com',
                'phone': '+60123456794', 'department': 'Research & Development', 'position': 'Research Scientist',
                'hire_date': date(2021, 9, 3), 'status': 'active', 'gender': 'M', 'salary': 7000.00
            },
            {
                'employee_id': 'EMP007', 'first_name': 'Fatimah', 'last_name': 'Ibrahim', 'email': 'fatimah.ibrahim@mentiga.com',
                'phone': '+60123456795', 'department': 'Information Technology', 'position': 'System Administrator',
                'hire_date': date(2020, 12, 1), 'status': 'active', 'gender': 'F', 'salary': 6000.00
            },
            {
                'employee_id': 'EMP008', 'first_name': 'David', 'last_name': 'Chen', 'email': 'david.chen@mentiga.com',
                'phone': '+60123456796', 'department': 'Finance', 'position': 'Accountant',
                'hire_date': date(2022, 3, 15), 'status': 'active', 'gender': 'M', 'salary': 5000.00
            },
        ]
        
        employees = []
        for emp_data in employees_data:
            dept = next(dept for dept in departments if dept.name == emp_data['department'])
            emp, created = Employee.objects.get_or_create(
                employee_id=emp_data['employee_id'],
                defaults={
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'email': emp_data['email'],
                    'phone': emp_data['phone'],
                    'department': dept,
                    'position': emp_data['position'],
                    'hire_date': emp_data['hire_date'],
                    'status': emp_data['status'],
                    'gender': emp_data['gender'],
                    'salary': emp_data['salary']
                }
            )
            employees.append(emp)
            if created:
                self.stdout.write(f'Created employee: {emp.full_name}')
        
        # Set managers
        if len(employees) >= 2:
            employees[1].manager = employees[0]  # Siti reports to Ahmad
            employees[1].save()
            employees[2].manager = employees[0]  # Mohammed reports to Ahmad
            employees[2].save()
            employees[3].manager = employees[1]  # Nurul reports to Siti
            employees[3].save()
            employees[4].manager = employees[0]  # Raj reports to Ahmad
            employees[4].save()
            employees[5].manager = employees[4]  # Li reports to Raj
            employees[5].save()
            employees[6].manager = employees[0]  # Fatimah reports to Ahmad
            employees[6].save()
            employees[7].manager = employees[2]  # David reports to Mohammed
            employees[7].save()
        
        # Create evaluations
        for i, employee in enumerate(employees):
            for j, period in enumerate(periods[:3]):  # Create evaluations for first 3 periods
                evaluator = employees[(i + 1) % len(employees)]  # Rotate evaluators
                
                evaluation, created = Evaluation.objects.get_or_create(
                    employee=employee,
                    period=period,
                    defaults={
                        'evaluator': evaluator,
                        'status': 'approved' if j > 0 else 'draft',
                        'overall_score': Decimal('85.0') + Decimal(str(i * 2)) + Decimal(str(j * 3)),
                        'comments': f'Comprehensive evaluation for {employee.full_name} in {period.name}',
                        'employee_comments': f'Employee feedback for {period.name} evaluation',
                        'strengths': f'Strong technical skills and good communication abilities',
                        'areas_for_improvement': f'Could improve in time management and leadership skills',
                        'development_plan': f'Focus on leadership training and project management skills'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created evaluation for {employee.full_name} - {period.name}')
                    
                    # Create evaluation details
                    for kpi in kpis[:5]:  # Create details for first 5 KPIs
                        actual_value = kpi.target * Decimal(str(0.8 + (i * 0.05) + (j * 0.02)))
                        score = min(Decimal('100'), max(Decimal('0'), (actual_value / kpi.target) * Decimal('100')))
                        
                        EvaluationDetail.objects.create(
                            evaluation=evaluation,
                            kpi=kpi,
                            target_value=kpi.target,
                            actual_value=actual_value,
                            score=score,
                            weight=kpi.weight,
                            comments=f'Good performance in {kpi.name}'
                        )
                    
                    # Create competency assessments
                    for competency in competencies[:6]:  # First 6 competencies
                        rating = 3.5 + (i * 0.1) + (j * 0.05)
                        rating = min(5.0, max(1.0, rating))
                        rating = Decimal(str(rating))
                        
                        CompetencyAssessment.objects.create(
                            evaluation=evaluation,
                            competency=competency,
                            rating=rating,
                            comments=f'Demonstrated {competency.name} competency'
                        )
        
        # Create goals
        goals_data = [
            {'title': 'Complete Advanced Python Course', 'goal_type': 'development', 'priority': 'high'},
            {'title': 'Implement New CRM System', 'goal_type': 'project', 'priority': 'high'},
            {'title': 'Improve Team Communication', 'goal_type': 'performance', 'priority': 'medium'},
            {'title': 'Reduce Bug Reports by 20%', 'goal_type': 'performance', 'priority': 'high'},
            {'title': 'Lead Team Building Workshop', 'goal_type': 'personal', 'priority': 'medium'},
            {'title': 'Complete Project Management Certification', 'goal_type': 'development', 'priority': 'high'},
            {'title': 'Optimize Database Performance', 'goal_type': 'project', 'priority': 'medium'},
            {'title': 'Mentor Junior Developers', 'goal_type': 'personal', 'priority': 'low'},
        ]
        
        for i, employee in enumerate(employees):
            for j, goal_data in enumerate(goals_data[:3]):  # 3 goals per employee
                target_date = date.today() + timedelta(days=30 + (j * 30))
                progress = min(Decimal('100'), Decimal(str(20 + (i * 10) + (j * 15))))
                status = 'completed' if progress >= Decimal('100') else 'in_progress' if progress > Decimal('20') else 'pending'
                
                goal, created = Goal.objects.get_or_create(
                    employee=employee,
                    title=goal_data['title'],
                    defaults={
                        'description': f'Goal for {employee.full_name}: {goal_data["title"]}',
                        'goal_type': goal_data['goal_type'],
                        'target_date': target_date,
                        'status': status,
                        'progress': progress,
                        'priority': goal_data['priority'],
                        'success_criteria': f'Successfully complete {goal_data["title"]}',
                        'obstacles': 'Time constraints and resource limitations',
                        'support_needed': 'Training resources and management support'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created goal for {employee.full_name}: {goal.title}')
                    
                    # Create goal progress updates
                    if progress > Decimal('20'):
                        GoalProgress.objects.create(
                            goal=goal,
                            progress_percentage=progress,
                            update_date=date.today() - timedelta(days=10),
                            comments=f'Progress update: {progress}% completed'
                        )
        
        # Create training records
        training_data = [
            {'title': 'Advanced Python Programming', 'training_type': 'technical', 'provider': 'Tech Academy'},
            {'title': 'Leadership Skills Workshop', 'training_type': 'leadership', 'provider': 'Leadership Institute'},
            {'title': 'Project Management Professional', 'training_type': 'certification', 'provider': 'PMI'},
            {'title': 'Communication Skills Training', 'training_type': 'soft_skills', 'provider': 'Communication Pro'},
            {'title': 'Cybersecurity Fundamentals', 'training_type': 'compliance', 'provider': 'Security Training Co'},
            {'title': 'Data Analysis Workshop', 'training_type': 'workshop', 'provider': 'Data Science Institute'},
        ]
        
        for i, employee in enumerate(employees):
            for j, training_info in enumerate(training_data[:2]):  # 2 trainings per employee
                start_date = date.today() - timedelta(days=30 + (j * 15))
                end_date = start_date + timedelta(days=5)
                status = 'completed' if j == 0 else 'in_progress'
                score = Decimal(str(85 + (i * 2) + (j * 5))) if status == 'completed' else None
                
                training, created = Training.objects.get_or_create(
                    employee=employee,
                    title=training_info['title'],
                    defaults={
                        'description': f'{training_info["title"]} training for {employee.full_name}',
                        'training_type': training_info['training_type'],
                        'provider': training_info['provider'],
                        'location': 'Online',
                        'start_date': start_date,
                        'end_date': end_date,
                        'duration_hours': 16.0,
                        'cost': 500.00,
                        'status': status,
                        'score': score,
                        'objectives': f'Learn {training_info["title"]} skills and techniques',
                        'outcomes': f'Successfully completed {training_info["title"]} training',
                        'feedback': f'Excellent training program with practical applications'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created training for {employee.full_name}: {training.title}')
        
        # Create performance improvement plans
        for i, employee in enumerate(employees[:3]):  # PIPs for first 3 employees
            evaluation = Evaluation.objects.filter(employee=employee).first()
            if evaluation:
                pip, created = PerformanceImprovementPlan.objects.get_or_create(
                    employee=employee,
                    evaluation=evaluation,
                    defaults={
                        'start_date': date.today() - timedelta(days=30),
                        'end_date': date.today() + timedelta(days=60),
                        'status': 'active',
                        'objectives': f'Improve performance in key areas for {employee.full_name}',
                        'action_plan': f'Weekly coaching sessions, skill development training, and regular feedback',
                        'success_criteria': f'Achieve 85% or higher in next evaluation',
                        'progress_notes': f'Making good progress with regular coaching sessions'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created PIP for {employee.full_name}')
        
        self.stdout.write(self.style.SUCCESS('Comprehensive sample data created successfully!'))
        self.stdout.write('You can now log in with:')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        self.stdout.write('')
        self.stdout.write('Sample data includes:')
        self.stdout.write(f'- {len(departments)} departments')
        self.stdout.write(f'- {len(competencies)} competencies')
        self.stdout.write(f'- {len(kpi_categories)} KPI categories')
        self.stdout.write(f'- {len(kpis)} KPIs')
        self.stdout.write(f'- {len(periods)} evaluation periods')
        self.stdout.write(f'- {len(employees)} employees')
        self.stdout.write(f'- Multiple evaluations with details and competency assessments')
        self.stdout.write(f'- Goals with progress tracking')
        self.stdout.write(f'- Training records')
        self.stdout.write(f'- Performance improvement plans')
