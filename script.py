import subprocess
import datetime

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def parse_pr_data(lines):
    parsed_data = []
    for line in lines:
        fields = line.strip().split('\t')  # Remove newline and split by tab
        if len(fields) >= 5:  # Assuming at least 5 fields
            pr_number = fields[0]
            pr_name = fields[1]
            parsed_data.append({'number': pr_number, 'name': pr_name})
    return parsed_data


# Authenticate with GitHub
# Uncomment the line below to run actual authentication (replace <your-personal-access-token>)
# run_command("gh auth login --with-token <your-personal-access-token>")

# Generate a milestone name based on the current date
milestone_date = datetime.datetime.now().strftime("%Y%m%d")

# Determine if it's morning or afternoon based on the 24-hour clock
current_hour = datetime.datetime.now().hour
release_suffix = ".1" if current_hour < 12 else ".2"

# Create the full milestone name
milestone_name = milestone_date + release_suffix

# Uncomment below to Create a new milestone
# run_command(f"gh api repos/JustinTurkaly-Koddi/ActionsTestRepo/milestones -f title={milestone_name}")
# print(f"Created milestone: {milestone_name}")
# Fetch PRs with specific labels and review status
stdout_passed, _ = run_command("gh pr list --search \"is:pr is:open base:main label:'QA - passed' -label:'HOLD'\" --json number -q '.data[].number'")
stdout_tbd, _ = run_command("gh pr list --search \"is:pr is:open base:main\"")
# stdout_tbd, _ = run_command("gh pr list --search \"is:pr is:open base:master review:approved label:'QA - tbd' -label:'HOLD'\" --json number -q '.data[].number'")

# # Combine the fetched PRs
all_prs = [stdout_tbd, stdout_tbd]
parsed = parse_pr_data(all_prs)

# parsed_passed = parse_pr_data(stdout_passed)
# parsed_tbd = parse_pr_data(stdout_tbd)
# parsed_all = parse_pr_data(all_prs)
# Print PRs
print(f"Fetched PRs with QA - passed label: {stdout_passed}")
print(f"Fetched PRs with QA - tbd label: {stdout_tbd}")
print(f"All fetched PRs: {parsed}")

# Uncomment below to add PRs to the milestone and merge
# for pr in all_prs:
#     run_command(f"gh api repos/:owner/:repo/issues/{pr} -X PATCH -f milestone={milestone_name}")
#     run_command(f"gh pr merge {pr} --merge")
