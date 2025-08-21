from django import forms
from django.forms import inlineformset_factory
from .models import (
    Employee, Department, Evaluation, EvaluationDetail, Goal, Training,
    KPICategory, KPI, EvaluationPeriod, Competency, CompetencyAssessment,
    GoalProgress, PerformanceImprovementPlan, EmployeeProfile, EmployeeSelfEvaluation,
    EmployeeGoalSubmission, EmployeeTrainingRequest, EmployeeLeaveRequest,
    LeaveBalance, LeaveType, LeaveApprovalLevel
)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone',
            'department', 'position', 'hire_date', 'status', 'manager',
            'gender', 'date_of_birth', 'address', 'emergency_contact',
            'emergency_phone', 'salary', 'user'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class KPICategoryForm(forms.ModelForm):
    class Meta:
        model = KPICategory
        fields = ['name', 'description', 'weight']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['category', 'name', 'description', 'target', 'unit', 'weight', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'target': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class EvaluationPeriodForm(forms.ModelForm):
    class Meta:
        model = EvaluationPeriod
        fields = ['name', 'period_type', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'employee', 'period', 'status', 'overall_score',
            'comments', 'employee_comments', 'strengths',
            'areas_for_improvement', 'development_plan'
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
            'employee_comments': forms.Textarea(attrs={'rows': 4}),
            'strengths': forms.Textarea(attrs={'rows': 3}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 3}),
            'development_plan': forms.Textarea(attrs={'rows': 3}),
            'overall_score': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class EvaluationDetailForm(forms.ModelForm):
    class Meta:
        model = EvaluationDetail
        fields = ['kpi', 'target_value', 'actual_value', 'score', 'weight', 'comments']
        widgets = {
            'target_value': forms.NumberInput(attrs={'step': '0.01'}),
            'actual_value': forms.NumberInput(attrs={'step': '0.01'}),
            'score': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

EvaluationDetailFormSet = inlineformset_factory(
    Evaluation, EvaluationDetail,
    form=EvaluationDetailForm,
    extra=1,
    can_delete=True
)

class CompetencyForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['name', 'description', 'category', 'weight', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class CompetencyAssessmentForm(forms.ModelForm):
    class Meta:
        model = CompetencyAssessment
        fields = ['competency', 'rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5', 'step': '0.1'}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            'employee', 'title', 'description', 'goal_type', 'target_date',
            'status', 'progress', 'priority', 'success_criteria',
            'obstacles', 'support_needed'
        ]
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'success_criteria': forms.Textarea(attrs={'rows': 3}),
            'obstacles': forms.Textarea(attrs={'rows': 3}),
            'support_needed': forms.Textarea(attrs={'rows': 3}),
            'progress': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class GoalProgressForm(forms.ModelForm):
    class Meta:
        model = GoalProgress
        fields = ['goal', 'progress_percentage', 'update_date', 'comments']
        widgets = {
            'update_date': forms.DateInput(attrs={'type': 'date'}),
            'progress_percentage': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'employee', 'title', 'description', 'training_type', 'provider',
            'location', 'start_date', 'end_date', 'duration_hours', 'cost',
            'status', 'score', 'objectives', 'outcomes', 'feedback', 'certificate'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'outcomes': forms.Textarea(attrs={'rows': 3}),
            'feedback': forms.Textarea(attrs={'rows': 3}),
            'duration_hours': forms.NumberInput(attrs={'min': '0', 'step': '0.5'}),
            'cost': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'score': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
        }

class PerformanceImprovementPlanForm(forms.ModelForm):
    class Meta:
        model = PerformanceImprovementPlan
        fields = [
            'employee', 'evaluation', 'start_date', 'end_date', 'status',
            'objectives', 'action_plan', 'success_criteria', 'progress_notes', 'outcome'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'action_plan': forms.Textarea(attrs={'rows': 4}),
            'success_criteria': forms.Textarea(attrs={'rows': 3}),
            'progress_notes': forms.Textarea(attrs={'rows': 3}),
            'outcome': forms.Textarea(attrs={'rows': 3}),
        }

# Search and filter forms
class EmployeeSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search employees...'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Employee.EMPLOYEE_STATUS, required=False)

class EvaluationSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search evaluations...'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Evaluation.EVALUATION_STATUS, required=False)
    period = forms.ModelChoiceField(queryset=EvaluationPeriod.objects.filter(is_active=True), required=False, empty_label="All Periods")
    rating = forms.ChoiceField(choices=[('', 'All Ratings')] + Evaluation.PERFORMANCE_RATINGS, required=False)

class GoalSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search goals...'}))
    goal_type = forms.ChoiceField(choices=[('', 'All Types')] + Goal.GOAL_TYPES, required=False)
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Goal.GOAL_STATUS, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")
    priority = forms.ChoiceField(choices=[('', 'All Priorities'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=False)

class TrainingSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search trainings...'}))
    training_type = forms.ChoiceField(choices=[('', 'All Types')] + Training.TRAINING_TYPES, required=False)
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Training.TRAINING_STATUS, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")

class ReportFilterForm(forms.Form):
    report_type = forms.ChoiceField(choices=[
        ('employee_performance', 'Employee Performance Report'),
        ('department_performance', 'Department Performance Report'),
        ('training', 'Training Report'),
        ('goal_progress', 'Goal Progress Report'),
    ])
    format = forms.ChoiceField(choices=[
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ], initial='pdf')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments")
    period = forms.ModelChoiceField(queryset=EvaluationPeriod.objects.filter(is_active=True), required=False, empty_label="All Periods")
    status = forms.ChoiceField(choices=[('', 'All Statuses')], required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    training_type = forms.ChoiceField(choices=[('', 'All Types')] + Training.TRAINING_TYPES, required=False)
    goal_type = forms.ChoiceField(choices=[('', 'All Types')] + Goal.GOAL_TYPES, required=False)
    priority = forms.ChoiceField(choices=[('', 'All Priorities'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=False)

class EmployeeProfileForm(forms.ModelForm):
    """Form for employees to update their profile"""
    class Meta:
        model = EmployeeProfile
        fields = [
            'bio', 'skills', 'certifications', 'languages', 'interests',
            'linkedin_profile', 'portfolio_url', 'profile_picture', 'resume',
            'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'emergency_contact_email',
            'bank_account_number', 'bank_name', 'tax_id', 'social_security_number'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List your key skills and competencies...'}),
            'certifications': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List your professional certifications...'}),
            'languages': forms.TextInput(attrs={'placeholder': 'e.g., English, Malay, Mandarin'}),
            'interests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your professional interests...'}),
            'linkedin_profile': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Emergency contact person name'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'placeholder': 'e.g., Spouse, Parent, Friend'}),
            'emergency_contact_phone': forms.TextInput(attrs={'placeholder': 'Emergency contact phone number'}),
            'emergency_contact_email': forms.EmailInput(attrs={'placeholder': 'Emergency contact email'}),
            'bank_account_number': forms.TextInput(attrs={'placeholder': 'Bank account number'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'Bank name'}),
            'tax_id': forms.TextInput(attrs={'placeholder': 'Tax identification number'}),
            'social_security_number': forms.TextInput(attrs={'placeholder': 'Social security number'}),
        }

class EmployeeSelfEvaluationForm(forms.ModelForm):
    """Form for employee self-evaluations"""
    class Meta:
        model = EmployeeSelfEvaluation
        fields = [
            'period', 'self_assessment', 'achievements', 'challenges',
            'goals_met', 'areas_for_improvement', 'career_aspirations', 'training_needs'
        ]
        widgets = {
            'period': forms.Select(attrs={'class': 'form-select'}),
            'self_assessment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a comprehensive self-assessment of your performance...'}),
            'achievements': forms.Textarea(attrs={'rows': 4, 'placeholder': 'List your key achievements during this period...'}),
            'challenges': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe challenges faced and how you overcame them...'}),
            'goals_met': forms.Textarea(attrs={'rows': 4, 'placeholder': 'List goals that were met during this period...'}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Identify areas where you need improvement...'}),
            'career_aspirations': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your career goals and aspirations...'}),
            'training_needs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What training and development do you need?'}),
        }

class EmployeeGoalSubmissionForm(forms.ModelForm):
    """Form for employee goal submissions"""
    class Meta:
        model = EmployeeGoalSubmission
        fields = [
            'title', 'description', 'goal_type', 'target_date', 'success_criteria',
            'resources_needed', 'priority'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter your goal title...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your goal in detail...'}),
            'goal_type': forms.Select(attrs={'class': 'form-select'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'success_criteria': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How will you measure success?'}),
            'resources_needed': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What resources and support do you need?'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

class EmployeeTrainingRequestForm(forms.ModelForm):
    """Form for employee training requests"""
    class Meta:
        model = EmployeeTrainingRequest
        fields = [
            'title', 'description', 'training_type', 'provider', 'location',
            'start_date', 'end_date', 'duration_hours', 'estimated_cost',
            'business_justification', 'expected_outcomes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Training program title...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Why do you need this training?'}),
            'training_type': forms.Select(attrs={'class': 'form-select'}),
            'provider': forms.TextInput(attrs={'placeholder': 'Training provider or institution'}),
            'location': forms.TextInput(attrs={'placeholder': 'Training location or online platform'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'min': '0', 'step': '0.5', 'placeholder': 'Duration in hours'}),
            'estimated_cost': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'placeholder': 'Estimated cost'}),
            'business_justification': forms.Textarea(attrs={'rows': 4, 'placeholder': 'How will this training benefit the business?'}),
            'expected_outcomes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What outcomes do you expect from this training?'}),
        }

