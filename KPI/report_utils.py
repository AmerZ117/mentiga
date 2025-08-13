"""
Report utilities for KPI management system
"""

from django.http import HttpResponse
from django.db.models import Avg, Count, Q
from datetime import datetime, timedelta
import csv
import json


class ReportGenerator:
    """Basic report generator for KPI system"""
    
    def __init__(self):
        pass
    
    def generate_employee_performance_report(self, report_format, filters):
        """Generate employee performance report"""
        try:
            from .models import Employee, Evaluation
            
            # Basic employee performance data
            employees = Employee.objects.filter(status='active')
            
            if filters.get('department'):
                employees = employees.filter(department_id=filters['department'])
            
            report_data = []
            for employee in employees:
                evaluations = Evaluation.objects.filter(employee=employee)
                avg_score = evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
                
                report_data.append({
                    'employee_id': employee.employee_id,
                    'name': employee.full_name,
                    'department': employee.department.name,
                    'position': employee.position,
                    'avg_score': round(avg_score, 2),
                    'evaluation_count': evaluations.count(),
                })
            
            return report_data
        except Exception as e:
            return None
    
    def generate_department_performance_report(self, report_format, filters):
        """Generate department performance report"""
        try:
            from .models import Department, Evaluation
            
            departments = Department.objects.all()
            report_data = []
            
            for dept in departments:
                evaluations = Evaluation.objects.filter(employee__department=dept)
                avg_score = evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
                employee_count = dept.employee_set.filter(status='active').count()
                
                report_data.append({
                    'department': dept.name,
                    'employee_count': employee_count,
                    'avg_score': round(avg_score, 2),
                    'evaluation_count': evaluations.count(),
                })
            
            return report_data
        except Exception as e:
            return None
    
    def generate_training_report(self, report_format, filters):
        """Generate training report"""
        try:
            from .models import Training
            
            trainings = Training.objects.all()
            
            if filters.get('training_type'):
                trainings = trainings.filter(training_type=filters['training_type'])
            
            report_data = []
            for training in trainings:
                report_data.append({
                    'training_name': training.name,
                    'training_type': training.training_type,
                    'status': training.status,
                    'score': training.score or 0,
                    'completion_date': training.completion_date.strftime('%Y-%m-%d') if training.completion_date else 'N/A',
                })
            
            return report_data
        except Exception as e:
            return None
    
    def generate_goal_progress_report(self, report_format, filters):
        """Generate goal progress report"""
        try:
            from .models import Goal
            
            goals = Goal.objects.all()
            
            if filters.get('goal_type'):
                goals = goals.filter(goal_type=filters['goal_type'])
            
            report_data = []
            for goal in goals:
                report_data.append({
                    'goal_title': goal.title,
                    'employee': goal.employee.full_name,
                    'goal_type': goal.goal_type,
                    'status': goal.status,
                    'progress': goal.progress,
                    'due_date': goal.due_date.strftime('%Y-%m-%d'),
                })
            
            return report_data
        except Exception as e:
            return None


def generate_report_response(report_data, filename, report_format):
    """Generate HTTP response for report download"""
    if not report_data:
        return None
    
    if report_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        if report_data:
            writer = csv.DictWriter(response, fieldnames=report_data[0].keys())
            writer.writeheader()
            writer.writerows(report_data)
        
        return response
    
    elif report_format == 'json':
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        response.write(json.dumps(report_data, indent=2, default=str))
        return response
    
    else:  # Default to CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        if report_data:
            writer = csv.DictWriter(response, fieldnames=report_data[0].keys())
            writer.writeheader()
            writer.writerows(report_data)
        
        return response
