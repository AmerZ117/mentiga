from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import (
    Department, Employee, KPICategory, KPI, EvaluationPeriod, 
    Evaluation, EvaluationDetail, Goal, Training, Competency,
    CompetencyAssessment, GoalProgress, Report, PerformanceImprovementPlan,
    Notification, EmployeeProfile, EmployeeSelfEvaluation, EmployeeGoalSubmission,
    EmployeeTrainingRequest, EmployeeLeaveRequest, LeaveType, LeaveBalance,
    LeaveApprovalLevel, LeaveRequestDocument
)
from django.utils import timezone

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'position', 'status', 'hire_date', 'has_user_account', 'user_actions']
    list_filter = ['status', 'department', 'hire_date', 'user']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']
    readonly_fields = ['created_at']
    actions = ['create_user_accounts', 'reset_passwords']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Employment Details', {
            'fields': ('department', 'position', 'hire_date', 'status', 'manager')
        }),
        ('Personal Information', {
            'fields': ('gender', 'date_of_birth', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Financial Information', {
            'fields': ('salary',)
        }),
        ('User Account', {
            'fields': ('user',),
            'description': 'Link to Django user account for employee login'
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )
    
    def has_user_account(self, obj):
        if obj.user:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    has_user_account.short_description = 'User Account'
    
    def user_actions(self, obj):
        if obj.user:
            return format_html(
                '<a class="button" href="{}">Reset Password</a>',
                reverse('admin:reset_employee_password', args=[obj.id])
            )
        else:
            return format_html(
                '<a class="button" href="{}">Create Account</a>',
                reverse('admin:create_employee_user', args=[obj.id])
            )
    user_actions.short_description = 'Actions'
    
    def create_user_accounts(self, request, queryset):
        created_count = 0
        for employee in queryset:
            if not employee.user:
                try:
                    # Create username from employee_id
                    username = employee.employee_id.lower()
                    
                    # Generate a random password
                    password = get_random_string(12)
                    
                    # Create user account
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
                    
                    # Show success message with credentials
                    messages.success(
                        request, 
                        f'User account created for {employee.full_name}. '
                        f'Username: {username}, Password: {password}'
                    )
                    
                except Exception as e:
                    messages.error(
                        request, 
                        f'Failed to create user account for {employee.full_name}: {str(e)}'
                    )
        
        if created_count > 0:
            messages.success(request, f'{created_count} user account(s) created successfully!')
    
    create_user_accounts.short_description = "Create user accounts for selected employees"
    
    def reset_passwords(self, request, queryset):
        reset_count = 0
        for employee in queryset:
            if employee.user:
                try:
                    # Generate new password
                    new_password = get_random_string(12)
                    
                    # Reset password
                    employee.user.set_password(new_password)
                    employee.user.save()
                    
                    reset_count += 1
                    
                    # Show success message with new password
                    messages.success(
                        request, 
                        f'Password reset for {employee.full_name}. '
                        f'New password: {new_password}'
                    )
                    
                except Exception as e:
                    messages.error(
                        request, 
                        f'Failed to reset password for {employee.full_name}: {str(e)}'
                    )
        
        if reset_count > 0:
            messages.success(request, f'{reset_count} password(s) reset successfully!')
    
    reset_passwords.short_description = "Reset passwords for selected employees"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:employee_id>/create-user/',
                self.admin_site.admin_view(self.create_user_view),
                name='create_employee_user',
            ),
            path(
                '<int:employee_id>/reset-password/',
                self.admin_site.admin_view(self.reset_password_view),
                name='reset_employee_password',
            ),
        ]
        return custom_urls + urls
    
    def create_user_view(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            if not employee.user:
                # Generate username and password
                username = employee.employee_id.lower()
                password = get_random_string(12)
                
                # Create user account
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
                
                messages.success(
                    request, 
                    f'User account created successfully for {employee.full_name}!<br>'
                    f'<strong>Username:</strong> {username}<br>'
                    f'<strong>Password:</strong> {password}<br>'
                    f'<strong>Login URL:</strong> <a href="/employee/login/">Employee Login</a>'
                )
            else:
                messages.warning(request, f'{employee.full_name} already has a user account.')
                
        except Exception as e:
            messages.error(request, f'Error creating user account: {str(e)}')
        
        return HttpResponseRedirect(reverse('admin:KPI_employee_change', args=[employee_id]))
    
    def reset_password_view(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            if employee.user:
                # Generate new password
                new_password = get_random_string(12)
                
                # Reset password
                employee.user.set_password(new_password)
                employee.user.save()
                
                messages.success(
                    request, 
                    f'Password reset successfully for {employee.full_name}!<br>'
                    f'<strong>New Password:</strong> {new_password}<br>'
                    f'<strong>Login URL:</strong> <a href="/employee/login/">Employee Login</a>'
                )
            else:
                messages.error(request, f'{employee.full_name} does not have a user account.')
                
        except Exception as e:
            messages.error(request, f'Error resetting password: {str(e)}')
        
        return HttpResponseRedirect(reverse('admin:KPI_employee_change', args=[employee_id]))

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

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_allocation', 'requires_approval', 'is_active', 'color_display']
    list_filter = ['requires_approval', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active', 'requires_approval']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'color')
        }),
        ('Configuration', {
            'fields': ('default_allocation', 'requires_approval', 'is_active')
        }),
    )
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'year', 'allocated_days', 'used_days', 'pending_days', 'remaining_days', 'carried_over_days']
    list_filter = ['year', 'leave_type', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    ordering = ['-year', 'employee__first_name', 'leave_type__name']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'leave_type', 'year')
        }),
        ('Leave Allocation', {
            'fields': ('allocated_days', 'carried_over_days')
        }),
        ('Usage Tracking', {
            'fields': ('used_days', 'pending_days'),
            'description': 'These fields are automatically calculated based on leave requests'
        }),
    )
    
    readonly_fields = ['used_days', 'pending_days']
    
    def remaining_days(self, obj):
        return obj.remaining_days
    remaining_days.short_description = 'Remaining Days'

