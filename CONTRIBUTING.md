# Contributing to Patient Data Analysis Using SQL

Thank you for your interest in contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, MySQL version)
- Screenshots if applicable

### Suggesting Enhancements

We welcome feature requests! Please:
- Check if the feature has already been requested
- Clearly describe the proposed feature
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git fork https://github.com/aachalmahakale/Patient-Data-Analysis-Using-SQL.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   - Ensure all existing tests pass
   - Add new tests for new features
   - Test with the actual database

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Patient-Data-Analysis-Using-SQL.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   mysql -u root -p < database/schema.sql
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def calculate_age(birthdate: date) -> int:
    """
    Calculate age from birthdate.
    
    Args:
        birthdate (date): Patient's date of birth
        
    Returns:
        int: Age in years
    """
    today = date.today()
    return today.year - birthdate.year
```

### SQL
- Use uppercase for SQL keywords
- Format queries for readability
- Add comments for complex queries
- Use meaningful aliases

Example:
```sql
-- Get patient count by state
SELECT 
    state,
    COUNT(*) AS patient_count
FROM patients
WHERE state IS NOT NULL
GROUP BY state
ORDER BY patient_count DESC;
```

### Documentation
- Update README.md for new features
- Add inline comments for complex logic
- Include docstrings for all functions
- Update database schema documentation

## Testing

Before submitting a PR:
- [ ] Test database connections
- [ ] Verify all queries execute correctly
- [ ] Test the Streamlit dashboard
- [ ] Run report generation
- [ ] Check visualizations display properly
- [ ] Ensure no hardcoded credentials

## Project Structure

When adding new features, follow this structure:

```
Patient-Data-Analysis-Using-SQL/
├── database/              # SQL schema and queries
├── healthcare_data_project/
│   ├── src/              # Python source code
│   ├── data/             # Generated reports
│   ├── docs/             # Documentation
│   └── tests/            # Unit tests (to be added)
├── .env                  # Environment config (not in git)
├── .env.example          # Example config (in git)
└── requirements.txt      # Dependencies
```

## Areas for Contribution

We especially welcome contributions in:

### 🐛 Bug Fixes
- Database connection issues
- Query optimization
- Error handling improvements

### ✨ New Features
- Additional SQL queries
- New visualization types
- Enhanced dashboard features
- Export formats (PDF, Excel)
- API endpoints
- Authentication system

### 📚 Documentation
- Tutorial videos
- API documentation
- Code examples
- Translation to other languages

### 🧪 Testing
- Unit tests
- Integration tests
- Performance tests
- Data validation

### 🎨 UI/UX
- Dashboard improvements
- Responsive design
- Accessibility features
- Custom themes

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to the maintainer

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow best practices

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making this project better! 🙏
