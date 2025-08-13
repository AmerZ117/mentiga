from django import forms
from django.forms import inlineformset_factory
from .models import (
    Employee, Department, Evaluation, EvaluationDetail, Goal, Training,
    KPICategory, KPI, EvaluationPeriod, Competency, CompetencyAssessment,
    GoalProgress, PerformanceImprovementPlan
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
