from django.urls import path
from . import views

app_name = 'KPI'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    
    # Evaluation management
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
    path('evaluations/create/', views.evaluation_create, name='evaluation_create'),
    path('evaluations/<int:evaluation_id>/', views.evaluation_detail, name='evaluation_detail'),
    path('evaluations/<int:evaluation_id>/edit/', views.evaluation_edit, name='evaluation_edit'),
    path('evaluations/<int:evaluation_id>/submit/', views.evaluation_submit, name='evaluation_submit'),
    
    # Goal management
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:goal_id>/edit/', views.goal_edit, name='goal_edit'),
    path('goals/<int:goal_id>/update-progress/', views.goal_update_progress, name='goal_update_progress'),
    
    # Training management
    path('trainings/', views.training_list, name='training_list'),
    path('trainings/create/', views.training_create, name='training_create'),
    path('trainings/<int:training_id>/', views.training_detail, name='training_detail'),
    path('trainings/<int:training_id>/edit/', views.training_edit, name='training_edit'),
    path('trainings/<int:training_id>/update-status/', views.training_update_status, name='training_update_status'),
    
    # Competency management
    path('competencies/', views.competency_list, name='competency_list'),
    
    # Performance improvement plans
    path('performance-improvement-plans/', views.performance_improvement_plans, name='performance_improvement_plans'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    
    # API endpoints
    path('api/employee/<int:employee_id>/', views.get_employee_data, name='get_employee_data'),
    path('api/kpi-data/', views.get_kpi_data, name='get_kpi_data'),
    
    # Employee Self-Service URLs
    path('employee/login/', views.employee_login, name='employee_login'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('employee/self-evaluations/', views.employee_self_evaluations, name='employee_self_evaluations'),
    path('employee/self-evaluations/create/', views.employee_self_evaluation_create, name='employee_self_evaluation_create'),
    path('employee/self-evaluations/<int:evaluation_id>/edit/', views.employee_self_evaluation_edit, name='employee_self_evaluation_edit'),
    path('employee/goal-submissions/', views.employee_goal_submissions, name='employee_goal_submissions'),
    path('employee/goal-submissions/create/', views.employee_goal_submission_create, name='employee_goal_submission_create'),
    path('employee/training-requests/', views.employee_training_requests, name='employee_training_requests'),
    path('employee/training-requests/create/', views.employee_training_request_create, name='employee_training_request_create'),
    path('employee/leave-requests/', views.employee_leave_requests, name='employee_leave_requests'),
    path('employee/leave-requests/create/', views.employee_leave_request_create, name='employee_leave_request_create'),
    path('employee/change-password/', views.employee_change_password, name='employee_change_password'),
    
    # Admin Management URLs for Employee Data
    path('admin/employee-profiles/', views.admin_employee_profiles, name='admin_employee_profiles'),
    path('admin/employee-profiles/<int:profile_id>/', views.admin_employee_profile_detail, name='admin_employee_profile_detail'),
    path('admin/employee-profiles/<int:profile_id>/edit/', views.admin_employee_profile_edit, name='admin_employee_profile_edit'),
]
