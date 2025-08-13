from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, Employee, KPICategory, KPI, EvaluationPeriod, 
    Evaluation, EvaluationDetail, Goal, Training, Competency,
    CompetencyAssessment, GoalProgress, Report, PerformanceImprovementPlan,
    Notification, EmployeeProfile, EmployeeSelfEvaluation, EmployeeGoalSubmission,
    EmployeeTrainingRequest, EmployeeLeaveRequest
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'position', 'status', 'hire_date']
    list_filter = ['department', 'status', 'hire_date', 'gender']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth')
        }),
        ('Employment Details', {
            'fields': ('department', 'position', 'hire_date', 'status', 'manager', 'salary')
        }),
        ('Additional Information', {
            'fields': ('address', 'emergency_contact', 'emergency_phone', 'user')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'weight', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(KPICategory)
class KPICategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight', 'description']
    search_fields = ['name']
    ordering = ['name']

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'target', 'unit', 'weight', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(EvaluationPeriod)
class EvaluationPeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'period_type', 'start_date', 'end_date', 'is_active']
    list_filter = ['period_type', 'is_active', 'start_date']
    search_fields = ['name']
    ordering = ['-start_date']

class EvaluationDetailInline(admin.TabularInline):
    model = EvaluationDetail
    extra = 1
    fields = ['kpi', 'target_value', 'actual_value', 'score', 'weight', 'comments']

class CompetencyAssessmentInline(admin.TabularInline):
    model = CompetencyAssessment
    extra = 1
    fields = ['competency', 'rating', 'comments']

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'evaluator', 'period', 'status', 'overall_score', 'performance_rating', 'created_at']
    list_filter = ['status', 'performance_rating', 'period', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'evaluator__first_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at', 'reviewed_at']
    inlines = [EvaluationDetailInline, CompetencyAssessmentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'evaluator', 'period', 'status')
        }),
        ('Scores', {
            'fields': ('overall_score', 'performance_rating')
        }),
        ('Comments', {
            'fields': ('comments', 'employee_comments', 'strengths', 'areas_for_improvement', 'development_plan')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'submitted_at', 'reviewed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EvaluationDetail)
class EvaluationDetailAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'kpi', 'target_value', 'actual_value', 'score', 'weight']
    list_filter = ['evaluation__period', 'kpi__category']
    search_fields = ['evaluation__employee__first_name', 'kpi__name']
    ordering = ['evaluation', 'kpi__category', 'kpi__name']

@admin.register(CompetencyAssessment)
class CompetencyAssessmentAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'competency', 'rating', 'comments']
    list_filter = ['competency__category', 'rating']
    search_fields = ['evaluation__employee__first_name', 'competency__name']
    ordering = ['evaluation', 'competency__category', 'competency__name']

