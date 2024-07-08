# Python Microservice Template

This repository contains a minimal "enrichment app" built to demonstrate a standardized setup for Python-based microservices used in Valley Forge. This readme will guide you through the basic layout and tooling of the repository. Additionally, you will find documentation throughout the repo.

## Goal

Reduce the amount of time spent writing boilerplate code and figuring out how to configure Python microservices to work with Kafka.

## Objectives

- Improve interoperability between services
- Reuse boilerplate code used to connect to Kafka and robustly ingest messages
- Simplify packaging through use of a similar technology stack and deployment patterns
- Encourage healthy CI/CD practices that alleviate stress on the build servers

## Usage

This template service is minimally functional. It accepts a single string and returns that string + " goodbye". You can integrate this into your current stack by copying the service specification in the Compose file into your own. Be sure to also copy over the environment variables. You can find the Kafka topics messages will be consumed from and produced to in `.env`.

## Testing

At a minimum, it's a good idea to test your enrichment module. There are partially implemented tests available in `tests/test_enrich.py`. Tests can be run calling `pytest` from the root directory.

Integration tests are also partially implemented under the `tests/integration_testing` directory. These tests can be calling the `run_integration_tests.sh` bash script from the integration_testing directory. The script will forward the exit code that Pytest produces within the container to the shell it was called in.

## Printing the Software Bill of Materials (SBOM)

You can use the command `cyclonedx-py environment` to generate a JSON object defining the SBOM in the OWASP CycloneDX format.

## Contributing

Feel free to offer changes through new PRs. Reach out to Stephen Melsom or Nick Newman for review/approval.

## Todo

- [ ] Determine how to best prevent and handle OOM errors. Especially for services that process a variable amount of data.
- [ ] Combine downloader scripts into a single downloader tool
- [ ] Add examples to `get_resources.sh`
