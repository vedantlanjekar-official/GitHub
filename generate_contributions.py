#!/usr/bin/env python
"""
Script to generate 400 contributions over the last 6 months in the current repository.
"""
import os
import subprocess
from datetime import datetime, timedelta
from random import randint, choice

# List of commit messages to make it look more realistic
COMMIT_MESSAGES = [
    "Update documentation",
    "Fix minor bug",
    "Refactor code",
    "Add new feature",
    "Improve performance",
    "Update dependencies",
    "Fix typo",
    "Add comments",
    "Optimize code",
    "Update README",
    "Fix formatting",
    "Add test cases",
    "Update configuration",
    "Improve error handling",
    "Clean up code",
    "Add validation",
    "Update license",
    "Fix linting issues",
    "Add examples",
    "Update changelog"
]

def make_commit(date, message):
    """Create a commit with a specific date."""
    # Create or update a file with some content
    content_file = "contributions_log.txt"
    
    with open(content_file, 'a', encoding='utf-8') as f:
        f.write(f"Contribution on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Stage the file
    subprocess.run(['git', 'add', content_file], check=True, capture_output=True)
    
    # Commit with backdated timestamp
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    env['GIT_COMMITTER_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    
    subprocess.run(
        ['git', 'commit', '-m', message, '--date', date.strftime('%Y-%m-%d %H:%M:%S')],
        check=True,
        env=env,
        capture_output=True
    )

def main():
    """Generate 400 contributions over the last 6 months."""
    print("Generating 400 contributions over the last 6 months...")
    
    # Calculate date range (6 months = ~180 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Generate 400 commits
    total_commits = 400
    commits_made = 0
    
    # Distribute commits over the 180-day period
    # Some days will have more commits, some fewer
    current_date = start_date
    
    while commits_made < total_commits and current_date < end_date:
        # Randomly decide how many commits for this day (1-5 commits per day on average)
        # But we need to ensure we get exactly 400 total
        remaining_commits = total_commits - commits_made
        remaining_days = (end_date - current_date).days
        
        if remaining_days <= 0:
            break
            
        # Calculate average commits per remaining day
        avg_per_day = remaining_commits / remaining_days if remaining_days > 0 else 0
        
        # For this day, commit 1-5 times, but ensure we don't exceed total
        if remaining_days == 1:
            commits_today = remaining_commits
        else:
            # Use weighted random to get more commits on some days
            max_commits_today = min(8, remaining_commits)
            commits_today = randint(1, max(1, int(avg_per_day * 2)))
            commits_today = min(commits_today, remaining_commits)
        
        # Skip weekends occasionally (70% chance of committing on weekends)
        if current_date.weekday() >= 5:  # Saturday or Sunday
            if randint(1, 100) > 70:
                current_date += timedelta(days=1)
                continue
        
        # Make commits for this day
        for i in range(commits_today):
            # Random time during the day (between 9 AM and 11 PM)
            hour = randint(9, 23)
            minute = randint(0, 59)
            commit_time = current_date.replace(hour=hour, minute=minute, second=randint(0, 59))
            
            message = choice(COMMIT_MESSAGES)
            try:
                make_commit(commit_time, message)
                commits_made += 1
                
                if commits_made % 50 == 0:
                    print(f"Progress: {commits_made}/{total_commits} commits created...")
            except Exception as e:
                print(f"Error creating commit: {e}")
                continue
        
        # Move to next day
        current_date += timedelta(days=1)
    
    print(f"\nSuccessfully created {commits_made} contributions!")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()

