"""Synthetic CLI outcome corpus with tool-family-held-out evaluation.

No external logs or proprietary data are used. Every record is generated from
explicit templates below. Test template families never occur in training.
"""
from __future__ import annotations

LABELS = ("success", "failure", "blocked", "unknown")

# label, family, command, exit code, stdout, stderr
TRAIN = [
    ("success", "pytest_pass", "pytest tests/{path}", 0, "{n} passed in {duration}s", ""),
    ("success", "npm_pass", "npm test -- {path}", 0, "Test Suites: 1 passed, 1 total\nTests: {n} passed, {n} total", ""),
    ("success", "go_pass", "go test ./{path}", 0, "ok  \texample/{path}\t{duration}s", ""),
    ("success", "cargo_pass", "cargo test {path}", 0, "running {n} tests\ntest result: ok. {n} passed; 0 failed", ""),
    ("success", "eslint_clean", "eslint src/{path}", 0, "", ""),
    ("success", "tsc_clean", "tsc --noEmit -p {path}", 0, "", ""),
    ("success", "webpack_build", "webpack --config {path}", 0, "webpack compiled successfully in {duration} ms", ""),
    ("success", "git_clean", "git status --porcelain {path}", 0, "", ""),
    ("success", "curl_ok", "curl -i https://{path}/health", 0, "HTTP/2 200 OK\ncontent-type: application/json\n{\"status\":\"ok\"}", ""),
    ("success", "docker_build", "docker build -t {path} .", 0, "Successfully built image {path}\nSuccessfully tagged {path}:latest", ""),
    ("success", "pip_install", "pip install {path}", 0, "Successfully installed {path}-1.2.{n}", ""),
    ("success", "terraform_apply", "terraform apply -auto-approve {path}", 0, "Apply complete! Resources: {n} added, 0 changed, 0 destroyed.", ""),

    ("failure", "pytest_fail", "pytest tests/{path}", 1, "{n} failed, 2 passed in {duration}s\nFAILED test_{path} - AssertionError: expected true", ""),
    ("failure", "jest_fail", "npx jest {path}", 1, "FAIL src/{path}\nTests: {n} failed, 3 passed, 7 total\n● expected received to equal expected", ""),
    ("failure", "go_fail", "go test ./{path}", 1, "--- FAIL: Test{path} (0.01s)\nFAIL\nexit status 1", ""),
    ("failure", "cargo_fail", "cargo test {path}", 101, "test result: FAILED. 2 passed; {n} failed\nerror: test failed, to rerun pass --lib", ""),
    ("failure", "tsc_error", "tsc --noEmit -p {path}", 2, "{path}.ts({n},7): error TS2322: Type 'string' is not assignable to type 'number'.", ""),
    ("failure", "webpack_error", "webpack --config {path}", 1, "ERROR in ./src/{path}.js\nModule build failed: SyntaxError: Unexpected token", ""),
    ("failure", "python_assertion", "python {path}.py", 1, "Traceback (most recent call last):\n  File \"{path}.py\", line {n}, in <module>\nAssertionError", ""),
    ("failure", "eslint_error", "eslint src/{path}", 1, "src/{path}.js\n  {n}:5  error  'value' is not defined  no-undef\n✖ 1 problem (1 error, 0 warnings)", ""),
    ("failure", "git_conflict", "git merge {path}", 1, "Auto-merging src/{path}\nCONFLICT (content): Merge conflict in src/{path}\nAutomatic merge failed; fix conflicts and then commit the result.", ""),
    ("failure", "curl_500", "curl -i https://{path}/health", 0, "HTTP/1.1 500 Internal Server Error\n{\"status\":\"error\",\"ready\":false}", ""),
    ("failure", "docker_fail", "docker build -t {path} .", 1, "ERROR: failed to solve: process \"/bin/sh -c make {path}\" did not complete successfully: exit code: 2", ""),
    ("failure", "rust_panic", "cargo run --bin {path}", 101, "thread 'main' panicked at src/{path}.rs:{n}:9:\ncalled `Result::unwrap()` on an `Err` value", ""),

    ("blocked", "pytest_no_module", "pytest tests/{path}", 2, "", "ERROR: file or directory not found: tests/{path}\nModuleNotFoundError: No module named '{path}'"),
    ("blocked", "npm_missing", "npm test -- {path}", 1, "", "npm ERR! Missing script: \"test\"\nnpm ERR! A complete log of this run can be found in {path}.log"),
    ("blocked", "go_denied", "go test ./{path}", 1, "", "go: downloading example/{path}: reading module proxy: 403 Forbidden"),
    ("blocked", "cargo_network", "cargo test {path}", 101, "", "error: failed to download from https://crates.io/{path}\nCaused by: Couldn't resolve host name"),
    ("blocked", "permission_denied", "./scripts/{path}.sh", 126, "", "bash: ./scripts/{path}.sh: Permission denied"),
    ("blocked", "read_only", "cp source.txt {path}/target.txt", 1, "", "cp: cannot create regular file '{path}/target.txt': Read-only file system"),
    ("blocked", "git_auth", "git push origin {path}", 128, "", "remote: Invalid username or password.\nfatal: Authentication failed for 'https://example/{path}.git/'"),
    ("blocked", "rate_limit", "curl -i https://api.{path}", 0, "HTTP/1.1 429 Too Many Requests\nretry-after: 60\n{\"error\":\"rate limit exceeded\"}", ""),
    ("blocked", "disk_full", "python setup.py build {path}", 1, "", "OSError: [Errno 28] No space left on device: '{path}'"),
    ("blocked", "docker_daemon", "docker run {path}", 1, "", "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"),
    ("blocked", "network_unreachable", "ssh {path} hostname", 255, "", "ssh: connect to host {path} port 22: Network is unreachable"),
    ("blocked", "command_missing", "{path} --version", 127, "", "{path}: command not found"),

    ("unknown", "pytest_none", "pytest tests/{path}", 5, "collected 0 items\nno tests ran in {duration}s", ""),
    ("unknown", "jest_none", "npx jest {path}", 1, "No tests found, exiting with code 1\n0 tests matched {path}", ""),
    ("unknown", "cargo_none", "cargo test {path}", 0, "running 0 tests\ntest result: ok. 0 passed; 0 failed", ""),
    ("unknown", "go_none", "go test ./{path}", 0, "ok  \texample/{path}\t{duration}s [no tests to run]", ""),
    ("unknown", "npm_empty", "npm test -- {path}", 0, "", ""),
    ("unknown", "build_pending", "npm run build -- {path}", 0, "Build queued. Waiting for available worker.\nJob {n} is pending", ""),
    ("unknown", "truncated", "pytest tests/{path} > full.log", 0, "============================= test session starts ==============================\n... output truncated ...", ""),
    ("unknown", "dry_run", "terraform plan {path}", 0, "No changes. Your infrastructure matches the configuration.\nThis was a dry run; no resources were changed.", ""),
    ("unknown", "all_skipped", "pytest tests/{path}", 0, "collected {n} items\n{n} skipped in {duration}s", ""),
    ("unknown", "silent_test", "./test/{path} --verify", 0, "", ""),
    ("unknown", "incomplete", "npm run deploy -- {path}", 0, "Starting deployment to {path}...\nUploading artifacts", ""),
    ("unknown", "warning_only", "npm run check -- {path}", 0, "WARNING: deprecated option --{path} was ignored", ""),

    ("success", "ant_build", "ant -f {path}.xml test", 0, "BUILD SUCCESSFUL\nTotal time: {duration} seconds", ""),
    ("success", "nose_counts", "nosetests {path}", 0, "Tests: {n}, Failures: 0, Errors: 0\nOK", ""),
    ("success", "minitest_pass", "ruby {path}_test.rb", 0, "{n} runs, {n} assertions, 0 failures, 0 errors, 0 skips", ""),
    ("success", "health_json_ok", "curl -sS https://{path}/ready", 0, "{\"ready\":true,\"status\":\"ok\"}", ""),
    ("failure", "ant_failure", "ant -f {path}.xml test", 1, "BUILD FAILED\nTests: {n}, Failures: 1, Errors: 0", ""),
    ("failure", "health_json_fail", "curl -sS https://{path}/ready", 0, "{\"ready\":false,\"status\":\"degraded\"}", ""),
    ("blocked", "redis_refused", "redis-cli -h {path} ping", 1, "", "Could not connect to Redis at {path}:6379: Connection refused"),
    ("blocked", "repo_unauthorized", "curl -i https://packages.{path}/artifact", 0, "HTTP/1.1 401 Unauthorized\nauthentication failed", ""),
    ("blocked", "config_access", "ruff check --config {path}.toml src", 2, "", "error: Permission denied (os error 13) while reading {path}.toml"),
    ("unknown", "ant_none", "ant -f {path}.xml test", 0, "BUILD SUCCESSFUL\nTests run: 0, Failures: 0\nNo tests executed", ""),
    ("unknown", "minitest_none", "ruby {path}_test.rb", 0, "0 runs, 0 assertions, 0 failures, 0 errors, 0 skips", ""),
    ("unknown", "generic_skipped", "./test-runner {path}", 0, "Tests: 0 passed, {n} skipped\nAll discovered tests were skipped.", ""),
]

