# Leave Management System

## Overview
A comprehensive leave request and approval system for company employees with a two-level approval workflow, leave balance tracking, and document generation capabilities.

## Features

### 🎯 Core Functionality
- **Two-Level Approval System**: Different departments handle different approval levels
- **Leave Balance Management**: HR can track and manage employee leave balances
- **Document Generation**: Generate PDF/Word documents for approved leaves
- **Workflow Tracking**: Visual progress indicators for approval status

### 👥 User Roles
- **Employees**: Submit leave requests, view status, download documents
- **Managers**: First-level approval for their department
- **HR Staff**: Second-level approval, balance management, system administration

### 📋 Leave Types
- Annual Leave (21 days default)
- Sick Leave (14 days default)
- Personal Leave (5 days default)
- Maternity Leave (90 days default)
- Paternity Leave (14 days default)
- Bereavement Leave (5 days default)
- Study Leave (10 days default)
- Other (custom types)

## System Architecture

### Models
- `LeaveType`: Configurable leave types with allocations
- `LeaveBalance`: Employee leave balances by type and year
- `LeaveApprovalLevel`: Approval workflow configuration
- `EmployeeLeaveRequest`: Enhanced leave requests with workflow
- `LeaveRequestDocument`: Generated documents storage

### Approval Workflow
1. **Draft**: Employee creates request
2. **Submitted**: Request submitted for approval
3. **First Approval Pending**: Awaiting department manager
4. **First Approved**: First level approved
5. **Second Approval Pending**: Awaiting HR/final approval
6. **Approved**: Final approval granted
7. **Rejected**: Request denied

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Setup Leave System
```bash
python manage.py setup_leave_system
```

### 4. Configure Approval Levels
- Set up department managers for first-level approval
- Configure HR staff for second-level approval
- Customize approval roles as needed

## Usage Guide

### For Employees
1. Navigate to Employee Dashboard → Leave Requests
2. Click "Create Leave Request"
3. Fill in leave details and submit
4. Track approval progress
5. Download approved leave documents

### For Managers
1. Access Leave Management Dashboard
2. Review pending first-level approvals
3. Approve/reject requests with comments
4. Monitor team leave patterns

### For HR Staff
1. Access Leave Management Dashboard
2. Review second-level approvals
3. Manage leave balances
4. Generate reports and documents

## Key URLs

- **HR Dashboard**: `/leave-management/`
- **Leave Requests**: `/leave-management/requests/`
- **Leave Balances**: `/leave-management/balances/`
- **Employee Requests**: `/employee/leave-requests/`

## Customization

### Leave Types
- Modify default allocations in `setup_leave_system.py`
- Add new leave types through admin interface
- Configure approval requirements per type

### Approval Workflow
- Adjust approval levels in `LeaveApprovalLevel` model
- Customize approval roles and departments
- Modify workflow statuses as needed

## Technical Details

### Document Generation
- **PDF**: Uses ReportLab library
- **Word**: Uses python-docx library
- Templates stored in `LeaveRequestDocument` model

### Security
- Role-based access control
- Department-level permissions
- Audit trail for all approvals

### Performance
- Optimized database queries
- Pagination for large datasets
- Caching for frequently accessed data

## Support & Maintenance

### Regular Tasks
- Monitor leave balance updates
- Review approval workflows
- Generate monthly/quarterly reports
- Backup leave data

### Troubleshooting
- Check approval level configurations
- Verify department assignments
- Review user permissions
- Monitor system logs

## Future Enhancements

- Email notifications
- Mobile app integration
- Advanced reporting
- Leave calendar integration
- Automated balance calculations
