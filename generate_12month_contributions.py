#!/usr/bin/env python
"""
Script to generate 400 contributions over the last 12 months in the current repository.
Some days will have no contributions to make it more realistic.
"""
import os
import subprocess
from datetime import datetime, timedelta
from random import randint, choice, random

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
    "Update changelog",
    "Improve code structure",
    "Add error messages",
    "Update tests",
    "Fix security issue",
    "Optimize algorithm",
    "Add logging",
    "Update comments",
    "Refactor module",
    "Add documentation",
    "Fix memory leak"
]

def make_commit(date, message):
    """Create a commit with a specific date."""
    # Create or update a file with some content
    content_file = "contributions_log.txt"
    
    with open(content_file, 'a', encoding='utf-8') as f:
        f.write(f"Contribution on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Stage the file
    result = subprocess.run(['git', 'add', content_file], capture_output=True)
    if result.returncode != 0:
        # File might not have changed, try to force add
        subprocess.run(['git', 'add', '-f', content_file], capture_output=True)
    
    # Commit with backdated timestamp
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    env['GIT_COMMITTER_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    
    result = subprocess.run(
        ['git', 'commit', '-m', message, '--date', date.strftime('%Y-%m-%d %H:%M:%S')],
        env=env,
        capture_output=True
    )
    
    return result.returncode == 0

def main():
    """Generate 400 contributions over the last 12 months with some days having no commits."""
    print("Generating 400 contributions over the last 12 months...")
    print("Some days will have no contributions for a more realistic pattern...")
    
    # Calculate date range (12 months = ~365 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Generate 400 commits
    total_commits = 400
    commits_made = 0
    
    # We want to distribute commits over ~200-250 active days (leaving ~115-165 days with no commits)
    # This makes it more realistic - not every day has commits
    active_days_target = randint(200, 250)
    
    # Track which days will have commits
    days_with_commits = set()
    current_date = start_date
    
    # First, randomly select which days will have commits
    while len(days_with_commits) < active_days_target and current_date < end_date:
        # 60% chance of having commits on weekdays, 30% on weekends
        if current_date.weekday() < 5:  # Weekday
            if random() < 0.60:
                days_with_commits.add(current_date.date())
        else:  # Weekend
            if random() < 0.30:
                days_with_commits.add(current_date.date())
        
        current_date += timedelta(days=1)
    
    # Reset current_date
    current_date = start_date
    
    # Now distribute 400 commits across the selected days
    commits_per_day = {}
    remaining_commits = total_commits
    
    # Distribute commits to selected days
    selected_days_list = sorted(list(days_with_commits))
    
    for day in selected_days_list:
        if remaining_commits <= 0:
            break
        
        # Assign 1-5 commits per day (weighted towards 1-3)
        if remaining_commits == 1:
            commits_per_day[day] = 1
            remaining_commits -= 1
        else:
            # More likely to have 1-3 commits, less likely to have 4-5
            # Use weighted random selection
            rand_val = random()
            if rand_val < 0.4:
                num_commits = 1
            elif rand_val < 0.7:
                num_commits = 2
            elif rand_val < 0.9:
                num_commits = 3
            elif rand_val < 0.97:
                num_commits = 4
            else:
                num_commits = 5
            num_commits = min(num_commits, remaining_commits)
            commits_per_day[day] = num_commits
            remaining_commits -= num_commits
    
    # If we still have remaining commits, distribute them
    if remaining_commits > 0:
        for day in selected_days_list:
            if remaining_commits <= 0:
                break
            if day in commits_per_day:
                commits_per_day[day] += 1
                remaining_commits -= 1
    
    # Now create the commits
    print(f"Will create commits on {len(commits_per_day)} days")
    print("Generating commits...")
    
    current_date = start_date
    days_processed = 0
    
    while current_date < end_date and commits_made < total_commits:
        day_date = current_date.date()
        
        if day_date in commits_per_day:
            num_commits_today = commits_per_day[day_date]
            
            for i in range(num_commits_today):
                # Random time during the day (between 8 AM and 11 PM)
                hour = randint(8, 23)
                minute = randint(0, 59)
                commit_time = current_date.replace(hour=hour, minute=minute, second=randint(0, 59))
                
                message = choice(COMMIT_MESSAGES)
                
                if make_commit(commit_time, message):
                    commits_made += 1
                    
                    if commits_made % 50 == 0:
                        print(f"Progress: {commits_made}/{total_commits} commits created...")
                else:
                    # Try with a different approach - ensure file changes
                    try:
                        with open("contributions_log.txt", "a", encoding="utf-8") as f:
                            f.write(f"\nAdditional contribution at {commit_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        subprocess.run(['git', 'add', 'contributions_log.txt'], capture_output=True)
                        env = os.environ.copy()
                        env['GIT_AUTHOR_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
                        env['GIT_COMMITTER_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
                        subprocess.run(
                            ['git', 'commit', '-m', message, '--date', commit_time.strftime('%Y-%m-%d %H:%M:%S')],
                            env=env,
                            capture_output=True
                        )
                        commits_made += 1
                        if commits_made % 50 == 0:
                            print(f"Progress: {commits_made}/{total_commits} commits created...")
                    except:
                        pass
        
        current_date += timedelta(days=1)
        days_processed += 1
        
        if days_processed % 30 == 0:
            print(f"Processed {days_processed} days, created {commits_made} commits so far...")
    
    print(f"\nSuccessfully created {commits_made} contributions!")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Active days with commits: {len(commits_per_day)}")
    print(f"Days with no commits: {365 - len(commits_per_day)}")

if __name__ == "__main__":
    main()