TEST = [
    ("success", "maven_pass", "mvn test -Dtest={path}", 0, "[INFO] Tests run: {n}, Failures: 0, Errors: 0, Skipped: 0\n[INFO] BUILD SUCCESS", ""),
    ("success", "gradle_pass", "./gradlew test --tests {path}", 0, "{n} tests completed successfully\nBUILD SUCCESSFUL in {duration}s", ""),
    ("success", "rspec_pass", "bundle exec rspec spec/{path}", 0, "{n} examples, 0 failures\nFinished in {duration} seconds", ""),
    ("success", "phpunit_pass", "vendor/bin/phpunit tests/{path}", 0, "OK ({n} tests, {n} assertions)\nTime: {duration}s", ""),
    ("success", "dotnet_pass", "dotnet test tests/{path}", 0, "Passed!  - Failed: 0, Passed: {n}, Skipped: 0\nTest Run Successful.", ""),
    ("success", "cmake_pass", "cmake --build build/{path}", 0, "[100%] Built target {path}\nBuild finished successfully", ""),
    ("success", "make_pass", "make -C {path} all", 0, "make: Leaving directory '{path}'\nAll targets are up to date. Build completed.", ""),
    ("success", "kubectl_rollout", "kubectl rollout status deploy/{path}", 0, "deployment \"{path}\" successfully rolled out", ""),
    ("success", "ruff_clean", "ruff check src/{path}", 0, "All checks passed!", ""),
    ("success", "mypy_clean", "mypy src/{path}", 0, "Success: no issues found in {n} source files", ""),
    ("success", "git_push", "git push origin {path}", 0, "To https://example/{path}.git\n   a1b2c3d..e4f5a6b  {path} -> {path}\nEverything up-to-date", ""),
    ("success", "health_ok", "curl -fsS https://{path}/ready", 0, "{\"ready\":true,\"checks\":{\"database\":\"up\"}}", ""),

    ("failure", "maven_fail", "mvn test -Dtest={path}", 1, "[ERROR] Tests run: {n}, Failures: 1, Errors: 0\n[ERROR] BUILD FAILURE", ""),
    ("failure", "gradle_fail", "./gradlew test --tests {path}", 1, "{path} > test FAILED\nBUILD FAILED in {duration}s\n1 actionable task: 1 executed", ""),
    ("failure", "rspec_fail", "bundle exec rspec spec/{path}", 1, "{n} examples, 1 failure\nFailed examples:\nrspec ./spec/{path}.rb:12", ""),
    ("failure", "phpunit_fail", "vendor/bin/phpunit tests/{path}", 1, "FAILURES!\nTests: {n}, Assertions: {n}, Failures: 1.\nFailed asserting that false is true.", ""),
    ("failure", "dotnet_fail", "dotnet test tests/{path}", 1, "Failed!  - Failed: {n}, Passed: 2, Skipped: 0\nTest Run Failed.", ""),
    ("failure", "cmake_error", "cmake --build build/{path}", 2, "src/{path}.cpp:{n}:8: error: expected ‘;’ before ‘return’\nmake: *** [Makefile:91] Error 1", ""),
    ("failure", "make_error", "make -C {path} all", 2, "{path}.c:{n}: undefined reference to `main'\ncollect2: error: ld returned 1 exit status\nmake: *** Error 2", ""),
    ("failure", "kubectl_failed", "kubectl rollout status deploy/{path}", 1, "error: deployment \"{path}\" exceeded its progress deadline\ncontainer has crashloopbackoff", ""),
    ("failure", "ruff_errors", "ruff check src/{path}", 1, "src/{path}.py:{n}:5: F821 Undefined name `value`\nFound 1 error.", ""),
    ("failure", "mypy_errors", "mypy src/{path}", 1, "src/{path}.py:{n}: error: Incompatible return value type\nFound 1 error in 1 file", ""),
    ("failure", "health_fail", "curl -sS https://{path}/ready", 0, "{\"ready\":false,\"checks\":{\"database\":\"down\"}}", ""),
    ("failure", "node_uncaught", "node dist/{path}.js", 1, "node:internal/process/promises:{n}\n  triggerUncaughtException(err, true /* fromPromise */);\nError: Expected valid response", ""),

    ("blocked", "maven_auth", "mvn test -Dtest={path}", 1, "[ERROR] Could not transfer artifact {path} from/to central: authentication failed\nstatus code: 401, reason phrase: Unauthorized", ""),
    ("blocked", "gradle_access", "./gradlew test --tests {path}", 1, "", "FAILURE: Build failed with an exception.\nCould not create service of type FileSystem\nAccess is denied: C:\\{path}"),
    ("blocked", "rspec_load", "bundle exec rspec spec/{path}", 1, "An error occurred while loading ./spec/{path}_spec.rb.\nLoadError: cannot load such file -- spec_helper", ""),
    ("blocked", "php_extension", "vendor/bin/phpunit tests/{path}", 2, "PHP Fatal error: Uncaught Error: Call to undefined function curl_init()\nRequired extension ext-curl is missing", ""),
    ("blocked", "nuget_unavailable", "dotnet test tests/{path}", 1, "error NU1301: Unable to load the service index for source https://api.nuget.org/{path}\nThe remote name could not be resolved", ""),
    ("blocked", "compiler_missing", "cmake -S {path} -B build", 1, "CMake Error: Could not find CMAKE_C_COMPILER\nNo CMAKE_CXX_COMPILER could be found.", ""),
    ("blocked", "kube_forbidden", "kubectl rollout status deploy/{path}", 1, "Error from server (Forbidden): deployments.apps \"{path}\" is forbidden: User cannot get resource", ""),
    ("blocked", "db_unavailable", "psql {path} -c 'select 1'", 2, "psql: error: connection to server at \"{path}\" failed: Connection refused\nIs the server running on that host?", ""),
    ("blocked", "ruff_config", "ruff check src/{path}", 2, "error: Failed to read {path}/pyproject.toml: Permission denied (os error 13)", ""),
    ("blocked", "quota_exceeded", "gcloud run deploy {path}", 1, "ERROR: (gcloud.run.deploy) PERMISSION_DENIED: Quota exceeded for quota metric 'Read requests'", ""),
    ("blocked", "tool_absent", "dotnet test {path}", 127, "dotnet: The term 'dotnet' is not recognized as the name of a cmdlet.", ""),
    ("blocked", "offline", "bundle exec rspec {path}", 1, "Bundler::HTTPError: Network request failed. You are currently offline and the requested gem is not cached.", ""),

    ("unknown", "maven_none", "mvn test -Dtest={path}", 0, "[INFO] Tests run: 0, Failures: 0, Errors: 0, Skipped: 0\n[INFO] BUILD SUCCESS\n[INFO] No tests to run.", ""),
    ("unknown", "gradle_none", "./gradlew test --tests {path}", 0, "NO-SOURCE\nSkipping task ':test' as it has no source files\nBUILD SUCCESSFUL", ""),
    ("unknown", "rspec_none", "bundle exec rspec spec/{path}", 0, "0 examples, 0 failures\nNo examples found.", ""),
    ("unknown", "phpunit_none", "vendor/bin/phpunit tests/{path}", 1, "No tests executed!\nThe test suite is empty.", ""),
    ("unknown", "dotnet_skipped", "dotnet test tests/{path}", 0, "Passed! - Failed: 0, Passed: 0, Skipped: {n}\nAll discovered tests were skipped.", ""),
    ("unknown", "ctest_none", "ctest --test-dir build/{path}", 0, "No tests were found!!!\n0% tests passed, 0 tests failed out of 0", ""),
    ("unknown", "make_noop", "make -C {path} verify", 0, "make: Nothing to be done for 'verify'.\nNo commands were executed.", ""),
    ("unknown", "kube_dry", "kubectl apply --dry-run=server -f {path}.yaml", 0, "deployment.apps/{path} configured (server dry run)\nNo object was persisted.", ""),
    ("unknown", "verify_silent", "./gradlew {path}:verify", 0, "", ""),
    ("unknown", "cut_output", "mvn test -Dtest={path}", 0, "[INFO] Scanning for projects...\n[remaining output omitted by logger]", ""),
    ("unknown", "deprecation", "bundle exec rspec {path}", 0, "DEPRECATION WARNING: The legacy formatter is deprecated and will be removed.", ""),
    ("unknown", "deployment_wait", "gcloud run deploy {path}", 0, "Deploying container to Cloud Run service [{path}]\nOperation is still running; result not available.", ""),
]


def _vary(text: str, n: int, path: str, duration: str) -> str:
    return text.replace("{n}", str(n)).replace("{path}", path).replace("{duration}", duration)


def build(split: str) -> list[dict]:
    specs = TRAIN if split == "train" else TEST
    variants = 24 if split == "train" else 4
    paths = ["payments", "auth", "search", "billing", "profile", "checkout", "catalog", "upload"]
    records = []
    for index, (label, family, command, code, stdout, stderr) in enumerate(specs):
        for variant in range(variants):
            n = variant + 1
            path = paths[(index + variant) % len(paths)]
            if variant % 3 == 1:
                path += f"/module_{n}"
            elif variant % 3 == 2:
                path += f"-v{n}"
            duration = f"{(variant % 9) + 0.13:.2f}"
            records.append({
                "id": f"{split}-{family}-{variant:02d}",
                "command": _vary(command, n, path, duration),
                "exit_code": code,
                "stdout": _vary(stdout, n, path, duration),
                "stderr": _vary(stderr, n, path, duration),
                "label": label,
                "family": family,
                "source": "synthetic-template",
            })
    return records
