import subprocess
import datetime
import json

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

# Authenticate with GitHub CLI
# Uncomment the line below to run actual authentication (replace <your-personal-access-token>)
# run_command("gh auth login --with-token <your-personal-access-token>")

# Generate a milestone name based on the current date
milestone_date = datetime.datetime.now().strftime("%Y%m%d")

# Determine if it's morning or afternoon based on the 24-hour clock
current_hour = datetime.datetime.now().hour
release_suffix = ".1" if current_hour < 12 else ".2"

# Create the full milestone name
milestone_name = milestone_date + release_suffix

# Fetch PRs with specific labels and review status
stdout_passed, _ = run_command("gh pr list --search 'is:pr is:open base:main label:\"QA - passed\" label:\"HOLD\"' --json number --json title")
stdout_tbd, _ = run_command("gh pr list --search 'is:pr is:open base:main label:\"test\"' --json number --json title")

# Convert JSON strings to Python objects (lists in this case)
passed_prs = json.loads(stdout_passed)
tbd_prs = json.loads(stdout_tbd)

# Combine the two lists
combined_prs = passed_prs + tbd_prs
print(f"All fetched PRs: {combined_prs}")

# TODO: send to slackbot.....wait for approval then continue

# Create a new milestone
run_command(f"gh api repos/JustinTurkaly-Koddi/ActionsTestRepo/milestones -f title={milestone_name}")
print(f"Created milestone: {milestone_name}")

# Loop through PRs and add them to the milestone
for pr in combined_prs:
    run_command(f"gh pr edit {pr['number']} --milestone \"{milestone_name}\"")

# Loop through PRs and merge them
for pr in combined_prs:
    run_command(f"gh pr merge {pr['number']} --merge")

