from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Count, Q, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, date, timedelta
from decimal import Decimal
import json

from .models import (
    Employee, Department, Evaluation, EvaluationDetail, Goal, Training,
    KPICategory, KPI, EvaluationPeriod, Competency, CompetencyAssessment,
    GoalProgress, Report, PerformanceImprovementPlan, Notification
)
from .forms import (
    EmployeeForm, EvaluationForm, EvaluationDetailFormSet, GoalForm,
    TrainingForm, DepartmentForm, KPICategoryForm, KPIForm, EvaluationPeriodForm,
    CompetencyForm, CompetencyAssessmentForm, GoalProgressForm
)
from .report_utils import ReportGenerator, generate_report_response

@login_required
def dashboard(request):
    """Enhanced dashboard with comprehensive statistics"""
    # Get current date
    today = date.today()
    
    # Employee statistics
    total_employees = Employee.objects.filter(status='active').count()
    new_employees_this_month = Employee.objects.filter(
        hire_date__month=today.month,
        hire_date__year=today.year
    ).count()
    
    # Department statistics
    departments = Department.objects.annotate(
        employee_count=Count('employee', filter=Q(employee__status='active'))
    )
    
    # Evaluation statistics
    evaluations = Evaluation.objects.all()
    total_evaluations = evaluations.count()
    pending_evaluations = evaluations.filter(status='draft').count()
    completed_evaluations = evaluations.filter(status='approved').count()
    avg_score = evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
    
    # Goal statistics
    goals = Goal.objects.all()
    total_goals = goals.count()
    completed_goals = goals.filter(status='completed').count()
    overdue_goals = goals.filter(status='overdue').count()
    avg_progress = goals.aggregate(Avg('progress'))['progress__avg'] or 0
    
    # Training statistics
    trainings = Training.objects.all()
    total_trainings = trainings.count()
    completed_trainings = trainings.filter(status='completed').count()
    ongoing_trainings = trainings.filter(status='in_progress').count()
    avg_training_score = trainings.aggregate(Avg('score'))['score__avg'] or 0
    
    # Recent activities
    recent_evaluations = evaluations.order_by('-created_at')[:5]
    recent_goals = goals.order_by('-created_at')[:5]
    recent_trainings = trainings.order_by('-created_at')[:5]
    
    # Performance trends (last 6 months)
    six_months_ago = today - timedelta(days=180)
    monthly_scores = []
    for i in range(6):
        month_date = six_months_ago + timedelta(days=30*i)
        month_evaluations = evaluations.filter(
            created_at__year=month_date.year,
            created_at__month=month_date.month
        )
        avg_monthly_score = month_evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
        monthly_scores.append({
            'month': month_date.strftime('%b %Y'),
            'score': float(avg_monthly_score)
        })
    
    # Department performance
    department_performance = []
    for dept in departments:
        dept_evaluations = evaluations.filter(employee__department=dept)
        dept_avg_score = dept_evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
        department_performance.append({
            'name': dept.name,
            'score': float(dept_avg_score),
            'employee_count': dept.employee_count
        })
    
    context = {
        'total_employees': total_employees,
        'new_employees_this_month': new_employees_this_month,
        'total_evaluations': total_evaluations,
        'pending_evaluations': pending_evaluations,
        'completed_evaluations': completed_evaluations,
        'avg_score': round(avg_score, 2),
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'overdue_goals': overdue_goals,
        'avg_progress': round(avg_progress, 2),
        'total_trainings': total_trainings,
        'completed_trainings': completed_trainings,
        'ongoing_trainings': ongoing_trainings,
        'avg_training_score': round(avg_training_score, 2),
        'recent_evaluations': recent_evaluations,
        'recent_goals': recent_goals,
        'recent_trainings': recent_trainings,
        'monthly_scores': monthly_scores,
        'department_performance': department_performance,
        'departments': departments,
    }
    
    return render(request, 'KPI/dashboard.html', context)

@login_required
def employee_list(request):
    """Enhanced employee list with search and filtering"""
    employees = Employee.objects.select_related('department', 'manager').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(position__icontains=search_query)
        )
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        employees = employees.filter(status=status_filter)
    
    # Sort by
    sort_by = request.GET.get('sort', 'first_name')
    if sort_by in ['first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date']:
        employees = employees.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    
    context = {
        'employees': page_obj,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter,
        'status_filter': status_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'KPI/employee_list.html', context)

