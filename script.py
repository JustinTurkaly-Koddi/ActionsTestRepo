import subprocess
import datetime

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

# Authenticate with GitHub CLI
# Uncomment the line below to run actual authentication (replace <your-personal-access-token>)
# run_command("gh auth login --with-token <your-personal-access-token>")

# Generate a milestone name based on the current date
milestone_name = datetime.datetime.now().strftime("%Y%m%d")

# Uncomment below to Create a new milestone
run_command(f"gh api repos/JustinTurkaly-Koddi/ActionsTestRepo/milestones -f title={milestone_name}")

# Fetch PRs with specific labels and review status
stdout_passed, _ = run_command("gh pr list --search \"is:pr is:open base:master review:approved label:'QA - passed' -label:'HOLD'\" --json number -q '.data[].number'")
stdout_tbd, _ = run_command("gh pr list --search \"is:pr is:open base:master review:approved label:'QA - tbd' -label:'HOLD'\" --json number -q '.data[].number'")

# Combine the fetched PRs
all_prs = stdout_passed.strip().split() + stdout_tbd.strip().split()

# Print fetched PRs
print(f"Fetched PRs with QA - passed label: {stdout_passed}")
print(f"Fetched PRs with QA - tbd label: {stdout_tbd}")
print(f"All fetched PRs: {all_prs}")

# Uncomment below to add PRs to the milestone and merge them
# for pr in all_prs:
#     run_command(f"gh api repos/:owner/:repo/issues/{pr} -X PATCH -f milestone={milestone_name}")
#     run_command(f"gh pr merge {pr} --merge")