class GoalProgressInline(admin.TabularInline):
    model = GoalProgress
    extra = 1
    fields = ['progress_percentage', 'update_date', 'comments']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'goal_type', 'target_date', 'status', 'progress', 'priority']
    list_filter = ['goal_type', 'status', 'priority', 'target_date']
    search_fields = ['title', 'employee__first_name', 'employee__last_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GoalProgressInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'title', 'description', 'goal_type', 'priority')
        }),
        ('Progress Tracking', {
            'fields': ('target_date', 'status', 'progress')
        }),
        ('Details', {
            'fields': ('success_criteria', 'obstacles', 'support_needed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GoalProgress)
class GoalProgressAdmin(admin.ModelAdmin):
    list_display = ['goal', 'progress_percentage', 'update_date', 'created_at']
    list_filter = ['update_date', 'created_at']
    search_fields = ['goal__title', 'goal__employee__first_name']
    ordering = ['-update_date']

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'training_type', 'provider', 'start_date', 'end_date', 'status', 'score']
    list_filter = ['training_type', 'status', 'start_date', 'end_date']
    search_fields = ['title', 'employee__first_name', 'employee__last_name', 'provider']
    ordering = ['-start_date']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'title', 'description', 'training_type', 'provider', 'location')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'duration_hours')
        }),
        ('Details', {
            'fields': ('cost', 'status', 'score', 'objectives', 'outcomes', 'feedback')
        }),
        ('Files', {
            'fields': ('certificate',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'format', 'generated_by', 'generated_at', 'is_scheduled']
    list_filter = ['report_type', 'format', 'is_scheduled', 'generated_at']
    search_fields = ['name', 'generated_by__username']
    ordering = ['-generated_at']
    readonly_fields = ['generated_at']
    fieldsets = (
        ('Report Information', {
            'fields': ('name', 'report_type', 'format', 'parameters')
        }),
        ('Generation', {
            'fields': ('generated_by', 'file_path', 'generated_at')
        }),
        ('Scheduling', {
            'fields': ('is_scheduled', 'schedule_frequency')
        }),
    )

@admin.register(PerformanceImprovementPlan)
class PerformanceImprovementPlanAdmin(admin.ModelAdmin):
    list_display = ['employee', 'evaluation', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['employee__first_name', 'employee__last_name']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'evaluation', 'start_date', 'end_date', 'status')
        }),
        ('Plan Details', {
            'fields': ('objectives', 'action_plan', 'success_criteria')
        }),
        ('Progress', {
            'fields': ('progress_notes', 'outcome')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    list_editable = ['is_read']

# Employee Self-Service Admin
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['employee', 'is_profile_complete', 'profile_completion_percentage', 'last_profile_update']
    list_filter = ['is_profile_complete', 'last_profile_update', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    readonly_fields = ['created_at', 'last_profile_update']
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee',)
        }),
        ('Personal Information', {
            'fields': ('bio', 'skills', 'certifications', 'languages', 'interests')
        }),
        ('Professional Links', {
            'fields': ('linkedin_profile', 'portfolio_url')
        }),
        ('Documents', {
            'fields': ('profile_picture', 'resume')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone', 'emergency_contact_email')
        }),
        ('Financial Information', {
            'fields': ('bank_account_number', 'bank_name', 'tax_id', 'social_security_number')
        }),
        ('System Information', {
            'fields': ('is_profile_complete', 'created_at', 'last_profile_update')
        }),
    )
    
    def profile_completion_percentage(self, obj):
        return f"{obj.get_completion_percentage():.1f}%"
    profile_completion_percentage.short_description = 'Profile Completion'

@admin.register(EmployeeSelfEvaluation)
class EmployeeSelfEvaluationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'period', 'status', 'submitted_at', 'reviewed_by']
    list_filter = ['status', 'period', 'submitted_at', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee', 'period', 'status')
        }),
        ('Self-Assessment', {
            'fields': ('self_assessment', 'achievements', 'challenges', 'goals_met')
        }),
        ('Development', {
            'fields': ('areas_for_improvement', 'career_aspirations', 'training_needs')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'review_comments', 'review_date')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'created_at', 'updated_at')
        }),
    )

@admin.register(EmployeeGoalSubmission)
class EmployeeGoalSubmissionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'goal_type', 'status', 'priority', 'target_date', 'progress']
    list_filter = ['status', 'goal_type', 'priority', 'target_date', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Goal Information', {
            'fields': ('employee', 'title', 'description', 'goal_type', 'priority')
        }),
        ('Timeline & Progress', {
            'fields': ('target_date', 'progress', 'status')
        }),
        ('Details', {
            'fields': ('success_criteria', 'resources_needed')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approval_date', 'approval_comments')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'created_at', 'updated_at')
        }),
    )

@admin.register(EmployeeTrainingRequest)
class EmployeeTrainingRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'training_type', 'status', 'start_date', 'end_date', 'estimated_cost']
    list_filter = ['status', 'training_type', 'start_date', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'title', 'provider']
    readonly_fields = ['submitted_at']
    fieldsets = (
        ('Request Information', {
            'fields': ('employee', 'title', 'description', 'training_type')
        }),
        ('Training Details', {
            'fields': ('provider', 'location', 'start_date', 'end_date', 'duration_hours', 'estimated_cost')
        }),
        ('Justification', {
            'fields': ('business_justification', 'expected_outcomes')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_date', 'review_comments', 'approved_date', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',)
        }),
    )

@admin.register(EmployeeLeaveRequest)
class EmployeeLeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status']
    list_filter = ['status', 'leave_type', 'start_date', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'reason']
    readonly_fields = ['submitted_at']
    fieldsets = (
        ('Leave Information', {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'total_days')
        }),
        ('Details', {
            'fields': ('reason', 'contact_during_leave', 'contact_phone')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_date', 'review_comments', 'approved_date', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',)
        }),
    )
