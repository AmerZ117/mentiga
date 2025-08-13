# 🔐 Employee Account Setup Guide

## 📋 **How Admins Create Employee IDs and Passwords**

### **Method 1: Through Django Admin Interface (Recommended)**

#### **Step 1: Create Employee**
1. Go to `http://localhost:8000/admin/` or your live admin URL
2. Login with your superuser account
3. Navigate to **KPI → Employees**
4. Click **"Add Employee"**
5. Fill in employee details:
   - **Employee ID**: e.g., "EMP001", "IT001", "HR001"
   - **First Name**: Employee's first name
   - **Last Name**: Employee's last name
   - **Email**: Employee's email address
   - **Department**: Select department
   - **Position**: Employee's job title
   - **Other required fields**

#### **Step 2: Create User Account**
1. After saving the employee, you'll see a **"Create Account"** button
2. Click it to automatically generate:
   - **Username**: Same as Employee ID (lowercase)
   - **Password**: Random 12-character password
3. The system will display the credentials clearly
4. **Copy and share these credentials with the employee**

#### **Step 3: Employee Login**
- **Login URL**: `/employee/login/`
- **Username**: Employee ID (e.g., "emp001")
- **Password**: Generated password

---

### **Method 2: Bulk Account Creation**

#### **Using Admin Actions**
1. Go to **KPI → Employees**
2. Select multiple employees (checkboxes)
3. Choose **"Create user accounts for selected employees"** from actions
4. Click **"Go"**
5. All selected employees will get accounts with generated passwords

#### **Using Management Commands**
```bash
# Create accounts for all employees without accounts
python manage.py create_employee_accounts --all

# Create accounts for specific department
python manage.py create_employee_accounts --department "IT"

# Create account for specific employee
python manage.py create_employee_accounts --employee-id "EMP001"

# Custom password length
python manage.py create_employee_accounts --all --password-length 8
```

---

### **Method 3: Individual Account Management**

#### **For Existing Employees**
1. Go to **KPI → Employees**
2. Click on employee name
3. Use **"Create Account"** button if no account exists
4. Use **"Reset Password"** button to generate new password

---

## 🎯 **Employee Login Process**

### **Step 1: Employee Receives Credentials**
- **Username**: Their Employee ID (e.g., "emp001")
- **Password**: Generated password from admin
- **Login URL**: `/employee/login/`

### **Step 2: Employee Logs In**
1. Go to employee login page
2. Enter Employee ID and password
3. Click "Sign In"
4. Access employee dashboard

### **Step 3: Employee Can**
- ✅ View and edit their profile
- ✅ Submit self-evaluations
- ✅ Set goals
- ✅ Request training
- ✅ Submit leave requests
- ✅ Change their password

---

## 🔧 **Admin Features**

### **Employee Management**
- **Create/Edit Employees**: Full employee information management
- **User Account Status**: See which employees have login accounts
- **Quick Actions**: Create accounts and reset passwords
- **Bulk Operations**: Manage multiple employees at once

### **Password Management**
- **Auto-Generated Passwords**: Secure random passwords
- **Password Reset**: Generate new passwords when needed
- **Credential Display**: Clear display of usernames and passwords

### **Monitoring**
- **Profile Completion**: Track employee profile completion rates
- **User Account Status**: Monitor which employees can access the system
- **Activity Tracking**: See employee engagement

---

## 📱 **Employee Portal Features**

### **Dashboard**
- Profile completion tracking
- Recent activities
- Quick action buttons
- Pending items summary

### **Profile Management**
- Personal information
- Skills and certifications
- Emergency contacts
- Financial information
- Document uploads

### **Self-Service**
- Performance evaluations
- Goal setting
- Training requests
- Leave requests
- Password changes

---

## 🚨 **Security Notes**

### **Password Policy**
- Passwords are auto-generated (12 characters by default)
- Employees can change passwords after first login
- Admins can reset passwords anytime

### **Access Control**
- Only employees with user accounts can login
- Each employee sees only their own data
- Admin access required for system management

### **Best Practices**
- Share credentials securely (email, SMS, in-person)
- Encourage employees to change passwords after first login
- Monitor account creation and usage
- Regular password resets for security

---

## 🆘 **Troubleshooting**

### **Common Issues**
1. **Employee can't login**
   - Check if user account exists
   - Verify username (Employee ID)
   - Reset password if needed

2. **No "Create Account" button**
   - Employee already has user account
   - Check user field in employee record

3. **Password not working**
   - Use "Reset Password" action
   - Generate new password

4. **Bulk operations not working**
   - Check employee selection
   - Verify department names
   - Use management commands for debugging

---

## 📞 **Support**

For technical support:
- Check Django admin logs
- Use management commands for bulk operations
- Review employee and user records
- Contact system administrator

---

**🎉 The system is now ready for employee self-service!**