class EmployeeLeaveRequestForm(forms.ModelForm):
    """Enhanced form for employee leave requests"""
    class Meta:
        model = EmployeeLeaveRequest
        fields = [
            'leave_type', 'leave_type_other', 'start_date', 'end_date', 'total_days',
            'reason', 'contact_during_leave', 'contact_phone', 'contact_email',
            'is_half_day', 'half_day_type', 'attachments', 'notes'
        ]
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-select', 'id': 'leave_type_select'}),
            'leave_type_other': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify leave type...'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_days': forms.NumberInput(attrs={'min': '0.5', 'step': '0.5', 'class': 'form-control', 'placeholder': 'Total days requested'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Reason for leave request...'}),
            'contact_during_leave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact person during leave'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact phone number'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact email'}),
            'is_half_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'half_day_type': forms.Select(attrs={'class': 'form-select'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Additional notes...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make leave_type_other required only when leave_type is not selected
        self.fields['leave_type_other'].required = False
        self.fields['half_day_type'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_type')
        leave_type_other = cleaned_data.get('leave_type_other')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_half_day = cleaned_data.get('is_half_day')
        half_day_type = cleaned_data.get('half_day_type')
        
        # Validate leave type
        if not leave_type and not leave_type_other:
            raise forms.ValidationError("Please select a leave type or specify a custom type.")
        
        # Validate dates
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date cannot be after end date.")
            
            from datetime import date
            if start_date < date.today():
                raise forms.ValidationError("Start date cannot be in the past.")
        
        # Validate half-day fields
        if is_half_day and not half_day_type:
            raise forms.ValidationError("Please specify whether it's a morning or afternoon half-day.")
        
        return cleaned_data

class LeaveApprovalForm(forms.ModelForm):
    """Form for managers/HR to approve/reject leave requests"""
    APPROVAL_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('request_changes', 'Request Changes'),
    ]
    
    action = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Add your comments...'}), required=False)
    
    class Meta:
        model = EmployeeLeaveRequest
        fields = []  # No model fields, just custom fields
    
    def __init__(self, *args, **kwargs):
        self.approval_level = kwargs.pop('approval_level', 1)
        super().__init__(*args, **kwargs)
        
        if self.approval_level == 1:
            self.fields['action'].choices = [
                ('approve', 'Approve (First Level)'),
                ('reject', 'Reject'),
                ('request_changes', 'Request Changes'),
            ]
        else:
            self.fields['action'].choices = [
                ('approve', 'Approve (Final)'),
                ('reject', 'Reject'),
                ('request_changes', 'Request Changes'),
            ]

