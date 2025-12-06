# GitHub Contribution Generator

A Python script that generates GitHub contribution history by creating commits with backdated timestamps.

## Features

- Generate contribution history for any date range
- Customize commit frequency and maximum commits per day
- Option to exclude weekends
- Support for both SSH and HTTPS repository URLs
- Automatic repository initialization and push

## Installation

This script uses only Python standard library modules, so no additional dependencies are required.

**Requirements:**
- Python 3.x
- Git installed and configured

## Usage

### Basic Usage

```bash
python contribute.py
```

This will create a new directory with a repository containing contribution history for the past 365 days.

### Advanced Options

```bash
python contribute.py [OPTIONS]
```

**Options:**
- `-nw, --no_weekends`: Do not commit on weekends
- `-mc, --max_commits N`: Maximum commits per day (1-20, default: 10)
- `-fr, --frequency N`: Percentage of days to commit (default: 80)
- `-r, --repository URL`: Remote repository URL (SSH or HTTPS)
- `-un, --user_name NAME`: Override git user.name
- `-ue, --user_email EMAIL`: Override git user.email
- `-db, --days_before N`: Days before current date to start (default: 365)
- `-da, --days_after N`: Days after current date to continue (default: 0)

### Examples

Generate contributions for the last 30 days:
```bash
python contribute.py -db 30
```

Generate contributions excluding weekends:
```bash
python contribute.py -nw
```

Generate and push to a remote repository:
```bash
python contribute.py -r git@github.com:user/repo.git
```

Generate with custom user info:
```bash
python contribute.py -un "Your Name" -ue "your.email@example.com"
```

## Testing

Run the test suite:
```bash
python -m unittest test_contribute -v
```

## License

Apache License 2.0 - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