@login_required
def employee_create(request):
    """Create new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.full_name} created successfully.')
            return redirect('KPI:employee_detail', employee_id=employee.id)
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
        'title': 'Add New Employee',
        'action': 'Create'
    }
    
    return render(request, 'KPI/employee_form.html', context)

@login_required
def employee_detail(request, employee_id):
    """Enhanced employee detail view with comprehensive information"""
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Get employee evaluations
    evaluations = Evaluation.objects.filter(employee=employee).order_by('-created_at')
    
    # Get employee goals
    goals = Goal.objects.filter(employee=employee).order_by('-created_at')
    
    # Get employee trainings
    trainings = Training.objects.filter(employee=employee).order_by('-start_date')
    
    # Get performance statistics
    if evaluations.exists():
        avg_score = evaluations.aggregate(Avg('overall_score'))['overall_score__avg']
        total_evaluations = evaluations.count()
        completed_evaluations = evaluations.filter(status='approved').count()
    else:
        avg_score = 0
        total_evaluations = 0
        completed_evaluations = 0
    
    # Get goal statistics
    if goals.exists():
        completed_goals = goals.filter(status='completed').count()
        avg_progress = goals.aggregate(Avg('progress'))['progress__avg']
    else:
        completed_goals = 0
        avg_progress = 0
    
    # Get training statistics
    if trainings.exists():
        completed_trainings = trainings.filter(status='completed').count()
        avg_training_score = trainings.aggregate(Avg('score'))['score__avg']
    else:
        completed_trainings = 0
        avg_training_score = 0
    
    # Get recent activities
    recent_activities = []
    
    # Add recent evaluations
    for evaluation in evaluations[:3]:
        recent_activities.append({
            'type': 'evaluation',
            'title': f'Evaluation for {evaluation.period.name}',
            'date': evaluation.created_at,
            'status': evaluation.get_status_display(),
            'score': evaluation.overall_score
        })
    
    # Add recent goals
    for goal in goals[:3]:
        recent_activities.append({
            'type': 'goal',
            'title': goal.title,
            'date': goal.created_at,
            'status': goal.get_status_display(),
            'progress': goal.progress
        })
    
    # Add recent trainings
    for training in trainings[:3]:
        recent_activities.append({
            'type': 'training',
            'title': training.title,
            'date': training.start_date,
            'status': training.get_status_display(),
            'score': training.score
        })
    
    # Sort activities by date
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = recent_activities[:5]
    
    context = {
        'employee': employee,
        'evaluations': evaluations,
        'goals': goals,
        'trainings': trainings,
        'avg_score': round(avg_score, 2) if avg_score else 0,
        'total_evaluations': total_evaluations,
        'completed_evaluations': completed_evaluations,
        'completed_goals': completed_goals,
        'avg_progress': round(avg_progress, 2) if avg_progress else 0,
        'completed_trainings': completed_trainings,
        'avg_training_score': round(avg_training_score, 2) if avg_training_score else 0,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'KPI/employee_detail.html', context)

@login_required
def employee_edit(request, employee_id):
    """Edit employee"""
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.full_name} updated successfully.')
            return redirect('KPI:employee_detail', employee_id=employee.id)
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
        'title': f'Edit Employee - {employee.full_name}',
        'action': 'Update'
    }
    
    return render(request, 'KPI/employee_form.html', context)

@login_required
def evaluation_list(request):
    """Enhanced evaluation list with comprehensive filtering"""
    evaluations = Evaluation.objects.select_related(
        'employee', 'employee__department', 'evaluator', 'period'
    ).all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        evaluations = evaluations.filter(
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query) |
            Q(evaluator__first_name__icontains=search_query) |
            Q(evaluator__last_name__icontains=search_query)
        )
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        evaluations = evaluations.filter(employee__department_id=department_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        evaluations = evaluations.filter(status=status_filter)
    
    # Filter by period
    period_filter = request.GET.get('period', '')
    if period_filter:
        evaluations = evaluations.filter(period_id=period_filter)
    
    # Filter by performance rating
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        evaluations = evaluations.filter(performance_rating=rating_filter)
    
    # Sort by
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['created_at', '-created_at', 'employee__first_name', 'overall_score', 'status']:
        evaluations = evaluations.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(evaluations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    periods = EvaluationPeriod.objects.filter(is_active=True)
    
    # Calculate statistics
    total_evaluations = evaluations.count()
    completed_count = evaluations.filter(status='completed').count()
    in_progress_count = evaluations.filter(status='in_progress').count()
    avg_score = evaluations.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
    
    context = {
        'evaluations': page_obj,
        'departments': departments,
        'periods': periods,
        'search_query': search_query,
        'department_filter': department_filter,
        'status_filter': status_filter,
        'period_filter': period_filter,
        'rating_filter': rating_filter,
        'sort_by': sort_by,
        'total_evaluations': total_evaluations,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'avg_score': avg_score,
        'today': date.today(),
    }
    
    return render(request, 'KPI/evaluation_list.html', context)

@login_required
def evaluation_create(request):
    """Create new evaluation with enhanced form"""
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user.employee if hasattr(request.user, 'employee') else None
            evaluation.save()
            
            # Create evaluation details for each KPI
            kpis = KPI.objects.filter(is_active=True)
            for kpi in kpis:
                EvaluationDetail.objects.create(
                    evaluation=evaluation,
                    kpi=kpi,
                    target_value=kpi.target,
                    weight=kpi.weight
                )
            
            # Create competency assessments
            competencies = Competency.objects.filter(is_active=True)
            for competency in competencies:
                CompetencyAssessment.objects.create(
                    evaluation=evaluation,
                    competency=competency,
                    rating=3.0  # Default rating
                )
            
            messages.success(request, f'Evaluation for {evaluation.employee.full_name} created successfully.')
            return redirect('KPI:evaluation_detail', evaluation_id=evaluation.id)
    else:
        form = EvaluationForm()
    
    context = {
        'form': form,
        'title': 'Create New Evaluation',
        'action': 'Create'
    }
    
    return render(request, 'KPI/evaluation_form.html', context)

@login_required
def evaluation_detail(request, evaluation_id):
    """Enhanced evaluation detail view"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    evaluation_details = evaluation.details.all().order_by('kpi__category', 'kpi__name')
    competency_assessments = evaluation.competency_assessments.all().order_by('competency__category', 'competency__name')
    
    # Calculate weighted scores
    total_weight = sum(detail.weight for detail in evaluation_details)
    weighted_score = 0
    
    for detail in evaluation_details:
        if detail.score and detail.weight:
            weighted_score += (detail.score * detail.weight / total_weight)
    
    # Calculate competency average
    competency_avg = 0
    if competency_assessments.exists():
        competency_avg = sum(assessment.rating for assessment in competency_assessments) / competency_assessments.count()
    
    context = {
        'evaluation': evaluation,
        'evaluation_details': evaluation_details,
        'competency_assessments': competency_assessments,
        'weighted_score': round(weighted_score, 2),
        'competency_avg': round(competency_avg, 2),
        'total_weight': total_weight,
    }
    
    return render(request, 'KPI/evaluation_detail.html', context)