class LeaveBalanceForm(forms.ModelForm):
    """Form for HR to manage employee leave balances"""
    class Meta:
        model = LeaveBalance
        fields = ['allocated_days', 'carried_over_days', 'notes']
        widgets = {
            'allocated_days': forms.NumberInput(attrs={'min': '0', 'step': '0.5', 'class': 'form-control'}),
            'carried_over_days': forms.NumberInput(attrs={'min': '0', 'step': '0.5', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Notes about this leave balance...'}),
        }

class LeaveTypeForm(forms.ModelForm):
    """Form for managing leave types"""
    class Meta:
        model = LeaveType
        fields = ['name', 'description', 'default_allocation', 'requires_approval', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'default_allocation': forms.NumberInput(attrs={'min': '0', 'step': '0.5', 'class': 'form-control'}),
            'requires_approval': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }

class LeaveApprovalLevelForm(forms.ModelForm):
    """Form for managing approval levels"""
    class Meta:
        model = LeaveApprovalLevel
        fields = ['level', 'department', 'approver_role', 'is_active']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'approver_role': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmployeeLoginForm(forms.Form):
    """Form for employee login"""
    employee_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Employee ID',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class EmployeePasswordChangeForm(forms.Form):
    """Form for employee password change"""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current password'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords don't match.")
            if len(new_password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data
