# Testing

Minimal __unit tests__ and __integration__ tests are provided to encourage test driven development and provide a basic pattern for testing.

## Unit Tests

To run the unit tests, you will first need to set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/text.txt
```

After your virtual environment has been set up, call `pytest` from the root directory. The tests will be run and the results will be printed to stdout.

### Contributing

Adapting the unit tests to you application only requires updating `test_enrich.py`. Update and add test cases that fit your needs.

## Integration Tests

Integration tests are much more involved and designed to more closely simulate production. Running the integration tests consists of standing up a Kafka container, a test container, and an app container. The test procedure is detailed below:

1. From the test container, generate and publish a message to Kafka.
2. The app container will process the message and publish a new message to Kafka.
3. The test container will receive and evaluate the message to ensure it was processed correctly.

The integration tests are run using the `run_integration_tests.sh` script. The script will build and start the containers, run the tests, and stop the containers.

### Contributing

Adapting the integration tests to your app requires changes to two files: `run_integration_tests.sh` and `test_service.py`.

The only change that needs to be made to `run_integration_tests.sh` is updating the app name to match the name in the root directory `compose.yml` file. The app name is found on line 10 in the shell script.

The `test_service.py` file needs to be updated in several places:
- `Config.consumer_topics` must match ___producer_topic___ found in `config.py`
- `Config.producer_topic` must match ___consumer_topic___ found in `config.py`
- `Config.group_id` must match the __group_id__ found in `config.py`
- Update the message (`msg`) sent to your app
- Adapt the assertion to properly test your app
- [optional] Update the consumer polling timeout if your service takes longer than the default value

#### Debugging

Debugging the integration tests can be challenging due to the containerized and distributed nature of the tests. It is important to note that both the test and app containers are rebuilt whenever `run_integration_tests.sh` is executed.

#### Tips

- Start with the unit tests before moving on to integration tests.
- Add "-s" to the test container entrypoint in `Dockerfile.test` to disable pytest stdout capture and instead print to console. This is needed if you want to add print/log statements.
- If your running into errors, it's always best to first read message contents.
