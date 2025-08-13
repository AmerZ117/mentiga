from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Employee(models.Model):
    EMPLOYEE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('probation', 'Probation'),
        ('contract', 'Contract'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    status = models.CharField(max_length=20, choices=EMPLOYEE_STATUS, default='active')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.employee_id}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def years_of_service(self):
        from datetime import date
        today = date.today()
        return (today - self.hire_date).days // 365
    
    class Meta:
        ordering = ['first_name', 'last_name']

class Competency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)  # Technical, Soft Skills, Leadership, etc.
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.category}"
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = "Competencies"

class KPICategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "KPI Categories"

class KPI(models.Model):
    category = models.ForeignKey(KPICategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    target = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
    class Meta:
        ordering = ['category', 'name']

class EvaluationPeriod(models.Model):
    PERIOD_TYPES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('mid_year', 'Mid-Year'),
    ]
    
    name = models.CharField(max_length=100)
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
    
    class Meta:
        ordering = ['-start_date']

class Evaluation(models.Model):
    EVALUATION_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    PERFORMANCE_RATINGS = [
        ('excellent', 'Excellent (90-100)'),
        ('very_good', 'Very Good (80-89)'),
        ('good', 'Good (70-79)'),
        ('satisfactory', 'Satisfactory (60-69)'),
        ('needs_improvement', 'Needs Improvement (Below 60)'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='evaluations_conducted')
    period = models.ForeignKey(EvaluationPeriod, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=EVALUATION_STATUS, default='draft')
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    performance_rating = models.CharField(max_length=20, choices=PERFORMANCE_RATINGS, null=True, blank=True)
    comments = models.TextField(blank=True)
    employee_comments = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    development_plan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Evaluation for {self.employee.full_name} - {self.period.name}"
    
    def save(self, *args, **kwargs):
        if self.overall_score:
            if self.overall_score >= 90:
                self.performance_rating = 'excellent'
            elif self.overall_score >= 80:
                self.performance_rating = 'very_good'
            elif self.overall_score >= 70:
                self.performance_rating = 'good'
            elif self.overall_score >= 60:
                self.performance_rating = 'satisfactory'
            else:
                self.performance_rating = 'needs_improvement'
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['employee', 'period']

class EvaluationDetail(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='details')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    actual_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.kpi.name} - Score: {self.score}"
    
    class Meta:
        ordering = ['kpi__category', 'kpi__name']

class CompetencyAssessment(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='competency_assessments')
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.competency.name} - Rating: {self.rating}"
    
    class Meta:
        ordering = ['competency__category', 'competency__name']

class Goal(models.Model):
    GOAL_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    GOAL_TYPES = [
        ('performance', 'Performance Goal'),
        ('development', 'Development Goal'),
        ('project', 'Project Goal'),
        ('personal', 'Personal Goal'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default='performance')
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='pending')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    success_criteria = models.TextField(blank=True)
    obstacles = models.TextField(blank=True)
    support_needed = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.employee.full_name}"
    
    class Meta:
        ordering = ['-created_at']

class GoalProgress(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_updates')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    update_date = models.DateField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.goal.title} - {self.progress_percentage}% on {self.update_date}"
    
    class Meta:
        ordering = ['-update_date']

class Training(models.Model):
    TRAINING_STATUS = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    TRAINING_TYPES = [
        ('technical', 'Technical Training'),
        ('soft_skills', 'Soft Skills Training'),
        ('leadership', 'Leadership Training'),
        ('compliance', 'Compliance Training'),
        ('certification', 'Certification'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPES, default='technical')
    provider = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=TRAINING_STATUS, default='planned')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    objectives = models.TextField(blank=True)
    outcomes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.employee.full_name}"
    
    class Meta:
        ordering = ['-start_date']

class Report(models.Model):
    REPORT_TYPES = [
        ('employee_performance', 'Employee Performance Report'),
        ('department_performance', 'Department Performance Report'),
        ('training_report', 'Training Report'),
        ('goal_progress', 'Goal Progress Report'),
        ('evaluation_summary', 'Evaluation Summary Report'),
        ('competency_report', 'Competency Assessment Report'),
        ('custom', 'Custom Report'),
    ]
    
    REPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=REPORT_FORMATS, default='pdf')
    parameters = models.JSONField(default=dict, blank=True)  # Store report filters/parameters
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=500, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, blank=True)  # daily, weekly, monthly
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
    
    class Meta:
        ordering = ['-generated_at']