@admin.register(LeaveApprovalLevel)
class LeaveApprovalLevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'department', 'approver_role', 'is_active']
    list_filter = ['level', 'is_active', 'department']
    search_fields = ['department__name', 'approver_role']
    ordering = ['level', 'department__name']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Approval Configuration', {
            'fields': ('level', 'department', 'approver_role')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(EmployeeLeaveRequest)
class EmployeeLeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type_display', 'start_date', 'end_date', 'total_days', 'status', 'submitted_at', 'approval_progress_display']
    list_filter = ['status', 'leave_type', 'start_date', 'submitted_at', 'employee__department']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'created_at', 'updated_at', 'approval_progress']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee', 'leave_type', 'leave_type_other')
        }),
        ('Leave Details', {
            'fields': ('start_date', 'end_date', 'total_days', 'is_half_day', 'half_day_type')
        }),
        ('Request Information', {
            'fields': ('reason', 'notes', 'attachments')
        }),
        ('Emergency Contact', {
            'fields': ('contact_during_leave', 'contact_phone', 'contact_email')
        }),
        ('Approval Workflow', {
            'fields': ('status', 'first_approver', 'first_approval_date', 'first_approval_comments'),
            'description': 'First level approval details'
        }),
        ('Final Approval', {
            'fields': ('second_approver', 'second_approval_date', 'second_approval_comments'),
            'description': 'Second level approval details'
        }),
        ('Rejection Details', {
            'fields': ('rejected_by', 'rejection_date', 'rejection_reason'),
            'description': 'Only filled if request is rejected'
        }),
        ('System Information', {
            'fields': ('submitted_at', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_requests', 'reject_requests', 'reset_to_draft']
    
    def leave_type_display(self, obj):
        return obj.leave_type_display
    leave_type_display.short_description = 'Leave Type'
    
    def approval_progress_display(self, obj):
        progress = obj.approval_progress
        if progress == 100:
            color = '#28a745'
            icon = '✓'
        elif progress > 0:
            color = '#ffc107'
            icon = '⏳'
        else:
            color = '#6c757d'
            icon = '⏸'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 5px;">'
            '<span style="color: {};">{}</span>'
            '<div style="width: 60px; height: 8px; background: #e9ecef; border-radius: 4px;">'
            '<div style="width: {}%; height: 100%; background: {}; border-radius: 4px;"></div>'
            '</div>'
            '<span style="font-size: 12px; color: #6c757d;">{}%</span>'
            '</div>',
            color, icon, progress, color, progress
        )
    approval_progress_display.short_description = 'Progress'
    
    def approve_requests(self, request, queryset):
        approved_count = 0
        for leave_request in queryset:
            if leave_request.status in ['submitted', 'first_approval_pending']:
                leave_request.status = 'first_approved'
                leave_request.first_approver = request.user.employee if hasattr(request.user, 'employee') else None
                leave_request.first_approval_date = timezone.now()
                leave_request.save()
                approved_count += 1
        
        if approved_count > 0:
            self.message_user(request, f'Successfully approved {approved_count} leave request(s).')
        else:
            self.message_user(request, 'No requests were eligible for approval.')
    approve_requests.short_description = 'Approve selected requests (First Level)'
    
    def reject_requests(self, request, queryset):
        rejected_count = 0
        for leave_request in queryset:
            if leave_request.status in ['submitted', 'first_approval_pending', 'first_approved', 'second_approval_pending']:
                leave_request.status = 'rejected'
                leave_request.rejected_by = request.user.employee if hasattr(request.user, 'employee') else None
                leave_request.rejection_date = timezone.now()
                leave_request.rejection_reason = 'Bulk rejection from admin'
                leave_request.save()
                rejected_count += 1
        
        if rejected_count > 0:
            self.message_user(request, f'Successfully rejected {rejected_count} leave request(s).')
        else:
            self.message_user(request, 'No requests were eligible for rejection.')
    reject_requests.short_description = 'Reject selected requests'
    
    def reset_to_draft(self, request, queryset):
        reset_count = 0
        for leave_request in queryset:
            if leave_request.status != 'approved':
                leave_request.status = 'draft'
                leave_request.save()
                reset_count += 1
        
        if reset_count > 0:
            self.message_user(request, f'Successfully reset {reset_count} leave request(s) to draft.')
        else:
            self.message_user(request, 'No requests were eligible for reset.')
    reset_to_draft.short_description = 'Reset to draft'

@admin.register(LeaveRequestDocument)
class LeaveRequestDocumentAdmin(admin.ModelAdmin):
    list_display = ['leave_request', 'document_type', 'generated_at', 'generated_by']
    list_filter = ['document_type', 'generated_at']
    search_fields = ['leave_request__employee__first_name', 'leave_request__employee__last_name']
    ordering = ['-generated_at']
    readonly_fields = ['generated_at', 'generated_by']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('leave_request', 'document_type', 'file_path')
        }),
        ('Generation Details', {
            'fields': ('generated_at', 'generated_by')
        }),
    )