@login_required
def evaluation_edit(request, evaluation_id):
    """Edit evaluation with enhanced functionality"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            evaluation = form.save()
            messages.success(request, f'Evaluation for {evaluation.employee.full_name} updated successfully.')
            return redirect('KPI:evaluation_detail', evaluation_id=evaluation.id)
    else:
        form = EvaluationForm(instance=evaluation)
    
    context = {
        'form': form,
        'evaluation': evaluation,
        'title': f'Edit Evaluation - {evaluation.employee.full_name}',
        'action': 'Update'
    }
    
    return render(request, 'KPI/evaluation_form.html', context)

@login_required
def evaluation_submit(request, evaluation_id):
    """Submit evaluation for review"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    
    if evaluation.status == 'draft':
        evaluation.status = 'submitted'
        evaluation.submitted_at = timezone.now()
        evaluation.save()
        
        messages.success(request, f'Evaluation for {evaluation.employee.full_name} submitted successfully.')
    else:
        messages.warning(request, 'Evaluation can only be submitted from draft status.')
    
    return redirect('KPI:evaluation_detail', evaluation_id=evaluation.id)

@login_required
def goal_list(request):
    """Enhanced goal list with comprehensive filtering"""
    goals = Goal.objects.select_related('employee', 'employee__department').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        goals = goals.filter(
            Q(title__icontains=search_query) |
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query)
        )
    
    # Filter by goal type
    goal_type_filter = request.GET.get('goal_type', '')
    if goal_type_filter:
        goals = goals.filter(goal_type=goal_type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        goals = goals.filter(status=status_filter)
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        goals = goals.filter(employee__department_id=department_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        goals = goals.filter(priority=priority_filter)
    
    # Sort by
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['created_at', '-created_at', 'target_date', '-target_date', 'progress', '-progress', 'priority']:
        goals = goals.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(goals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    
    # Calculate statistics
    total_goals = goals.count()
    completed_count = goals.filter(status='completed').count()
    in_progress_count = goals.filter(status='in_progress').count()
    avg_progress = goals.aggregate(Avg('progress'))['progress__avg'] or 0
    
    context = {
        'goals': page_obj,
        'departments': departments,
        'search_query': search_query,
        'goal_type_filter': goal_type_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
        'total_goals': total_goals,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'avg_progress': avg_progress,
        'today': date.today(),
    }
    
    return render(request, 'KPI/goal_list.html', context)

@login_required
def goal_create(request):
    """Create new goal"""
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save()
            messages.success(request, f'Goal "{goal.title}" created successfully.')
            return redirect('KPI:goal_list')
    else:
        form = GoalForm()
    
    context = {
        'form': form,
        'title': 'Create New Goal',
        'action': 'Create'
    }
    
    return render(request, 'KPI/goal_form.html', context)

@login_required
def goal_detail(request, goal_id):
    """Goal detail view"""
    goal = get_object_or_404(Goal, id=goal_id)
    
    context = {
        'goal': goal,
    }
    
    return render(request, 'KPI/goal_detail.html', context)

@login_required
def goal_edit(request, goal_id):
    """Edit goal"""
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save()
            messages.success(request, f'Goal "{goal.title}" updated successfully.')
            return redirect('KPI:goal_detail', goal_id=goal.id)
    else:
        form = GoalForm(instance=goal)
    
    context = {
        'form': form,
        'goal': goal,
        'title': f'Edit Goal - {goal.title}',
        'action': 'Update'
    }
    
    return render(request, 'KPI/goal_form.html', context)

@login_required
def goal_update_progress(request, goal_id):
    """Update goal progress"""
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'POST':
        progress_percentage = request.POST.get('progress_percentage')
        comments = request.POST.get('progress_comments', '')
        
        if progress_percentage:
            # Update the goal's progress
            goal.progress = float(progress_percentage)
            
            # Create a progress update record
            GoalProgress.objects.create(
                goal=goal,
                progress_percentage=float(progress_percentage),
                update_date=date.today(),
                comments=comments
            )
            
            # Update goal status based on progress
            if float(progress_percentage) >= 100:
                goal.status = 'completed'
            elif float(progress_percentage) > 0:
                goal.status = 'in_progress'
            
            goal.save()
            messages.success(request, f'Progress updated for goal "{goal.title}"')
        
    return redirect('KPI:goal_list')

@login_required
def training_list(request):
    """Enhanced training list with comprehensive filtering"""
    trainings = Training.objects.select_related('employee', 'employee__department').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        trainings = trainings.filter(
            Q(title__icontains=search_query) |
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query) |
            Q(provider__icontains=search_query)
        )
    
    # Filter by training type
    training_type_filter = request.GET.get('training_type', '')
    if training_type_filter:
        trainings = trainings.filter(training_type=training_type_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        trainings = trainings.filter(status=status_filter)
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        trainings = trainings.filter(employee__department_id=department_filter)
    
    # Sort by
    sort_by = request.GET.get('sort', '-start_date')
    if sort_by in ['start_date', '-start_date', 'end_date', 'score']:
        trainings = trainings.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(trainings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    
    # Calculate statistics
    total_trainings = trainings.count()
    completed_count = trainings.filter(status='completed').count()
    in_progress_count = trainings.filter(status='in_progress').count()
    total_hours = trainings.aggregate(Sum('duration_hours'))['duration_hours__sum'] or 0
    
    context = {
        'trainings': page_obj,
        'departments': departments,
        'search_query': search_query,
        'training_type_filter': training_type_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'sort_by': sort_by,
        'total_trainings': total_trainings,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'total_hours': total_hours,
        'today': date.today(),
    }
    
    return render(request, 'KPI/training_list.html', context)

@login_required
def training_create(request):
    """Create new training"""
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save()
            messages.success(request, f'Training "{training.title}" created successfully.')
            return redirect('KPI:training_list')
    else:
        form = TrainingForm()
    
    context = {
        'form': form,
        'title': 'Create New Training',
        'action': 'Create'
    }
    
    return render(request, 'KPI/training_form.html', context)

@login_required
def training_detail(request, training_id):
    """Training detail view"""
    training = get_object_or_404(Training, id=training_id)
    
    context = {
        'training': training,
    }
    
    return render(request, 'KPI/training_detail.html', context)

@login_required
def training_edit(request, training_id):
    """Edit training"""
    training = get_object_or_404(Training, id=training_id)
    
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            training = form.save()
            messages.success(request, f'Training "{training.title}" updated successfully.')
            return redirect('KPI:training_detail', training_id=training.id)
    else:
        form = TrainingForm(instance=training)
    
    context = {
        'form': form,
        'training': training,
        'title': f'Edit Training - {training.title}',
        'action': 'Update'
    }
    
    return render(request, 'KPI/training_form.html', context)

@login_required
def training_update_status(request, training_id):
    """Update training status"""
    training = get_object_or_404(Training, id=training_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        comments = request.POST.get('comments', '')
        
        if new_status:
            training.status = new_status
            
            # Update additional fields based on status
            if new_status == 'completed':
                training.end_date = date.today()
                if not training.score and request.POST.get('score'):
                    training.score = float(request.POST.get('score'))
            
            training.save()
            messages.success(request, f'Training "{training.title}" status updated to {training.get_status_display()}')
        
    return redirect('KPI:training_list')

@login_required
def reports(request):
    """Enhanced reports page with comprehensive reporting options"""
    # Get filter options
    departments = Department.objects.all()
    periods = EvaluationPeriod.objects.filter(is_active=True)
    
    # Get report statistics
    total_reports = Report.objects.count()
    recent_reports = Report.objects.order_by('-generated_at')[:5]
    
    context = {
        'departments': departments,
        'periods': periods,
        'total_reports': total_reports,
        'recent_reports': recent_reports,
    }
    
    return render(request, 'KPI/reports.html', context)

@login_required
def generate_report(request):
    """Generate and download reports"""
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        report_format = request.POST.get('format', 'pdf')
        
        # Get filters
        filters = {}
        if request.POST.get('department'):
            filters['department'] = request.POST.get('department')
        if request.POST.get('period'):
            filters['period'] = request.POST.get('period')
        if request.POST.get('status'):
            filters['status'] = request.POST.get('status')
        if request.POST.get('date_from'):
            filters['date_from'] = request.POST.get('date_from')
        if request.POST.get('date_to'):
            filters['date_to'] = request.POST.get('date_to')
        if request.POST.get('training_type'):
            filters['training_type'] = request.POST.get('training_type')
        if request.POST.get('goal_type'):
            filters['goal_type'] = request.POST.get('goal_type')
        if request.POST.get('priority'):
            filters['priority'] = request.POST.get('priority')
        
        # Generate report
        generator = ReportGenerator()
        
        if report_type == 'employee_performance':
            report_data = generator.generate_employee_performance_report(report_format, filters)
            filename = f"employee_performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        elif report_type == 'department_performance':
            report_data = generator.generate_department_performance_report(report_format, filters)
            filename = f"department_performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        elif report_type == 'training':
            report_data = generator.generate_training_report(report_format, filters)
            filename = f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        elif report_type == 'goal_progress':
            report_data = generator.generate_goal_progress_report(report_format, filters)
            filename = f"goal_progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            messages.error(request, 'Invalid report type.')
            return redirect('KPI:reports')
        
        if report_data:
            # Save report record
            Report.objects.create(
                name=f"{report_type.replace('_', ' ').title()} Report",
                report_type=report_type,
                format=report_format,
                parameters=filters,
                generated_by=request.user
            )
            
            return generate_report_response(report_data, filename, report_format)
        else:
            messages.error(request, 'Failed to generate report.')
    
    return redirect('KPI:reports')

@login_required
def get_employee_data(request, employee_id):
    """API endpoint to get employee data for AJAX requests"""
    try:
        employee = Employee.objects.get(id=employee_id)
        data = {
            'id': employee.id,
            'employee_id': employee.employee_id,
            'full_name': employee.full_name,
            'email': employee.email,
            'department': employee.department.name,
            'position': employee.position,
            'hire_date': employee.hire_date.strftime('%Y-%m-%d'),
            'status': employee.status,
        }
        return JsonResponse(data)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

@login_required
def get_kpi_data(request):
    """API endpoint to get KPI data for AJAX requests"""
    try:
        kpis = KPI.objects.filter(is_active=True).select_related('category')
        data = []
        for kpi in kpis:
            data.append({
                'id': kpi.id,
                'name': kpi.name,
                'category': kpi.category.name,
                'target': float(kpi.target),
                'unit': kpi.unit,
                'weight': float(kpi.weight),
            })
        return JsonResponse({'kpis': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def competency_list(request):
    """List competencies"""
    competencies = Competency.objects.filter(is_active=True).order_by('category', 'name')
    
    context = {
        'competencies': competencies,
    }
    
    return render(request, 'KPI/competency_list.html', context)

@login_required
def performance_improvement_plans(request):
    """List performance improvement plans"""
    pips = PerformanceImprovementPlan.objects.select_related('employee', 'evaluation').order_by('-created_at')
    
    context = {
        'pips': pips,
    }
    
    return render(request, 'KPI/performance_improvement_plans.html', context)

@login_required
def notifications(request):
    """List user notifications"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark notifications as read
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'KPI/notifications.html', context)
