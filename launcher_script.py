import subprocess
import json

# Execute the login script
login_process = subprocess.Popen(["python", "login_script.py"], stdout=subprocess.PIPE)

# Wait for the login script to complete
login_output, _ = login_process.communicate()

# Retrieve the session data from the output of the login script
session_data = json.loads(login_output.decode())

# Execute the main test script, passing the session data as an argument
main_test_process = subprocess.Popen(["python", "main_test.py", json.dumps(session_data)])

# Wait for the main test script to complete
main_test_process.wait()