class PerformanceImprovementPlan(models.Model):
    PIP_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('extended', 'Extended'),
        ('terminated', 'Terminated'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=PIP_STATUS, default='active')
    objectives = models.TextField()
    action_plan = models.TextField()
    success_criteria = models.TextField()
    progress_notes = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"PIP for {self.employee.full_name} - {self.start_date}"
    
    class Meta:
        ordering = ['-start_date']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('evaluation_due', 'Evaluation Due'),
        ('goal_deadline', 'Goal Deadline'),
        ('training_reminder', 'Training Reminder'),
        ('report_ready', 'Report Ready'),
        ('system_alert', 'System Alert'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    class Meta:
        ordering = ['-created_at']

class EmployeeProfile(models.Model):
    """Employee self-service profile for updates and submissions"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="Personal bio and summary")
    skills = models.TextField(blank=True, help_text="Skills and competencies")
    certifications = models.TextField(blank=True, help_text="Professional certifications")
    languages = models.CharField(max_length=200, blank=True, help_text="Languages spoken")
    interests = models.TextField(blank=True, help_text="Professional interests and hobbies")
    linkedin_profile = models.URLField(blank=True, help_text="LinkedIn profile URL")
    portfolio_url = models.URLField(blank=True, help_text="Portfolio or personal website")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    social_security_number = models.CharField(max_length=20, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    last_profile_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Profile for {self.employee.full_name}"
    
    def get_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.bio, self.skills, self.certifications, self.languages,
            self.interests, self.emergency_contact_name, self.emergency_contact_phone,
            self.bank_account_number, self.bank_name, self.tax_id
        ]
        filled_fields = sum(1 for field in fields if field)
        return (filled_fields / len(fields)) * 100
    
    class Meta:
        verbose_name = "Employee Profile"
        verbose_name_plural = "Employee Profiles"

class EmployeeSelfEvaluation(models.Model):
    """Employee self-evaluation submissions"""
    EVALUATION_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='self_evaluations')
    period = models.ForeignKey(EvaluationPeriod, on_delete=models.CASCADE)
    self_assessment = models.TextField(help_text="Employee's self-assessment")
    achievements = models.TextField(help_text="Key achievements during the period")
    challenges = models.TextField(help_text="Challenges faced and how they were overcome")
    goals_met = models.TextField(help_text="Goals that were met during the period")
    areas_for_improvement = models.TextField(help_text="Areas where improvement is needed")
    career_aspirations = models.TextField(help_text="Career goals and aspirations")
    training_needs = models.TextField(help_text="Training and development needs")
    status = models.CharField(max_length=20, choices=EVALUATION_STATUS, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_self_evaluations')
    review_comments = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Self-Evaluation for {self.employee.full_name} - {self.period.name}"
    
    class Meta:
        unique_together = ['employee', 'period']
        ordering = ['-created_at']
        verbose_name = "Employee Self-Evaluation"
        verbose_name_plural = "Employee Self-Evaluations"

class EmployeeGoalSubmission(models.Model):
    """Employee goal submissions and updates"""
    GOAL_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='goal_submissions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_type = models.CharField(max_length=20, choices=Goal.GOAL_TYPES, default='performance')
    target_date = models.DateField()
    success_criteria = models.TextField(help_text="How success will be measured")
    resources_needed = models.TextField(blank=True, help_text="Resources and support needed")
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='draft')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_goals')
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.employee.full_name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Employee Goal Submission"
        verbose_name_plural = "Employee Goal Submissions"

class EmployeeTrainingRequest(models.Model):
    """Employee training requests"""
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    TRAINING_TYPES = [
        ('technical', 'Technical Training'),
        ('soft_skills', 'Soft Skills Training'),
        ('leadership', 'Leadership Training'),
        ('compliance', 'Compliance Training'),
        ('certification', 'Certification'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('online_course', 'Online Course'),
        ('conference', 'Conference'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_requests')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Why this training is needed")
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPES, default='technical')
    provider = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    business_justification = models.TextField(help_text="How this training benefits the business")
    expected_outcomes = models.TextField(help_text="Expected outcomes and benefits")
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_training_requests')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.employee.full_name}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Employee Training Request"
        verbose_name_plural = "Employee Training Requests"

class EmployeeLeaveRequest(models.Model):
    """Employee leave requests"""
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('bereavement', 'Bereavement Leave'),
        ('study', 'Study Leave'),
        ('other', 'Other'),
    ]
    
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, default='annual')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=1, help_text="Total leave days requested")
    reason = models.TextField(help_text="Reason for leave request")
    contact_during_leave = models.CharField(max_length=100, blank=True, help_text="Emergency contact during leave")
    contact_phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leave_requests')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.leave_type.title()} Leave - {self.employee.full_name}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Employee Leave Request"
        verbose_name_plural = "Employee Leave Requests"
