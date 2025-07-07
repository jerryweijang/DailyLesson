# Testing Guide for Daily Lesson Project

This document describes how to run and work with tests in the Daily Lesson project.

## Overview

The project now includes comprehensive test coverage for all major components:

- **Unit Tests**: Test individual classes and functions in isolation
- **Integration Tests**: Test component interactions and end-to-end workflows
- **Performance Tests**: Test system performance with larger datasets

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_interfaces.py          # Tests for abstract interfaces
├── test_lesson_service.py      # Tests for lesson fetching and selection
├── test_image_service.py       # Tests for image generation services
├── test_content_renderer.py    # Tests for content rendering
├── test_orchestrator.py        # Tests for orchestration logic
└── test_integration.py         # End-to-end integration tests
```

## Running Tests

### Quick Start

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest

# Run all tests with verbose output
python -m pytest -v

# Run using the test runner script
python run_tests.py
```

### Test Runner Script

The `run_tests.py` script provides convenient options:

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --unit

# Run only integration tests  
python run_tests.py --integration

# Run with coverage report
python run_tests.py --coverage

# Run specific test file
python run_tests.py --file test_interfaces.py

# Include slow tests
python run_tests.py --slow

# Verbose output
python run_tests.py --verbose
```

### Using pytest directly

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_interfaces.py

# Run specific test class
python -m pytest tests/test_interfaces.py::TestLessonFetcher

# Run specific test method
python -m pytest tests/test_interfaces.py::TestLessonFetcher::test_lesson_fetcher_is_abstract

# Run tests with specific markers
python -m pytest -m "not slow"          # Exclude slow tests
python -m pytest -m "unit"              # Run only unit tests
python -m pytest -m "integration"       # Run only integration tests

# Run with coverage
python -m pytest --cov=. --cov-report=html --cov-report=term

# Run in parallel (if pytest-xdist is installed)
python -m pytest -n auto
```

## Test Categories

### Unit Tests

Test individual components in isolation using mocks and fixtures:

- **Interfaces**: Abstract base class behavior
- **Lesson Service**: Subject filtering, lesson selection algorithms
- **Image Service**: Mock image generation, service integration
- **Content Renderer**: HTML/JSON rendering logic
- **Orchestrator**: Component coordination and workflow

### Integration Tests

Test component interactions and real workflows:

- **End-to-End**: Complete lesson generation workflow
- **System Integration**: Real component interactions
- **Error Recovery**: System behavior under failure conditions
- **Performance**: Response times and scalability

### Slow Tests

Tests marked with `@pytest.mark.slow` that may take longer:

- Async batch processing tests
- Large dataset performance tests
- Network simulation tests

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = 
    -v
    --tb=short
    --strict-markers
    --strict-config
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests that may take a while
```

### Requirements

Testing dependencies in `requirements.txt`:

```
pytest>=7.0.0           # Testing framework
pytest-mock>=3.10.0     # Mocking utilities
pytest-asyncio>=0.23.0  # Async test support
```

## Writing Tests

### Test Structure

Follow this pattern for new tests:

```python
"""
Unit tests for [module_name] module
"""
import pytest
from unittest.mock import Mock, patch
from module_name import ClassToTest


class TestClassName:
    """Test ClassName class"""
    
    def test_method_basic_behavior(self):
        """Test basic method behavior"""
        instance = ClassToTest()
        result = instance.method()
        assert result == expected_value
    
    def test_method_with_mock(self):
        """Test method with mocked dependencies"""
        mock_dependency = Mock()
        instance = ClassToTest(mock_dependency)
        
        result = instance.method()
        
        mock_dependency.some_method.assert_called_once()
        assert result == expected_value
    
    @pytest.mark.slow
    def test_performance_scenario(self):
        """Test performance with large dataset"""
        # Test implementation
        pass
```

### Mocking Guidelines

- Mock external dependencies (Selenium, file I/O, network calls)
- Use `unittest.mock.Mock` for simple mocks
- Use `@patch` decorator for patching modules
- Verify mock calls with `assert_called_once()`, `assert_called_with()`

### Async Testing

For async tests, use `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_method(self):
    """Test async method"""
    service = AsyncService()
    result = await service.async_method()
    assert result is not None
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Scheduled daily runs

### Test Coverage

Current test coverage includes:

- ✅ Abstract interfaces (100%)
- ✅ Lesson service components (95%+)
- ✅ Image service components (95%+)
- ✅ Content renderers (100%)
- ✅ Orchestrator logic (95%+)
- ✅ Integration workflows (90%+)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root directory
2. **Async Test Failures**: Make sure `pytest-asyncio` is installed
3. **Mock Warnings**: Use `@patch` with correct module paths
4. **Slow Tests**: Skip with `-m "not slow"` for faster runs

### Running Individual Test Components

```bash
# Test only interfaces
python -m pytest tests/test_interfaces.py

# Test only lesson service
python -m pytest tests/test_lesson_service.py

# Test only image service
python -m pytest tests/test_image_service.py

# Test only content rendering
python -m pytest tests/test_content_renderer.py

# Test only orchestrator
python -m pytest tests/test_orchestrator.py

# Test only integration
python -m pytest tests/test_integration.py
```

### Debug Mode

For debugging failed tests:

```bash
# Run with debug output
python -m pytest --tb=long -s tests/test_file.py::test_method

# Run with pdb debugger
python -m pytest --pdb tests/test_file.py::test_method

# Run single test with maximum verbosity
python -m pytest -vvv tests/test_file.py::test_method
```

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add integration tests for new workflows
4. Update this documentation if needed
5. Maintain test coverage above 90%

### Test Checklist

- [ ] Unit tests for new classes/methods
- [ ] Integration tests for new workflows
- [ ] Mock external dependencies
- [ ] Test error conditions
- [ ] Test edge cases (empty inputs, None values)
- [ ] Performance tests for complex operations
- [ ] Documentation updated

## Test Data

Tests use consistent test data:

- **Subjects**: 自然, 國文, 歷史, 地理, 公民
- **Title Formats**: 【1-1】format for most subjects, 【第一課】format for 國文
- **Mock URLs**: https://example.com/mock-images/ for image generation
- **Date Format**: YYYY-MM-DD for file outputs

This ensures tests are predictable and reproducible across environments.