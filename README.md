# KwickPOS Test Automation Framework

A comprehensive test automation framework for KwickPOS restaurant system using Selenium WebDriver and Pytest.

## Overview

This framework tests the KwickPOS restaurant point-of-sale system, covering:
- User authentication and login functionality
- Dine-in and takeout order processing
- Menu item selection and cart management
- Financial calculations (discounts, taxes, tips)
- Database validation

## Architecture

- **Framework**: Pytest with Selenium WebDriver
- **Pattern**: Page Object Model (POM)
- **Database**: MySQL with direct validation
- **Browser**: Chrome (configurable)

## Project Structure

```
├── pages/          # Page Object Model implementations
├── tests/          # Test cases and configuration
├── utils/          # Browser management utilities
├── database/       # Database connection and operations
├── config.py       # Environment configuration
├── conftest.py     # Pytest fixtures and setup
└── requirements.txt # Project dependencies
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+**
2. **Chrome browser** installed
3. **Access to KwickPOS server** (default: 192.168.1.86)
4. **MySQL database access** to mypos database

### Installation

1. **Clone/Download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables (REQUIRED):**
   
   **⚠️ SECURITY NOTICE: Credentials are required and must be stored securely**
   
   a. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   b. Edit the `.env` file with your actual credentials:
   ```bash
   # Server Configuration
   TEST_SERVER_IP=your_actual_server_ip
   
   # Database Configuration  
   DB_USERNAME=your_actual_db_username
   DB_PASSWORD=your_actual_db_password
   DB_NAME=your_actual_db_name
   
   # SSH Configuration
   SSH_USERNAME=your_actual_ssh_username
   SSH_PASSWORD=your_actual_ssh_password
   
   # Test User Credentials
   KWICKPOS_USER=your_actual_kwickpos_username
   KWICKPOS_PASS=your_actual_kwickpos_password
   BOSS_USER=your_actual_boss_username  
   BOSS_PASS=your_actual_boss_password
   ```
   
   **🔒 IMPORTANT SECURITY NOTES:**
   - The `.env` file is automatically excluded from version control
   - Never commit credentials to your repository
   - Each team member needs their own `.env` file
   - Keep credentials secure and rotate them regularly

### Configuration

The framework uses `config.py` for centralized configuration. **All sensitive credentials must be provided via environment variables** in the `.env` file.

**Key Configuration Options:**
- `SERVER_IP`: KwickPOS server IP address (**REQUIRED**)
- `DB_*`: Database connection settings (**REQUIRED**)
- `SSH_*`: Server SSH credentials (**REQUIRED**)
- `TEST_USERS`: Login credentials for different user roles (**REQUIRED**)

**Security Features:**
- All credentials are loaded from environment variables
- No hardcoded passwords in the codebase
- Automatic validation ensures all required credentials are provided
- Clear error messages if credentials are missing

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
# Login tests only
pytest tests/test_login.py

# Ordering tests only
pytest tests/test_ordering.py
```

### Run with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in Headless Mode
```bash
HEADLESS=true pytest
```

## Test Coverage

### Login Tests (`test_login.py`)
- Successful login with valid credentials
- Failed login with invalid credentials
- Multiple user roles (kwickpos, boss)

### Ordering Tests (`test_ordering.py`)
- End-to-end order processing
- Financial calculations validation
- Database verification
- Parameterized testing with various discount/tip combinations
- Both dine-in and takeout workflows

## Page Objects

- **LoginPage**: Authentication functionality
- **DineinPage**: Table selection and guest management
- **TogoPage**: Customer information for takeout orders
- **OrderingPage**: Menu navigation and item selection
- **CartPage**: Order totals, discounts, tips, tax calculations

## Database Integration

The framework includes direct database validation:
- MySQL connection to `mypos` database
- Order verification and financial calculation validation
- SSH command execution for server management
- Database settings manipulation for test scenarios

## Troubleshooting

### Common Issues

1. **Missing environment variables**
   - Error: `ValueError: TEST_SERVER_IP environment variable is required`
   - Solution: Ensure you've created the `.env` file with all required credentials

2. **ChromeDriver not found**
   - Ensure ChromeDriver is in your PATH or use webdriver-manager
   - Install: `pip install webdriver-manager`

3. **Connection refused to server**
   - Verify SERVER_IP in your `.env` file
   - Ensure KwickPOS server is running and accessible

4. **Database connection errors**
   - Check database credentials in your `.env` file
   - Verify MySQL server is running
   - Ensure database user has proper permissions

5. **SSH connection failures**
   - Verify SSH credentials in your `.env` file
   - Ensure SSH access is enabled on the server

### Environment Variables Setup

If tests fail with connection issues, verify your `.env` file exists and contains required values:
```bash
# Check if .env file exists
ls .env

# Verify environment variables are loaded (without showing passwords)
python -c "from config import Config; print(f'Server: {Config.SERVER_IP}')"
```

**🔐 Security Reminder**: Never run commands that would display your actual passwords in terminal history.

## Contributing

1. Follow the existing Page Object Model pattern
2. Add appropriate test data and assertions
3. Include database validation where applicable
4. Update documentation for new features

## Test Data

Currently testing with limited menu items. To expand coverage:
1. Update `menu_arr` in `test_ordering.py`
2. Add new menu categories and items
3. Update price information accordingly

## Notes

- Tests automatically clear the database before execution
- Apache server is restarted when database settings are modified
- Tests include both UI and database validation
- Financial calculations are tested with various tip/discount combinations